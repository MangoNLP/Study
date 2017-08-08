import re
import scrapy
import requests

from urllib.parse import unquote
from bs4 import BeautifulSoup as bs
from collections import namedtuple

from scrapy.loader import ItemLoader
from parsing.items import ParsingItem


Regular = namedtuple('Regular', 'reg, func')

domain_reg = re.compile(r'(?:https?://)?(.[^/?]*)')


def trim(text):
    return unquote(text).replace('\n', '').strip()


class NewsSpider(scrapy.Spider):
    # Scrapy Document: https://doc.scrapy.org/en/1.1/index.html
    name = 'news'
    custom_settings = {
        "ITEM_PIPELINES": {
            'parsing.pipelines.ParsingPipeline': 800,
        },
    }

    # news_query = 'https://search.naver.com/search.naver?where=news&query=%s'
    news_query = 'http://newssearch.naver.com/search.naver?where=rss&query=%s&field=1'

    non_parser_lst = []

    def __init__(self, name=None, **kwargs):
        super(NewsSpider, self).__init__(name, **kwargs)
        self.regs = self.get_parser()

    def get_parser(self):
        return [
            # 중앙일보
            Regular(re.compile(r'(?:https?://)?news.joins.com/?(.*)?'), self.parser_center),
            Regular(re.compile(r'(?:https?://)?news.joins.com/?(.*)?'), self.parser_center),

            # 네이버 뉴스
            Regular(re.compile(r'(?:https?://)?sports.news.naver.com/?(.*)?'), self.parser_naver_sport),

            # 네이버 연애
            Regular(re.compile(r'(?:https?://)?entertain.naver.com/?(.*)?'), self.parser_naver_entertain),
        ]

    def start_requests(self):
        '''키워드 별 리퀘스트 (뉴스 컨텐츠)'''
        keywords = self.get_hotkeyword()
        urls = [(self.news_query % keyword.text) for keyword in keywords]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def get_hotkeyword(self):
        '''실검 키워드 가져오기'''
        res = requests.get('https://www.naver.com')
        soup = bs(res.text, 'lxml')
        items = soup.find_all('ul', class_='ah_l', attrs={'data-list': "1to10"})
        # print(items[0])
        item = items[0]
        keywords = item.find_all('span', class_='ah_k')
        return keywords

    def parse(self, response):
        '''rss feed 수신 후 각 언론사 파서에 전달'''
        soup = bs(response.text, 'xml')
        items = soup.find_all('item')
        for item in items:
            link = item.link.text
            domain = domain_reg.search(link).groups()[0]

            for obj in self.regs:
                if obj.reg.match(link):
                    yield scrapy.Request(url=link, callback=obj.func)
                    break
            else:
                self.non_parser_lst += [domain]
                yield self.parser_undefine(item)

    def close(self, reason):
        non_parser_list = set(self.non_parser_lst)
        print(non_parser_list)

    def parser_center(self, response):
        '''중앙일보'''
        soup = bs(response.text, 'lxml')

        title = trim(soup.find(class_='subject').text)
        writer = trim(soup.find('div', class_='byline').em.text)
        body = trim(soup.find(id='article_body').text)
        update_at = soup.find('div', class_='byline').next_sibling

        yield ParsingItem(
            title=title,
            writer=writer,
            media="중앙일보",
            update_at=update_at,
            url=response.request.url,
            body=body,
        )

    def parser_naver_sport(self, response):
        '''네이버 스포츠'''
        soup = bs(response.text, 'lxml')
        content = soup.find('div', class_='content_area')

        headline = content.find('div', class_='news_headline')
        body = content.find(id='newsEndContents').text
        yield ParsingItem(
            title=trim(headline.h4.text),
            writer=trim(headline.span.img['alt']),
            media="네이버 스포츠",
            update_at=headline.div.span.next_sibling.next_sibling.text,
            url=response.request.url,
            body=body,
        )

    def parser_naver_entertain(self, response):
        '''네이버 연애'''
        soup = bs(response.text, 'lxml')
        content = soup.find('div', class_='end_ct')
        body = content.find('div', class_='end_body_wrp')
        body.script.decompose()

        yield ParsingItem(
            title=trim(content.div.h2.text),
            writer=trim(content.div.div.a.img['alt']),
            media="네이버 TV연애",
            update_at=content.find('div', class_='article_info').span.em,
            url=response.request.url,
            body=body,
        )

    def parser_undefine(self, item):
        '''파서 없는곳. rss 피드 저장'''
        return ParsingItem(
            title=trim(item.title.text),
            writer=trim(item.author.text),
            media="RSS Feed",
            update_at=trim(item.pubDate.text),
            url=item.link.text,
            body=trim(item.description.text),
        )

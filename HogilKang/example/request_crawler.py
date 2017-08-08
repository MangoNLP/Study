import requests
import time

from bs4 import BeautifulSoup as bs
from .base import BaseCrawler


class RequestCrawler(BaseCrawler):
    urls = []

    def __init__(self, urls=[]):
        res = requests.get('https://www.naver.com')
        soup = bs(res.text, 'lxml')
        items = soup.find_all('ul', class_='ah_l', attrs={'data-list': "1to10"})
        # print(items[0])
        item = items[0]
        urls = [item.li.a['href']] + [i.a['href'] for i in item.li.find_next_siblings('li')]
        self.urls = urls

    def send_request(self, url):
        return requests.get(url)

    def pipe_line(self, item):
        data = self.get_content(item)
        print('end pipe')

    def parser(self, response):
        soup = bs(response.text, 'lxml')

        news_section = soup('div', class_='news section')
        news = news_section[0]
        a = news.findChildren('a', attrs={'class': ['_sp_each_url', '_sp_each_title']})

        for i in a:
            if i.has_attr('title'):
                print(i['title'])
                yield i['href']

    def get_content(self, url):
        res = requests.get(url)
        return res.text

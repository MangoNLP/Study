from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup as bs
from time import time
from time import sleep
from pprint import pprint as p


PROCESS = 4


def get_news(lst):
    """ 뉴스 안에 내용 """
    res = []
    for i in lst:
        res += [requests.get(i)]
    return res


def get_content(url):
    """ 검색했을 때 노출되는 뉴스 컨텐츠 """
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    news_section = soup('div', class_='news section')
    news = news_section[0]
    a = news.findChildren('a', attrs={'class': ['_sp_each_url', '_sp_each_title']})

    lst = []
    for i in a:
        if i.has_attr('title'):
            lst += [i['href']]

    return lst


def get_hot_keyword_list():
    """ 실검 리스팅 """
    res = requests.get('https://www.naver.com')
    soup = bs(res.text, 'lxml')
    items = soup.find_all('ul', class_='ah_l', attrs={'data-list': "1to10"})
    # print(items[0])
    item = items[0]
    urls = [item.li.a['href']] + [i.a['href'] for i in item.li.find_next_siblings('li')]
    return urls


if __name__ == '__main__':
    s = time()

    pool = Pool(processes=PROCESS)
    urls = get_hot_keyword_list()

    result = pool.map(get_content, urls)
    result = pool.map(get_news, result)
    p(result)

    e = time()
    print("%s sec" % (e - s))

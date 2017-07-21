from time import time, sleep

from multiprocessing import Pool, Queue, Process
from selenium.webdriver import Chrome, PhantomJS
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("window-size=1,1")


PROCESS = 4


class Task(object):

    SEARCH = '검색'
    CONTENT = "뉴스 목록 가져오기"
    NEWS = "뉴스안에 내용 가져오기"
    END_TASK = "END_TASK"

    def __init__(self, type, url):
        self.type = type
        self.url = url


def get_news(driver, url):
    """ 뉴스 안에 내용 """
    driver.get(url)
    return driver.page_source


def get_content(driver, url):
    """ 검색했을 때 노출되는 뉴스 컨텐츠 """
    driver.get(url)

    elem = driver.find_element_by_xpath('//*[@id="main_pack"]/div[@class="news section"]/ul')
    news = elem.find_elements_by_xpath('li/dl/dt/a')
    lst = []
    for i in news:
        print(i.get_property('title'))
        lst += [i.get_property('href')]

    return lst


def get_hot_keyword_list(driver):
    """ 실검 리스팅 """
    driver.get("https://www.naver.com")
    elems = driver.find_elements_by_xpath('//*[@id="PM_ID_ct"]/div[1]/div[2]/div[2]/div[2]/ul[1]/li')
    urls = [elem.find_element_by_tag_name('a').get_attribute('href') for elem in elems]
    return urls


def start(queue):
    # Chrome
    # driver = Chrome(chrome_options=chrome_options)

    # Headless
    driver = PhantomJS()

    while 1:
        task = queue.get()

        if task.type == task.SEARCH:
            lst = get_content(driver, task.url)
            [queue.put(Task(Task.CONTENT, url)) for url in lst]

        if task.type == task.CONTENT:
            news_html = get_news(driver, task.url)
            print("news html", task.url)

        if task == "END_TASK":
            break
        if queue.empty():
            print('empty')
            continue

    driver.close()


if __name__ == '__main__':
    s = time()
    pool = Pool(processes=PROCESS)
    queue = Queue()

    driver = Chrome()
    urls = get_hot_keyword_list(driver)
    driver.close()

    for url in urls:
        queue.put(Task(Task.SEARCH, url))
    drivers = [Process(target=start, args=(queue,),).start() for i in range(PROCESS)]

    sleep(10)
    for process in range(PROCESS):
        queue.put(Task(Task.END_TASK, None),)

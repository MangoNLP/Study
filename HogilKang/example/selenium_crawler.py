from .base import BaseCrawler
from selenium.webdriver import Chrome, PhantomJS
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("window-size=1,1")


driver = Chrome
# driver = PhantomJS


class SeleniumCrawler(BaseCrawler):
    urls = []
    contents = []

    def __init__(self, urls=None):
        # Chrome
        self.driver = [driver(), ]
        # self.driver = [PhantomJS(), PhantomJS()]
        self.driver[0].implicitly_wait(1)

        self.driver[0].get("https://www.naver.com")
        elems = self.driver[0].find_elements_by_xpath('//*[@id="PM_ID_ct"]/div[1]/div[2]/div[2]/div[2]/ul[1]/li')
        urls = [elem.find_element_by_tag_name('a').get_attribute('href') for elem in elems]
        self.urls = urls

    def pipe_line(self, item):
        self.driver[0].get(item)
        data = self.driver[0].page_source

    def parser(self, response):
        elem = self.driver[0].find_element_by_xpath('//*[@id="main_pack"]/div[@class="news section"]/ul')
        news = elem.find_elements_by_xpath('li/dl/dt/a')
        lst = []
        for i in news:
            print(i.get_property('title'))
            lst += [i.get_property('href')]

        for i in lst:
            yield i

    def send_request(self, url):
        self.driver[0].get(url)

    # def get_content(self, url):
    #     self.driver[1].get(url)
    #     return self.driver[1].page_source

    def close(self):
        for driver in self.driver:
            driver.close()


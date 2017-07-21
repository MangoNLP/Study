from time import time

from HogilKang.example.request_crawler import RequestCrawler
from HogilKang.example.selenium_crawler import SeleniumCrawler


if __name__ == '__main__':
    s = time()

    rc = RequestCrawler()
    rc.start()

    # sc = SeleniumCrawler()
    # sc.start()
    # sc.close()

    e = time()
    print('%.2f sec' % (e-s))


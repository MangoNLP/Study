from abc import ABCMeta, abstractmethod


class BaseCrawler:
    __metaclass__ = ABCMeta
    urls = []

    @abstractmethod
    def parser(self, response: any) -> any:
        """
        Item Parsing Logic
        :param response:
        :return:
        """

    @abstractmethod
    def pipe_line(self, item: any) -> any:
        """
        Item Pipe Line
        :param item:
        :return:
        """

    @abstractmethod
    def send_request(self, url: str) -> any:
        """
        Send Request
        :param url:
        :return: Response Data for Parser
        """

    def set_urls(self, urls: list) -> None:
        """
        Setting url list
        :param urls: request to url
        :type
        :return: None
        """
        self.urls = urls

    def start(self) -> None:
        urls = iter(self.urls)

        for url in urls:
            response = self.send_request(url)
            for item in self.parser(response):
                self.pipe_line(item)

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, QQmlListProperty, qmlRegisterType
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from GoogleScraper import scrape_with_config, GoogleSearchError

from borda_method import MetasearchResultsAggregator

DEBUG = True


class Link(QObject):
    nameChanged = pyqtSignal()
    titleChanged = pyqtSignal()

    def __init__(self, name='', title='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._title = title

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name != self._name:
            self._name = name
            self.nameChanged.emit()

    @pyqtProperty('QString', notify=titleChanged)
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if title != self._title:
            self._title = title
            self.titleChanged.emit()


class StoreLinks(QObject):
    linksChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._links = []

    @pyqtProperty(QQmlListProperty, notify=linksChanged)
    def links(self):
        return QQmlListProperty(Link, self, self._links)

    @links.setter
    def links(self, links):
        if links != self._links:
            self._links = links
            self.linksChanged.emit()

    def appendLink(self, link):
        self._links.append(link)
        self.linksChanged.emit()


class WebSearcher(QObject):

    def __init__(self):
        self.search = ""

        self._numberPagesForKeyword = 3
        self._searchersNames = list()
        self._searchers = dict(baidu=StoreLinks(), bing=StoreLinks(), google=StoreLinks(),
                               yahoo=StoreLinks(), duckduckgo=StoreLinks())
        self._rangingList = StoreLinks()
        super().__init__()

    @pyqtSlot(str)
    def searchTextByAllEngines(self, search_text):

        config = {
            'proxy': 'socks5 localhost 9050',
            'use_own_ip': True,
            'keyword': search_text,
            'search_engines': self._searchersNames,
            'num_pages_for_keyword': self._numberPagesForKeyword,
            'scrape_method': 'http-async',
            'do_caching': False
        }
        try:
            self.search = scrape_with_config(config)

            engines_links = dict()
            for searcher in self._searchersNames:
                links = self.getURLsByEngine(searcher)
                engines_links[searcher] = links

                for url in links:
                    self._searchers[searcher].appendLink(Link(url, url))

            aggregator = MetasearchResultsAggregator(engines_links)
            # TODO: aggregate all links
            print(f"M = {aggregator.range_sequence_length}")
            aggregated_links_list = aggregator.get_ranked_link_list()
            print('Range result', aggregated_links_list)
            

        except GoogleSearchError as e:
            print(e)

    @pyqtSlot(str, str)
    def searchTextByEngine(self, search_text, engine_name):

        config = {
            'proxy': 'socks5 localhost 9050',
            'use_own_ip': True,
            'keyword': search_text,
            'search_engines': [engine_name],
            'num_pages_for_keyword': self._numberPagesForKeyword,
            'scrape_method': 'http-async',
            'do_caching': False
        }

        try:
            self.search = scrape_with_config(config)
            links = self.getURLsByEngine(engine_name)

            for url in links:
                self._searchers[engine_name].appendLink(Link(url, url))

        except GoogleSearchError as e:
            print(e)

    @pyqtSlot(str)
    def getURLsByEngine(self, name):

        result_links = []

        for serp in self.search.serps:
            if name == serp.search_engine_name:

                for lnk in serp.links:
                    if lnk.link:
                        result_links.append(lnk.link)

        return result_links

    baiduChanged = pyqtSignal()
    bingChanged = pyqtSignal()
    googleChanged = pyqtSignal()
    yahooChanged = pyqtSignal()
    duckduckgoChanged = pyqtSignal()
    rangingListChanged = pyqtSignal()

    @pyqtProperty(StoreLinks, notify=baiduChanged)
    def baidu(self):
        return self._searchers["baidu"]

    @pyqtProperty(StoreLinks, notify=bingChanged)
    def bing(self):
        return self._searchers["bing"]

    @pyqtProperty(StoreLinks, notify=googleChanged)
    def google(self):
        return self._searchers["google"]

    @pyqtProperty(StoreLinks, notify=yahooChanged)
    def yahoo(self):
        return self._searchers["yahoo"]

    @pyqtProperty(StoreLinks, notify=duckduckgoChanged)
    def duckduckgo(self):
        return self._searchers["duckduckgo"]

    @pyqtProperty(StoreLinks, notify=rangingListChanged)
    def rangingList(self):
        return self._rangingList

    searchersNamesChanged = pyqtSignal()

    @pyqtProperty(list, notify=searchersNamesChanged)
    def searchersNames(self):
        return self._searchersNames

    @searchersNames.setter
    def searchersNames(self, searchersNames):
        if searchersNames != self._searchersNames:
            self._searchersNames = searchersNames
            self.searchersNamesChanged.emit()

    numberPagesForKeywordChanged = pyqtSignal()

    @pyqtProperty(int, notify=numberPagesForKeywordChanged)
    def numberPagesForKeyword(self):
        return self._numberPagesForKeyword

    @numberPagesForKeyword.setter
    def numberPagesForKeyword(self, numberPagesForKeyword):
        if numberPagesForKeyword != self._numberPagesForKeyword:
            self._numberPagesForKeyword = numberPagesForKeyword
            self.numberPagesForKeywordChanged.emit()


if __name__ == "__main__":
    import sys

    # создаём экземпляр приложения
    app = QGuiApplication(sys.argv)

    qmlRegisterType(Link, 'SearchTypes', 1, 0, 'Link')
    qmlRegisterType(StoreLinks, 'SearchTypes', 1, 0, 'StoreLinks')

    # создаём QML движок
    engine = QQmlApplicationEngine()
    # создаём объект SearchEngine
    searchEngine = WebSearcher()

    # и регистрируем его в контексте QML
    engine.rootContext().setContextProperty("searchEngine", searchEngine)
    # загружаем файл qml в движок
    engine.load("main.qml")

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())

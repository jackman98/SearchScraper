from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, QQmlListProperty, qmlRegisterType
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from GoogleScraper import scrape_with_config, GoogleSearchError

DEBUG = True
SEARCHERS = ['yandex', 'bing', 'google', 'yahoo', 'duckduckgo']


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

        self._searchers = dict(yandex=StoreLinks(), bing=StoreLinks(), google=StoreLinks(),
                               yahoo=StoreLinks(), duckduckgo=StoreLinks())
        super().__init__()

    resultReceived = pyqtSignal(str, bool, arguments=['searchEngineName', 'isSuccessful'])

    @pyqtSlot(str)
    def searchTextByAllEngines(self, search_text):

        for searcher in SEARCHERS:
            config = {
                'use_own_ip': True,
                'keyword': search_text,
                'search_engines': [searcher],
                'num_pages_for_keyword': 1,
                'scrape_method': 'http',
                'do_caching': False
            }

            try:
                self.search = scrape_with_config(config)

                links = self.getURLsByEngine(searcher)

                for url in links:
                    self._searchers[searcher].appendLink(Link(url, url))

                self.resultReceived.emit(searcher, True)
            except GoogleSearchError as e:
                print(e)

    @pyqtSlot(str, str)
    def searchTextByEngine(self, search_text, engine_name):

        config = {
            'use_own_ip': True,
            'keyword': search_text,
            'search_engines': [engine_name],
            'num_pages_for_keyword': 1,
            'scrape_method': 'http',
            'do_caching': False
        }

        try:
            self.search = scrape_with_config(config)
            links = self.getURLsByEngine(engine_name)

            for url in links:
                self._searchers[engine_name].appendLink(Link(url, url))

            self.resultReceived.emit(engine_name, True)
        except GoogleSearchError as e:
            print(e)

    @pyqtSlot(str)
    def getURLsByEngine(self, name):

        for serp in self.search.serps:
            if name == serp.search_engine_name:
                if DEBUG:
                    print(serp.search_engine_name)
                    print(serp.page_number)

                result_links = []
                for lnk in serp.links:
                    if lnk.link:
                        result_links.append(lnk.link)

                return result_links

    yandexChanged = pyqtSignal()
    bingChanged = pyqtSignal()
    googleChanged = pyqtSignal()
    yahooChanged = pyqtSignal()
    duckduckgoChanged = pyqtSignal()

    @pyqtProperty(StoreLinks, notify=yandexChanged)
    def yandex(self):
        return self._searchers["yandex"]

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

    # searchEngine.searchTextByEngine('Dima', 'bing')
    # links = searchEngine.getURLsByEngine('bing')
    #
    # print(links)

    # и регистрируем его в контексте QML
    engine.rootContext().setContextProperty("searchEngine", searchEngine)
    # загружаем файл qml в движок
    engine.load("main.qml")

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())

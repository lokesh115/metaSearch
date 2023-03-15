class scrapers:
    def search_google(self, query, userAgent):
        from ScrapeSearchEngine.ScrapeSearchEngine import Google
        try:
            google = Google(query, userAgent)
        except:
            google = []
        return google

    def search_duck_duck_go(self, query, userAgent):
        from ScrapeSearchEngine.ScrapeSearchEngine import Duckduckgo
        duckduckgo = Duckduckgo(query, userAgent)
        utf_lst=[("%3A",":"),("%2F","/"),("%2D","-")]
        for i in range(len(duckduckgo)):
            url=duckduckgo[i][25:-69]
            for tup in utf_lst:
                url=url.replace(tup[0],tup[1])
            duckduckgo[i]=url
        return duckduckgo

    def search_bing(self, query, userAgent):
        from ScrapeSearchEngine.ScrapeSearchEngine import Bing
        try:
            bing = Bing(query, userAgent)
        except:
            bing = []
        return bing

    def search_yahoo(self, query, userAgent):
        from ScrapeSearchEngine.ScrapeSearchEngine import Yahoo
        yahoo = Yahoo(query, userAgent)
        return yahoo

    def search_ecosia(self, query, userAgent):
        from ScrapeSearchEngine.ScrapeSearchEngine import Ecosia
        ecosia = Ecosia(query, userAgent)
        return ecosia

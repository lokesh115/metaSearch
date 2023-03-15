class mse:
    def __init__(self,ua,query):
        self.userAgent = ua
        self.query = query
    def search_query(self):
        from . import scrapers
        from . import algorithms
        search = scrapers.scrapers()
        algorithms = algorithms.algorithms()
        google_results = search.search_google(self.query, self.userAgent)
        bing_results = search.search_bing(self.query, self.userAgent)
        yahoo_results = search.search_yahoo(self.query, self.userAgent)
        ddgo_results = search.search_duck_duck_go(self.query, self.userAgent)
        print("Results fetched!")
        results = [google_results, bing_results,yahoo_results, ddgo_results]

        ranked_results = algorithms.get_ranks(self.query, results)

        for i in range(len(ranked_results)):
            ranked_results[i] = list(ranked_results[i])
            ranked_results[i].append(self.query.capitalize())
        
        return ranked_results
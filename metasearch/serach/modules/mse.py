class mse:
    def __init__(self, ua, query):
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
        results = []
        for result in [(google_results, "google"), (bing_results, "bing"), (yahoo_results, "yahoo"), (ddgo_results, "ddgo")]:
            if len(result[0]) == 0:
                continue
            else:
                results.append((result[0], result[1]))
        print(
            f"Google : {len(google_results)}, Bing : {len(bing_results)}, Yahoo : {len(yahoo_results)}, Ddgo : {len(ddgo_results)}")
        #print(f"results : {results}")
        ranked_results = algorithms.ranking_alg(self.query, results)
        return ranked_results

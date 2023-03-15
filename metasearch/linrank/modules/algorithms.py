from . import semantic
class algorithms:
    def ranked_order(self, ranks):
        sorted_docs = sorted(ranks.items(), key=lambda kv: (
            kv[1], kv[0]), reverse=True)
        return sorted_docs

    def get_rank_dict(self,results):
        size = 99
        len_check = 0
        for i in range(len(results)):
            if len(results[i-len_check]) == 0:
                results.pop(i-len_check)
                len_check += 1
            elif len(results[i-len_check]) < size:
                size = len(results[i-len_check])
        ranks = dict()
        for result in results:
            for i in range(size):
                if result[i] not in ranks.keys():
                    ranks[result[i]] = 0
        return (ranks,size)
    # With normalization
    def normalized_linear_search(self, results1, results2, results3, results4):
        ranks = dict()
        for results in [results1, results2, results3, results4]:
            size = len(results)
            for i in range(len(results)):
                if results[i] not in ranks.keys():
                    ranks[results[i]] = (size-i+1)*100/size
                else:
                    ranks[results[i]] += (size-i+1)*100/size
        return ranks

    # Considering the results no. as that of the SE giving the least no. of results
    def linear_search(self,size,ranks,results):
        for result in results:
            for i in range(size):
                ranks[result[i]] += (size-i+1)
        for url in ranks.keys():
            ranks[url] *= 1.5

        return ranks

    def novel_approach(self, query, results):
        ranks,size = self.get_rank_dict(results)
        return self.ranked_order(ranks)
        lin_ranks = self.linear_search(size,ranks,results)
        print("Linear ranked!")

        sem = semantic.Semantic_search()
        sem_ranks = sem.start_semantic(query, ranks)
        print("Semantic ranked!")
        total_ranks = dict()
        for key in lin_ranks.keys():
            '''
            total_ranks[key] = [lin_ranks[key]+sem_ranks[key],lin_ranks[key], sem_ranks[key]]
            total_ranks[key] = lin_ranks[key]
            '''
            #total_ranks[key] = sem_ranks[key]
            total_ranks[key] = lin_ranks[key]+sem_ranks[key]

        return (self.ranked_order(total_ranks))
    def get_ranks(self, query, results):
        ranks,size = self.get_rank_dict(results)
        return self.ranked_order(ranks)
        
from . import semantic
from . import genetic


class algorithms:
    def ranked_order(self, ranks):
        sorted_docs = sorted(ranks.items(), key=lambda kv: (
            kv[1], kv[0]), reverse=True)
        return sorted_docs

    def get_rank_dict(self, results):
        size = 99
        for i in range(len(results)):
            if len(results[i][0]) < size and len(results[i][0]) != 0:
                size = len(results[i][0])
        ranks = dict()
        for res in results:
            result = res[0]
            site = res[1]
            for i in range(size):
                if result[i] not in ranks.keys():
                    ranks[result[i]] = [0, site]
                else:
                    ranks[result[i]][1] += f",{site}"
        return (ranks, size, results)
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
    def linear_search(self, size, ranks, results):
        for res in results:
            result = res[0]
            # print((result))
            site = res[1]
            for i in range(size):
                ranks[result[i]][0] += (size-i+1)
        for url in ranks.keys():
            ranks[url][0] *= 1.5
        return ranks

    def novel_approach(self, query, results):
        ranks, size, results = self.get_rank_dict(results)
        print(size)
        import copy
        lin_ranks = copy.deepcopy(ranks)
        sem_ranks = copy.deepcopy(ranks)

        lin_ranks = self.linear_search(size, lin_ranks, results)
        print("Linear ranked!")

        sem = semantic.Semantic_search()
        sem_ranks, titles = sem.start_semantic(query, sem_ranks)
        print("Semantic ranked!")

        total_ranks = dict()
        for key in lin_ranks.keys():
            '''
            total_ranks[key] = [lin_ranks[key]+sem_ranks[key],lin_ranks[key], sem_ranks[key]]
            total_ranks[key] = lin_ranks[key]
            '''
            #total_ranks[key] = sem_ranks[key]
            total_ranks[key] = [lin_ranks[key][0],sem_ranks[key][0], lin_ranks[key][1], titles[key]]
        return (total_ranks)
    
    def ranking_alg(self, query, results):
        ranks = self.novel_approach(query, results)
        gen = genetic.genetic(query, results, ranks)
        res = gen.start_ranking()
        print("Genetic Alg executed!!")
        print()
        print("Proposed Approach : ")
        for key in res.keys():
            print(f"{key} : {res[key][0]} , {res[key][1]} , {res[key][2]}, {ranks[key][0]}, {ranks[key][1]}")
        return (self.ranked_order(res))

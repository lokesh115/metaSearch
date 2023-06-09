# self.ranks[i][0] --> lin_rank
# self.ranks[i][1] --> sem_rank
# self.ranks[i][2] --> search engines

class genetic:
    def __init__(self, query, results, ranks):
        self.query = query
        self.results = results
        self.ranks = ranks

    def func(self, x, y):
        arg_vector = []
        s = 0
        for url in self.ranks.keys():
            tot = self.ranks[url][0]*x + self.ranks[url][1]*y
            arg_vector.append(tot)
            s+=tot
        l = len(arg_vector)
        if l==0:
            return 0 
        mu = s/l
        deviation_mean = []
        for i in arg_vector:
            deviation_mean.append(abs(i-mu))
        dev_sum = sum(deviation_mean)
        sim = []
        for i in deviation_mean:
            sim.append(1-((i/dev_sum)))
        sim_sum = sum(sim)
        w_vec = []
        for i in sim:
            w_vec.append(i/sim_sum)
        dowa = 0
        for i in range(len(w_vec)):
            dowa+=w_vec[i]*arg_vector[i]
            
        #print(x,y,f)
        #print(sim,deviation_mean,arg_vector)

        return dowa,deviation_mean

    def fitness(self, x, y):
        dowa, dev_mean = self.func(x, y)

        if min(dev_mean)<100:
            return 99999
        else:
            return abs(dowa)

    def start_ranking(self):
        # generate solutions
        import random
        solutions = []
        for s in range(1000):
            solutions.append((random.uniform(0, 10000),
                              random.uniform(0, 10000)))
        coun = 0
        for i in range(10000):
            coun+=1
            rankedsolutions = []
            for s in solutions:
                rankedsolutions.append((self.fitness(s[0], s[1]), s))
            rankedsolutions.sort()
            rankedsolutions.reverse()

            print(f"=== Gen {i} best solutions ===")
            print(rankedsolutions[0])

            bestsolutions = rankedsolutions[:100]

            if rankedsolutions[0][0] > 999999:
                final = rankedsolutions[0][1]
                break

            elements = []
            for s in bestsolutions:
                elements.append(s[1][0])
                elements.append(s[1][1])

            newGen = []
            for _ in range(1000):
                e1 = random.choice(elements) * random.uniform(0.99, 1.01)
                e2 = random.choice(elements) * random.uniform(0.99, 1.01)

                newGen.append((e1, e2))

            solutions = newGen
        total = dict()
        x, y = final[0], final[1]
        gen_ranks = dict()
        for url in self.ranks.keys():
            gen_ranks[url] = (self.ranks[url][0]*x +
                          self.ranks[url][1]*y)
        maxi = max(gen_ranks.values())
        maxi = maxi*(1.05)
        for url in self.ranks.keys():
            total[url] = (round(gen_ranks[url]*100/maxi,2), self.ranks[url][2], self.ranks[url][3])
        return total

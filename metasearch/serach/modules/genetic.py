# self.ranks[i][0] --> lin_rank
# self.ranks[i][1] --> sem_rank
# self.ranks[i][2] --> search engines

class genetic:
    def __init__(self, query, results, ranks):
        self.query = query
        self.results = results
        self.ranks = ranks

    def func(self, x, y):
        sums = []
        for url in self.ranks.keys():
            sums.append(self.ranks[url][0]*x + self.ranks[url][1]*y)

        owa = sum(sums)
        a_owa = owa/len(sums)

        max_fit = max(sums)

        cp = 0.5*max_fit

        f = abs((a_owa-cp)/(max_fit-cp))

        return f

    def fitness(self, x, y):
        ans = self.func(x, y)

        if ans == 0:
            return 99999
        else:
            return abs(1/ans)

    def start_ranking(self):
        # generate solutions
        import random
        solutions = []
        for s in range(1000):
            solutions.append((random.uniform(0, 10000),
                              random.uniform(0, 10000)))

        for i in range(10000):
            rankedsolutions = []
            for s in solutions:
                rankedsolutions.append((self.fitness(s[0], s[1]), s))
            rankedsolutions.sort()
            rankedsolutions.reverse()

            print(f"=== Gen {i} best solutions ===")
            print(rankedsolutions[0])

            bestsolutions = rankedsolutions[:100]

            if rankedsolutions[0][0] > 999999 and i<400:
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
        for url in self.ranks.keys():
            total[url] = (self.ranks[url][0]*x +
                          self.ranks[url][1]*y, self.ranks[url][2], self.ranks[url][3])

        return total

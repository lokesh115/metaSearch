from nltk.corpus import wordnet
from bs4 import BeautifulSoup
from collections import Counter


class Semantic_search:
    def clean_wordlist(self, wordlist):
        clean_list = []
        for word in wordlist:
            symbols = '!@#$%^&*()_-+={[}]|\;:\"<>?/., 1234567890'
            for i in range(len(symbols)):
                word = word.replace(symbols[i], '')
            if len(word) > 0:
                clean_list.append(word)
        return clean_list

    def semantic_search(self, query, words):
        try:
            source_word = (wordnet.synset(query+".n.1"))
        except:
            try:
                source_word = (wordnet.synset(query+".v.1"))
            except:
                return (0,0)
        score = 0
        similar_words = 0
        for word in words:
            try:
                comparer = wordnet.synset(word+".n.1")
                similar_score = source_word.wup_similarity(comparer)
                if similar_score > 0:
                    score += similar_score
                    similar_words += 1
            except:
                pass
        return (score, similar_words)

    def start_semantic(self, query, ranks):
        from bs4 import BeautifulSoup
        from urllib.request import Request, urlopen
        for url in ranks.keys():
            try:
                userAgent = (
                    'Mozilla/5.0 (Linux; Android 12; ASUS_I005DA) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36')
                hdr = {'User-Agent': userAgent}

                req = Request(url, headers=hdr)
                source_code = urlopen(req)

                soup = BeautifulSoup(
                    source_code, from_encoding=source_code.info().get_param('charset'), features="html.parser")
                ti=str(soup.find_all('title'))
                wordlist = str(soup).split(' ')
                wordlist = self.clean_wordlist(wordlist)
                query_lst=query.split()
                score,num=0,0
                for query in query_lst:
                    temp_score, temp_num = self.semantic_search(query, wordlist)
                    score+=temp_score
                    num+=temp_num
                ranks[url] = score*100/num
                print(str(ranks[url])+" "+str(query))
            except Exception as e:
                print("Semantic search lo Exception ochindi "+str(e))
                ranks[url] = 0
        return ranks

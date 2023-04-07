from nltk.corpus import wordnet
from bs4 import BeautifulSoup
from collections import Counter

class Semantic_search:
    def clean_wordlist(self, wordlist):
        clean_list = []
        blacklist = ['[document]', 'noscript',
                     'html', 'meta', 'input', 'script','style' ]
        for word in wordlist:
            if word.parent.name not in blacklist:
                symbols = '!@#$%^&*()_-+={[}]|\;:\"<>?/., 1234567890'
                for i in range(len(symbols)):
                    word = word.replace(symbols[i], '')
                if len(word) > 0:
                    clean_list.append(word)
        return clean_list

    def semantic_search(self, query, words, word_s,url):
        print("RAnking starts")
        score = 0
        similar_words = 0
        #print(query)
        try:
            source_word = (wordnet.synset(query+".n.1"))
        except:
            try:
                source_word = (wordnet.synset(query+".v.1"))
            except:
                similar_score = 0
                similar_words = word_s.count(query) + url.count(query)
                score = similar_words/2
                return (score, similar_words)
        for word in words:
            try:
                comparer = wordnet.synset(word+".n.1")
                similar_score = source_word.wup_similarity(comparer)
                if similar_score > 0:
                    score += similar_score
                    similar_words += 1
            except:
                pass
        if score == 0:
            score = 1
        print("RAnking ends")
        return (score, similar_words)
    
    
    def start_semantic(self, query, ranks):
        print(f"Ranks : {ranks}")
        from bs4 import BeautifulSoup
        from urllib.request import Request, urlopen
        import func_timeout

        titles_d = dict()
        userAgent = (
                    'Mozilla/5.0 (Linux; Android 12; ASUS_I005DA) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36')
        def souping(hdr,url):
            #hdr,url = args[0],args[1]
            from bs4 import BeautifulSoup
            from urllib.request import Request, urlopen
            req = Request(url, headers=hdr)
            source_code = urlopen(req)
            soup = BeautifulSoup(
                    source_code, from_encoding=source_code.info().get_param('charset'), features="html.parser")
            return soup
        for url in ranks.keys():
            try:
                hdr = {'User-Agent': userAgent}
                try:
                    print("Before souping")
                    soup = func_timeout.func_timeout(3,souping,args=[hdr,url])
                    print("After souping")
                except:
                    #print("Before ranking")
                    ranks[url][0] = 0
                    titles_d[url] = query
                    continue
                wordlist = soup.find_all(text=True)
                wordlist = self.clean_wordlist(wordlist)
                word_s =  ' '.join((str(n) for n in wordlist))
                query_lst = query.split()
                score, num = 0, 0
                for i in range(len(query_lst)):
                    temp_score, temp_num = self.semantic_search(
                        query_lst[i], wordlist,word_s,url)
                    score += temp_score
                    num += temp_num
                if num == 0:
                    num = 100
                ranks[url][0] = score*100/num
                print(str(ranks[url])+" "+str(query))
                #print("After ranking")
                #print("Titles before")
                # titles fetching
                c=0
                ti=""
                for title in soup.find_all('title'):
                    if c == 3:
                        break
                    ti = ti + title.get_text()
                    c += 1
                print(ti)
                unaccept = ["403 forbidden", "access denied"]
                if ti[:13].lower() in unaccept:
                    ti = self.query.capitalize()
                ti.replace("-","")
                titles_d[url] = ti
                #print("Titles after")
            except Exception as e:
                #print("Semantic search lo Exception ochindi "+str(e))
                titles_d[url] = query.capitalize()
                #print(str(ranks[url])+" "+str(query))
        return ranks, titles_d

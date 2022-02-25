import itertools
import math
import re
from collections import OrderedDict
import requests
from boilerpy3 import extractors
from bs4 import BeautifulSoup
import trafilatura
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#nltk.download('stopwords')
#nltk.download('omw-1.4')

# https://hal.archives-ouvertes.fr/hal-02768510v3/document 
# Pour choisir l'outil d'extraction de texte trafilatura selon les performances

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36'
}

#   Returns the text from a HTML file
#   With boilerpy3 library
def parse_html(url,name):
    # Text extraction with boilerpy3
    # DefaultExtractor generic extraction with simpler/no heuristic
    extractor = extractors.DefaultExtractor()

    resp = requests.get(url, headers=headers)

    if resp.ok:
        doc = extractor.get_content(resp.text)
        new = open("%s.txt"%name,"w",encoding="utf-8")
        new.write(str(doc))   #content for each file.
        new.close()
    else:
        raise Exception(f'Failed to get URL: {resp.status_code}')
   

#   Returns the text from a HTML file based on specified tags
#   BeautifulSoup
def parse_html2(url,name):

    resp = requests.get(url, headers=headers)

    if resp.ok:
        soup = BeautifulSoup(resp.text, 'html.parser')
        new = open("%s.txt"%name,"w",encoding="utf-8")

        TAGS = ['p']
        doc = ' '.join([tag.text.strip() for tag in soup.findAll(TAGS)])
        new.write(str(doc))   #content for each file.
        new.close()
    else:
        raise Exception(f'Failed to get URL: {resp.status_code}')


# Returns the text from a HTML file 
def parse_html3(url,name):
    # Text extraction with tarifilatura
    # DefaultExtractor generic extraction with simpler/no heuristic
    extractor = extractors.DefaultExtractor()

    resp = requests.get(url, headers=headers)

    if resp.ok:
        doc = trafilatura.extract(resp.text)
        new = open("%s.txt"%name,"w",encoding="utf-8")
        new.write(str(doc))   #content for each file.
        new.close()
    else:
        raise Exception(f'Failed to get URL: {resp.status_code}')


def lemmatization(tokens):
    lemmatizer = WordNetLemmatizer()
    for word in tokens:
        word = lemmatizer.lemmatize(word)
    return tokens

def tokenizeAndFilter(filename):
    stop_words = set(stopwords.words('english'))
    filex = open("%s.txt"%filename, 'r',encoding="utf8")
    text = filex.read()
    tokens = nltk.word_tokenize(text)
    tokens = [item for item in tokens if (item.isalpha() or item.isdigit()) and not item in stop_words]
    tokens = [token.lower() for token in tokens]
    return lemmatization(tokens)

terms_in_doc = []
def document_term_matrix(doc):
    dtm = []
    for i in range(0,len(doc)):
        dt = pd.DataFrame(doc[i])
        dt.columns=['terms']
        terms_in_doc.append(len(dt['terms']))
        dt = dict(dt['terms'].value_counts())
        dtm.append(dt)
    from collections import defaultdict
    
    terms = defaultdict(list)
    index = defaultdict(list)
    for i in range(0,len(dtm)):
        for key, value in dtm[i].items():
            index[key].append(i)
            terms[key].append(value)
    return index,terms

def search_binary(input,index,dtm):

    #operators = ['AND','NOT','OR']
    tk_and = input.split(" AND ")
    tk_and = [re.sub("[^a-zA-Z0-9]", " ", elem) for elem in tk_and]
    tk_or = []
    for token in tk_and:
        if (token.find("OR") != -1):
            tk_or = (token.split("OR"))
            tk_and.remove(token)
    
    tk_or = [re.sub("[^a-zA-Z0-9]", " ", elem) for elem in tk_or]
    tk_and = lemmatization(tk_and)
    
    #Si not et and dans la requête
    if(len(tk_and)>2):
        #Cas particulier
        tab_not = []
        tab_scores = []
        tab_indexes = []
        for token in tk_and:
            if (token.find("NOT") != -1):
                tk_not = token.split() 
                tab_index = index.get(tk_not[1])
                tab_not.append(tab_index)
            else:
                token = token.strip()
                token.lower()
                tab_score = TF_IDF_score(token,dtm)
                tab_index = index.get(token)
                tab_score, tab_index = (list(t) for t in zip(*sorted(zip(tab_score, tab_index),reverse = True)))
                tab_indexes.append(tab_index)
                tab_scores.append(tab_score)
        tab_not = list(set(itertools.chain(*tab_not)))
        for tab in tab_indexes:
            for no in tab_not:
                if no in tab:
                    tab.remove(no)
        return
            

    #Si au moins 2 tokens pour faire l'opération and
    if(len(tk_and)>1):
        tab_scores = []
        tab_indexes = []
        for token in tk_and:
            token = token.strip()
            token.lower()
            tab_score = TF_IDF_score(token,dtm)
            tab_index = index.get(token)
            
            if(tab_index != None):
                tab_score, tab_index = (list(t) for t in zip(*sorted(zip(tab_score, tab_index),reverse = True)))
                tab_scores.append(tab_score)
                tab_indexes.append(tab_index)
                print(token,tab_score,tab_index)
                if(len(tab_scores)>1):
                    for i in range(0,len(tab_indexes[0])):
                        for j in range(0,len(tab_indexes[1])):
                            if tab_indexes[0][i] == tab_indexes[1][j]:
                                tab_scores[0][i] = tab_scores[0][i] + tab_scores[1][j]
                    quit
        res_index = tab_indexes[0]
        res_score = tab_scores[0]
        res_score, res_index = (list(t) for t in zip(*sorted(zip(res_score, res_index),reverse = True)))



    results_or = []
    #Si au moins 2 tokens pour faire l'opération or
    if(len(tk_or)>1):
        for token in tk_or:
            token = token.strip()
            token.lower()
            tab_score = TF_IDF_score(token,dtm)
            tab_index = index.get(token)
            if(tab_index != None):
                tab_score, tab_index = (list(t) for t in zip(*sorted(zip(tab_score, tab_index),reverse = True)))
                print(token,tab_score,tab_index)
                results_or.append(tab_index)
                if(len(results_or)>1):
                    results_or = list(OrderedDict.fromkeys(results_or[0]+results_or[1]))
    
    if(len(tk_and)>1 and len(tk_or)>1):
        tab_result = [x for x in res_index if x in results_or]
        print("res",tab_result)
    elif(len(tk_or)>1):
        print("res",results_or)
    else:
        print("res",res_index)

        
def TF_IDF_score(word,dtm):
    print(word)
    tab_TF = TF_score(word,dtm)
    if (tab_TF != None):
        idf_score = IDF_score(word,dtm)
        for i in range(0,len(tab_TF)):
            tab_TF[i] = tab_TF[i] * idf_score
        return TF_score(word,dtm)


def TF_score(word,dtm):
    #print(dtm)
    tab_TF = []
    try:
        tab = dtm.get(str(word))
        if(tab != None):
            for i in range(0,len(tab)):
                tab_TF.append(tab[i]/terms_in_doc[i])
            return tab_TF
    except KeyError:
        print("err")
        pass


def IDF_score(word,dtm):
    #print(dtm)
    tab_TF = []
    try:
        tab = dtm.get(str(word))
        if(tab != None):
            return math.log(len(terms_in_doc)/(len(tab)))
    except KeyError:
        print("err")
        pass

def main():

    # Crawler les pages pour récupérer les données essentiel avec le module trafilatura
    URL = ['https://www.nature.com/articles/d41586-020-00502-w','https://www.nejm.org/doi/full/10.1056/NEJMoa2033700?query-featured_coronavirus=','https://www.nejm.org/doi/full/10.1056/NEJMoa2030340?query=featured_coronavirus'
    ,'https://www.nejm.org/doi/full/10.1056/NEJMoa2035002?query-featured_coronavirus=','https://www.nejm.org/doi/full/10.1056/NEJMoa2035002?query-featured_coronavirus=','https://www.nejm.org/doi/full/10.1056/NEJMoa2029849?query=featured_coronavirus','https://www.nejm.org/doi/full/10.1056/NEJMpv2035416?query=featured_coronavirus','https://www.thelancet.com/journals/lanrhe/article/PIIS2665-9913(21)00007-2/fulltext','https://www.thelancet.com/journals/lanres/article/PIIS2213-2600(21)00025-4/fulltext','https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)32656-8/fulltext','https://science.sciencemag.org/content/early/2021/01/11/science.abe6522']
    #for i in range(0,len(URL)):
    #    parse_html3(URL[i],i)

    # Pré-traitement des données et construction de la matrice d’incidence
    corpus = []
    for i in range(0,len(URL)):
        doc = tokenizeAndFilter(i)
        corpus.append(doc)
    
    index,dtm = document_term_matrix(corpus)
    print(terms_in_doc)
    search_binary("disease AND severe",index,dtm)
    search_binary("antibody AND plasma AND (cells OR receptors)",index,dtm)
    search_binary("NOT plasma AND infection AND NOT restrictions ",index,dtm)
    search_binary("(older adults AND antibodies) AND (genomes OR variant)",index,dtm)



if __name__ == "__main__":
    main()
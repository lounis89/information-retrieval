import os
import re
import requests
from boilerpy3 import extractors
from bs4 import BeautifulSoup
import trafilatura
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')

# https://hal.archives-ouvertes.fr/hal-02768510v3/document 
# Pour choisir l'outil d'extraction de texte trafilatura

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

def tokenizeAndFilter(filename):
    stop_words = set(stopwords.words('english'))
    filex = open("%s.txt"%filename, 'r',encoding="utf8")
    text = filex.read()
    tokens = nltk.word_tokenize(text)
    tokens = [item for item in tokens if (item.isalpha() or item.isdigit()) and not item in stop_words]
    return tokens


def main():

    # Crawler les pages pour récupérer les données essentiel avec le module boilerpy
    URL = ['https://www.nature.com/articles/d41586-020-00502-w','https://www.nejm.org/doi/full/10.1056/NEJMoa2033700?query-featured_coronavirus=','https://www.nejm.org/doi/full/10.1056/NEJMoa2030340?query=featured_coronavirus'
    ,'https://www.nejm.org/doi/full/10.1056/NEJMoa2035002?query-featured_coronavirus=','https://www.nejm.org/doi/full/10.1056/NEJMoa2035002?query-featured_coronavirus=','https://www.nejm.org/doi/full/10.1056/NEJMoa2029849?query=featured_coronavirus','https://www.nejm.org/doi/full/10.1056/NEJMpv2035416?query=featured_coronavirus','https://www.thelancet.com/journals/lanrhe/article/PIIS2665-9913(21)00007-2/fulltext','https://www.thelancet.com/journals/lanres/article/PIIS2213-2600(21)00025-4/fulltext','https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)32656-8/fulltext','https://science.sciencemag.org/content/early/2021/01/11/science.abe6522']
    #for i in range(0,len(URL)):
    #    parse_html3(URL[i],i)

    # Pré-traitement des données et construction de la matrice d’incidence
    print(tokenizeAndFilter(8))

if __name__ == "__main__":
    main()
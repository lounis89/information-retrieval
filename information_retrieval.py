import os
import re
import requests
from boilerpy3 import extractors

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36'
}

# Condenses all repeating newline characters into one single newline character
def condense_newline(text):
    return '\n'.join([p for p in re.split('\n|\r', text) if len(p) > 0])

# Returns the text from a HTML file
def parse_html(url,name):
    # Text extraction with boilerpy3
    # DefaultExtractor generic extraction with simpler/no heuristic
    extractor = extractors.ArticleExtractor()

    resp = requests.get(url, headers=headers)
    
    if resp.ok:
        doc = extractor.get_content(resp.text)
        new = open("%s.txt"%name,"w",encoding="utf-8")
        new.write(str(doc))   #content for each file.
        new.close()
    else:
        raise Exception(f'Failed to get URL: {resp.status_code}')
   

def main():

    #Crawler les pages pour récupérer nos données
    URL = ['https://www.nature.com/articles/d41586-020-00502-w','https://www.nejm.org/doi/full/10.1056/NEJMoa2033700?query-featured_coronavirus=','https://www.nejm.org/doi/full/10.1056/NEJMoa2033700?query-featured_coronavirus='
    ,'https://www.nejm.org/doi/full/10.1056/NEJMoa2035002?query-featured_coronavirus=']
    for i in range(0,len(URL)):
        parse_html(URL[i],i)

if __name__ == "__main__":
    main()
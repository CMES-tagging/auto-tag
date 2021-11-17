import requests
import json
from lxml.html import fromstring

#get ticket
def gettgt():
    with open('apikey.txt') as f:
        apikey = f.readline().strip()
    uri = 'https://utslogin.nlm.nih.gov'
    auth_endpoint = "/cas/v1/api-key"
    params = {'apikey': apikey}
    h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
    r = requests.post(uri+auth_endpoint, data=params, headers=h)
    response = fromstring(r.text)
    tgt = response.xpath('//form/@action')[0]
    return tgt

def getst(tgt):
    params = {'service': 'http://umlsks.nlm.nih.gov'}
    h = {'Content-type' : 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'User-Agent' : 'python' }
    r = requests.post(tgt, data=params, headers=h)
    st = r.text
    return st

def main():
    identifier = 'D019095'
    operation = 'parents'
    # UMLS/MeSH search function
    # identifier = MeSH id
    # operation = 'atoms' | 'parents' | 'children' | 'ancestors' | 'descendants' | 'relations'
    source = 'MSH'
    uri = "https://uts-ws.nlm.nih.gov"
    content_endpoint = "/rest/content/current/source/"+source+"/"+identifier+"/"+operation
    
    # get ticket for session
    tgt = gettgt()
    pageNumber = 1
    terms = []
    
    while True:
        query = {'ticket' : getst(tgt), 'pageNumber' : pageNumber}
        r = requests.get(uri+content_endpoint,params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        pageCount=items["pageCount"]
        for result in items["result"]:
            terms.append((result["name"], result["ui"]))
        pageNumber += 1
        if pageNumber > pageCount:
            break
    print(terms)
    return terms

if __name__ == '__main__':
    main()

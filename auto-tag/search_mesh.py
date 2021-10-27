import requests
import lxml.html as lh
from lxml.html import fromstring
import json

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

def umls_search(string):
    # UMLS/MeSH search function
    # string = search words
    # searchType = words | exact | etc.
    uri = "https://uts-ws.nlm.nih.gov"
    content_endpoint = "/rest/search/current"
    tgt = gettgt()
    vocab = 'MSH'
    returnIdType = 'sourceUi'
    pageNumber = 0
    terms = []
    
    # temp
    test = 0

    for word in string.split():
        while True:

            # temp
            test += 1
            print(test)
            if test > 4:
                break

            pageNumber += 1
            ticket = getst(tgt)
            query = {'string' : word, 'ticket' : ticket, 'searchType' : 'words', 
                    'returnIdType' : returnIdType, 'pageNumber' : pageNumber, 'sabs' : vocab}
            r = requests.get(uri+content_endpoint,params=query)
            r.encoding = 'utf-8'
            items  = json.loads(r.text)
            jsonData = items["result"]
            
            for result in jsonData["results"]:
                if jsonData["results"][0]["ui"] != "NONE":
                    terms.append((result["name"],result["ui"]))

                    # temp
                    # printing all terms
                    print(result["name"],result["ui"])

            if jsonData["results"][0]["ui"] == "NONE":
                break
        
        # temp
        if test > 4:
            break

    if terms == []:
        return ''
    else:
        # only returning first term
        return terms[0]


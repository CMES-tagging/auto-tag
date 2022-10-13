import warnings
warnings.filterwarnings('ignore')

import os
import pdftotext
import re
import pandas as pd
import contractions

import spacy
import scispacy

#Core models
#import en_core_sci_sm
#import en_core_sci_md
#import en_core_sci_lg

#NER specific models
#import en_ner_craft_md
import en_ner_bc5cdr_md
#import en_ner_jnlpba_md
#import en_ner_bionlp13cg_md

#Tools for extracting & displaying data
from spacy import displacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker

import requests
import lxml.html as lh
from lxml.html import fromstring
import json

from termcolor import colored

# clear screen for Windows, Mac, Linux OS
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

# convert PDF; split into pages and lines
def pdf_to_text(filename):
    with open(filename, 'rb') as f:
        doc = [page.split('\n') for page in pdftotext.PDF(f)]
    return doc

# remove unnecessary lines
def remove_lines(doc):
  newdoc = []
  for page in doc:
    newpage = []
    for line in page:
      if line.lstrip()[:15].lower() == 'editor-in-chief':
        pass
      elif line.lstrip()[:15].lower() == 'editor in chief':
        pass
      elif line.lstrip()[:16].lower() == 'executive editor':
        pass
      elif line.lstrip()[:15].lower() == 'managing editor':
        pass
      elif line.lstrip()[:25].lower() == 'associate managing editor':
        pass
      elif line.lstrip()[:12].lower() == 'pcma editors':
        pass
      elif line.lstrip()[:16].lower() == 'associate editor':
        pass
      elif line.lstrip()[:12].lower() == 'print editor':
        pass
      elif line.lstrip()[:15].lower() == 'abstract editor':
        pass
      elif line.strip() == '':
        pass
      elif re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s20\d+.*?Volume\s+\d+.*?Issue\s+\d+', line.strip()):
        pass
      elif re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d\d\d\d\s|\sAbstract', line.strip()):
        pass
      elif re.search(r'^[0-9]+$', line.strip()):
        pass
      elif re.search(r'^\d+\s+em:rap written summary.*?www.emrap.org\s*?$', line.strip().lower()):
        pass
      elif re.search(r'emrap.org', line.strip().lower()):
        pass
      elif re.search(r'primary care medical abstracts', line.strip().lower()):
        pass
      elif re.search(r'right on prime', line.strip().lower()):
        pass
      elif line.strip().lower() == 'notes':
        pass
      else:
        newpage.append(line)
    if newpage == []:
      pass
    else:
      newdoc.append(newpage)
  return newdoc

def display(message, text):
    scroll = False
    for page in text:
        for line in page:
            print(line)
        if not scroll:
            response = input('\n'+message+'\n'+'Press the X key to stop printing; S key for continuous scrolling; any other key to continue... '+'\n')
            if response.lower() == 'x':
                break
            elif response.lower() == 's':
                scroll = True

# find max midpoint of lines
def line_midpoint(page):
    length = 0
    for line in page:
        if len(line) > length:
            length = len(line)
    return length // 2

# split lines by finding spaces near midpoint
def split_line(line, mid):
    try:
        match = re.search('\s{2}(?=\S)', line[mid-20:mid+20])
        if match:
            # return tuple with line split
            return (line[:mid-25+match.span()[0]].strip(), line[mid-25+match.span()[1]:].strip())
        else:
            # nothing in right column
            return (line.strip(), '')
    except:
        # nothing in right column
        return (line.strip(), '')

# rebuild document in continuous column
def two_cols_to_one(doc):
    newdoc = []
    for page in doc:
        leftcol = []
        rightcol = []
        # locate middle of line
        mid = line_midpoint(page)
        for line in page:
            # split line at space near midpoint
            split = split_line(line, mid)
            if split[0] != '':
                # add to left column
                leftcol.append(split[0])
            if split[1] != '':
                # add to right column
                rightcol.append(split[1])
        # concatenate columns
        newpage = leftcol + rightcol
        newdoc.append(newpage)
    return newdoc

# split document into articles
def split_articles(doc):
    split_text = []
    title_pos = []
    titles = []
    authors = []
    p1 = -1
    text = [line for page in doc for line in page]
    for i, line in enumerate(text):
        if re.search(r'(MD|DO)', line):
            p2 = i-1
            titles.append(text[i-1])
            authors.append(text[i])
            if p1 != -1:
                title_pos.append((p1,p2))
            p1 = i+1
    title_pos.append((p1,i+1))
    for pos in title_pos:
        article_text = []
        for line in text[pos[0] : pos[1]]:
            article_text.append(line)
        split_text.append(article_text)
    return titles, authors, ['\n'.join(article) for article in split_text]            

def contraction_expansion(text):
    expanded_word = []    
    for word in text.split():
        # using contractions.fix to expand
        expanded_word.append(contractions.fix(word))   
    return  ' '.join(expanded_word)

def preprocessing(filename, text):
    id = filename[:re.search('_', filename).span()[0]]
    lst = [[id, filename, article] for article in text]
    df = pd.DataFrame(lst, columns = ['id', 'filename', 'text'])
    df['text_expanded'] = df['text'].apply(contraction_expansion)
    return df

def entity_extraction(text):
    doc = nlp(text)
    return list(doc.ents)

def list_to_string(lst):
    lst = [str(term) for term in lst]
    return ' '.join(lst)

def get_umls_terms(text, tags, screen, vocab, BT, Roots, CUI):
    umls_list, tag_list  = [], []
    if tags == []:
        print(colored('NONE', 'cyan'))
    else:
        tag_string = ', '.join([tag for tag in tags if tag==tag])
        print('Existing tags:', colored(tag_string, 'cyan'))
        tag_list = tag_string.split(', ')
    umls_list.append(tag_list)
    models = ['en_ner_bc5cdr_md'] #['en_core_sci_lg','en_ner_craft_md','en_ner_bc5cdr_md','en_ner_jnlpba_md','en_ner_bionlp13cg_md']
    first = True
    for model in models:
        if screen:
            print('Suggested terms (using', model+'):')
        else:
            if first:
                print('Writing CSV.', end='')
                first = False
            else:
                print('.', end='', flush=True)
        nlp = spacy.load(model)
        nlp.add_pipe("abbreviation_detector")
        nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "mesh"})
        doc = nlp(text)
        linker = nlp.get_pipe("scispacy_linker")
        terms = []
        for ent in doc.ents:
            entity = ent.text
            label = ent.label_
            for umls_ent in ent._.kb_ents:
                if float(umls_ent[1]) == 1.0:
                    cui = umls_ent[0]
                    umls_term = linker.kb.cui_to_entity[umls_ent[0]].canonical_name
                    terms.append((cui, umls_term))
        terms = sorted(list(set(terms)))
        if terms == []:
            if screen:
                print(colored('NONE', 'cyan'))
        else:
            for term in terms:
                if screen:
                    print(colored(term[0]+' '+term[1], 'cyan'))
                    if BT:
                        parent_list, id_list = [], []
                        for term_tuple in walk_hierarchy(term[0], 'parents'):
                            parent_list.append(term_tuple[0])
                            id_list.append(term_tuple[1])
                        #parents = '; '.join(parent_list)
                        for parent in parent_list:
                          print(' '*9+'BT  '+colored(parent, 'cyan'))
                        if Roots:
                            #root_terms = '; '.join(get_roots(id_list))
                            for root in get_roots(id_list):
                                print(' '*9+'Root:  '+colored(root, 'cyan'))
        umls_list.append([term[1] for term in terms])
    return ['\n'.join(terms) for terms in umls_list]

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
    for i, word in enumerate(string.split()):
        # search first 3 terms only
        if i > 0:
            break
        while True:
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
                    print(result['name'], result['ui'])
                    break
            if jsonData["results"][0]["ui"] == "NONE":
                break
    if terms == []:
        return ''
    else:
        # only returning first term
        return terms[0]

def walk_hierarchy(identifier, operation):
    # identifier = MeSH id
    # operation = 'atoms' | 'parents' | 'children' | 'ancestors' | 'descendants' | 'relations'
    source = 'MSH'
    uri = 'https://uts-ws.nlm.nih.gov'
    content_endpoint = '/rest/content/current/source/'+source+'/'+identifier+'/'+operation
    # get ticket for session
    tgt = gettgt()
    pageNumber = 1
    terms = []
    while True:
        query = {'ticket' : getst(tgt), 'pageNumber' : pageNumber}
        r = requests.get(uri+content_endpoint,params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        pageCount=items['pageCount']
        for result in items['result']:
            terms.append((result['name'], result['ui']))
        pageNumber += 1
        if pageNumber > pageCount:
            break
    return terms

#get roots
def get_roots(identifiers):
    mesh_categories = []
    for identifier in identifiers:
        parents = walk_hierarchy(identifier, 'parents')
        for parent in parents:
            test = parent
            while True:
                try:
                    t = walk_hierarchy(test[1], 'parents')[0][1][0]
                    if t != 'D': # i.e. not a MeSH term
                        mesh_categories.append(test[0])
                        break
                    else:
                        test = walk_hierarchy(test[1], 'parents')[0]
                except:
                    break
    return list(set(mesh_categories))

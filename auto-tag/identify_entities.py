import spacy
import scispacy

#Core models
#import en_core_sci_sm
import en_core_sci_lg

#NER specific models
#import en_ner_craft_md
#import en_ner_bc5cdr_md
#import en_ner_jnlpba_md
#import en_ner_bionlp13cg_md

#Tools for extracting & displaying data
from spacy import displacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker

def entity_extraction(text):
    doc = nlp(text)
    return list(doc.ents)

def list_to_string(lst):
    lst = [str(term) for term in lst]
    return ' '.join(lst)

def  get_umls_terms(text):
    nlp = spacy.load("en_core_sci_lg")
    nlp.add_pipe("abbreviation_detector")
    nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    doc = nlp(text)
    entity = doc.ents[1]
    clear()
    print("Name:", entity)
    linker = nlp.get_pipe("scispacy_linker")
    for umls_ent in entity._.kb_ents:
        print(linker.kb.cui_to_entity[umls_ent[0]])



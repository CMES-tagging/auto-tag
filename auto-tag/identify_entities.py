import spacy
import scispacy

#Core models
import en_core_sci_sm
import en_core_sci_lg

#NER specific models
import en_ner_craft_md
import en_ner_bc5cdr_md
import en_ner_jnlpba_md
import en_ner_bionlp13cg_md

#Tools for extracting & displaying data
from spacy import displacy

nlp = spacy.load("en_core_sci_lg")

def entity_extraction(text):
    doc = nlp(text)
    return list(doc.ents)

def list_to_string(lst):
    lst = [str(term) for term in lst]
    return ' '.join(lst)


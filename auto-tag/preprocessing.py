import pandas as pd
import re
import contractions
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

def contraction_expansion(text):
    expanded_word = []    
    for word in text.split():
        # using contractions.fix to expand
        expanded_word.append(contractions.fix(word))   
    return  ' '.join(expanded_word)

# this uses the scispaCy large vocabulary to find entities in an input column and write them to an output column
# ARGUMENTS: dataframe, input column, output column
def find_entities(df, input_col, output_col):
    for i in range(0, len(df[input_col])):
        text = df[input_col][i]
        print("processing document #" + str(i))
        doc = nlp(text)
        ents = list(doc.ents) 
        df.at[i, output_col] = ents

def entity_extraction(text):
    doc = nlp(text)
    return list(doc.ents)


def preprocessing(filename, text):
    id = filename[:re.search('_', filename).span()[0]]
    lst = [[id, filename, article] for article in text]
    df = pd.DataFrame(lst, columns = ['id', 'filename', 'text'])
    df['text_expanded'] = df['text'].apply(contraction_expansion)
    # load scispacy model
    df['entities'] = df['text_expanded'].apply(entity_extraction)
    return df

import pandas as pd
import contractions
import re

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

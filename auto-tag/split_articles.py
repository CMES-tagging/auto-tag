import re

# split document into articles
def split_articles(doc):
    split_text = []
    title_pos = []
    current = 0
    text = [line for page in doc for line in page]
    for i, line in enumerate(text):
        if re.search(r'(MD|DO)', line):
            title_pos.append(i)
    for pos in title_pos:
        article_text = []
        for line in text[current : pos-1]:
            article_text.append(line)
        split_text.append(article_text)
        current = pos-1
    return split_text            


from extract_text import *
from remove_lines import *
from display_text import *
from remove_columns import *
from split_articles import *

import os
import re

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def main():

    # read PDF files
    # returns list (pages) of lists (lines)
    path = '../../pdf/'
    pdfs = os.listdir(path)
    pdfs = [path+file for file in pdfs if file[-4:] == '.pdf']
    clear()
    n = 0
    print('Processing...')
    for f in pdfs:
        if re.search('\d\d\d+_EMRAP.*?_Written_Summary.*\.pdf', f):
            n += 1
            print('File:', n, f)
            text = pdf_to_text(f)
            print('... length of text:', len(text))

            # remove extraneous lines
            # returns list (pages) of lists (lines)
            text = remove_lines(text)
            print('... length of text:', len(text))

            # merge columns
            # returns list (pages) of lists (lines)
            text = two_cols_to_one(text)
            print('... length of text:', len(text))

            # split document into articles
            # returns list of articles
            text = split_articles(text)
            print('... length of text:', len(text))


if __name__ == '__main__':
    main()


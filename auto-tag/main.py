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
    while True:
        clear()
        print('Enter the ID of a file to process, or choose from the menu below.')
        response = input('E, for EMRAP files; R, for ROP files:  ')
        if response.lower() == 'e':
            npdfs = [path+file for file in pdfs if re.search('\d\d\d+_EMRAP_.*\.pdf', file)]
        elif response.lower() == 'r':
            npdfs = [path+file for file in pdfs if re.search('\d\d\d+_ROP_.*\.pdf', file)]
        elif re.search('^\d\d+$', response.strip()):
            found = False
            for file in pdfs:
                if file[:len(response.strip())+1] == response.strip()+'_':
                    npdfs = [path+file]
                    found = True
                    break
            if not found:
                print('File not found.')
                npdfs = []
        else:
            print('Invalid input.')
            npdfs = []
        n = 0
        for f in npdfs:
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

        # exit, or continue
        print()
        response = input('Press X to exit; press any other key to clear the screen and enter another request:  ')
        if response.lower() == 'x':
            break


if __name__ == '__main__':
    main()


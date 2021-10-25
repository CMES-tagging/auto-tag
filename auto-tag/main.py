from extract_text import *
from remove_lines import *
from display_text import *
from remove_columns import *

def main():
    f = input('Enter the path and name of the PDF file to be processed:\n')
    print(f'You entered {f}')
    print('Processing...')
    text = pdf_to_text(f)
    display('Displaying results of pdf_to_text...', text)
    text = remove_lines(text)
    display('Displaying result of remove_lines...', text)
    text = two_cols_to_one(text)
    display('Displaying result of two_cols_to_one...', text)

if __name__ == '__main__':
    main()


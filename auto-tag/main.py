from extract_text import *
from remove_lines import *
from display_text import *
from remove_columns import *

# convert PDF; split into pages and lines
#def pdf_to_text(filename):
#    with open(filename, 'rb') as f:
#        doc = [page.split('\n') for page in pdftotext.PDF(f)]
#    return doc

# remove unnecessary lines
#def remove_lines(doc):
#  newdoc = []
#  for page in doc:
#    newpage = []
#    for line in page:
#      if line.lstrip()[:16].lower() == 'editor-in-chief:':
#        pass
#      elif line.lstrip()[:17].lower() == 'executive editor:':
#        pass
#      elif line.lstrip()[:17].lower() == 'associate editor:':
#        pass
#      elif line.lstrip()[:13].lower() == 'print editor:':
#        pass
#      elif line.strip() == '':
#        pass
#      elif re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s20\d+.*?Volume\s+\d+.*?Issue\s+\d+', line.strip()):
#        pass
#      elif re.search(r'^[0-9]+$', line.strip()):
#        pass
#      elif re.search(r'^\d+\s+EM:RAP Written Summary.*?www.emrap.org\s*?$', line.strip()):
#        pass
#      elif line.strip().lower() == 'notes':
#        pass
#      else:
#        newpage.append(line)
#    if newpage == []:
#      pass
#    else:
#      newdoc.append(newpage)
#  return newdoc

#def display(message, text):
#    scroll = False
#    for page in text:
#        for line in page:
#            print(line)
#        if not scroll:
#            response = input(message+'\n'+'Press the X key to stop printing; S key for continuous scrolling; any other key to continue... ')
#            if response.lower() == 'x':
#                break
#            elif response.lower() == 's':
#                scroll = True

# find max midpoint of lines
#def line_midpoint(page):
#    mid = 0
#    for line in page:
#        if len(line) > mid:
#            mid = len(line)
#    return mid//2

# split lines by finding spaces near midpoint
#def split_line(line, mid):
#  try:
#    match = re.search('\s{3}(?=\S)', line[mid-20:mid+20])
#    if match:
#      # return tuple with line split
#      return (line[:mid-25+match.span()[0]].strip(), line[mid-25+match.span()[1]:].strip())
#    else:
#      # nothing in right column
#      return (line.strip(), '')
#  except:
#    # nothing in right column
#    return (line.strip(), '')

# rebuild document in continuous column
#def two_cols_to_one(doc):
#    newdoc = []
#    for page in doc:
#        leftcol = []
#        rightcol = []
#        # locate middle of line
#        mid = line_midpoint(page)
#        for line in page:
#            # split line at space near midpoint
#            split = split_line(line, mid)
#            if split[0] != '':
#                # add to left column
#                leftcol.append(split[0])
#            if split[1] != '':
#                # add to right column
#                rightcol.append(split[1])
#        # concatenate columns
#        newpage = leftcol + rightcol
#        newdoc.append(newpage)
#    return newdoc

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


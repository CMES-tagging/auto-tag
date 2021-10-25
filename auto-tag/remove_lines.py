import re

# remove unnecessary lines
def remove_lines(doc):
  newdoc = []
  for page in doc:
    newpage = []
    for line in page:
      if line.lstrip()[:16].lower() == 'editor-in-chief:':
        pass
      elif line.lstrip()[:17].lower() == 'executive editor:':
        pass
      elif line.lstrip()[:17].lower() == 'associate editor:':
        pass
      elif line.lstrip()[:13].lower() == 'print editor:':
        pass
      elif line.strip() == '':
        pass
      elif re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s20\d+.*?Volume\s+\d+.*?Issue\s+\d+', line.strip()):
        pass
      elif re.search(r'^[0-9]+$', line.strip()):
        pass
      elif re.search(r'^\d+\s+EM:RAP Written Summary.*?www.emrap.org\s*?$', line.strip()):
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

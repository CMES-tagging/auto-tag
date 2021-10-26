import re

# find max midpoint of lines
def line_midpoint(page):
    length = 0
    for line in page:
        if len(line) > length:
            length = len(line)
    return length // 2

# split lines by finding spaces near midpoint
def split_line(line, mid):
    try:
        match = re.search('\s{3}(?=\S)', line[mid-20:mid+20])
        if match:
            # return tuple with line split
            return (line[:mid-25+match.span()[0]].strip(), line[mid-25+match.span()[1]:].strip())
        else:
            # nothing in right column
            return (line.strip(), '')
    except:
        # nothing in right column
        return (line.strip(), '')

# rebuild document in continuous column
def two_cols_to_one(doc):
    newdoc = []
    for page in doc:
        leftcol = []
        rightcol = []
        # locate middle of line
        mid = line_midpoint(page)
        for line in page:
            # split line at space near midpoint
            split = split_line(line, mid)
            if split[0] != '':
                # add to left column
                leftcol.append(split[0])
            if split[1] != '':
                # add to right column
                rightcol.append(split[1])
        # concatenate columns
        newpage = leftcol + rightcol
        newdoc.append(newpage)
    return newdoc

from auto_tag_func import *

def main():

    # read PDF files
    path = '../../pdf/'
    pdfs = os.listdir(path)

    # read CSV files
    tags1_df = pd.read_csv('../../csv/cmes_tags.csv')
    tags2_df = pd.read_csv('../../csv/additional_tags.csv')
    tags_df = pd.concat([tags1_df[['Topic_ID', 'Tag_Name']], tags2_df[['Topic_ID', 'Tag_Name']]], axis=0)
    tags_df = tags_df.drop_duplicates()
    tags_df = tags_df.groupby(['Topic_ID'])['Tag_Name'].apply(list).reset_index(name='Tag_Names')
    
    # create empty dataframe 
    columns = ['id', 'filename', 'text', 'text_expanded', 'entities', 'entities_text', 'mesh_terms']
    df = pd.DataFrame(columns = columns)

    # loop over files
    while True:

        clear()

        # menu
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
            id = int(re.match(path+'\d\d\d+_', f).group()[len(path):-1])
            n += 1
            print('\nFile:', n, f)
            print('... extracting text')
            text = pdf_to_text(f)

            # remove extraneous lines
            # returns list (pages) of lists (lines)
            print('... removing headers and footers')
            text = remove_lines(text)

            if id >= 5482:
                # merge columns
                # returns list (pages) of lists (lines)
                print('... merging columns')
                text = two_cols_to_one(text)

            # split document into articles
            if id >= 5482:
                # returns list of articles
                print('... splitting into articles')
                text = split_articles(text)
            else:
                # returns simple list (one article)
                text = [line.strip() for page in text for line in page]
                text = [' '.join(text)] 


            print('... finding MeSH terms')
            try:
                tags = tags_df.loc[tags_df['Topic_ID'] == id]['Tag_Names'].values[0]
            except:
                tags = []
            get_umls_terms(text[0],tags)

            # create DataFrame
            # preprocessing
#            filename = f[len(path):]
#            df_add = preprocessing(filename, text)

            # NER
#            print('\n... identifying entities ...')
#            df_add['entities'] = df_add['text_expanded'].apply(entity_extraction)
#            df_add['entities_text'] = df_add['entities'].apply(list_to_string)
#            print(df_add)

            # search mesh
#            print('searching mesh ...')
#            df_add['mesh_terms'] = df_add['entities_text'].apply(umls_search)

            # add new rows to dataframe
#            df = pd.concat([df, df_add], axis = 0)

        # print dataframe to console
#        print(df)

        # menu
        response = input('\nPress X to exit; press any other key to clear the screen and enter another request:  ')
        if response.lower() == 'x':
            break


if __name__ == '__main__':
    main()


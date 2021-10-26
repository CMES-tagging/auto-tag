def display(message, text):
    scroll = False
    for page in text:
        for line in page:
            print(line)
        if not scroll:
            response = input('\n'+message+'\n'+'Press the X key to stop printing; S key for continuous scrolling; any other key to continue... '+'\n')
            if response.lower() == 'x':
                break
            elif response.lower() == 's':
                scroll = True


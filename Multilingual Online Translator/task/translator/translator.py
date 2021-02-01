def main():
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English to French:')
    lang = input()
    print('Type the word you want to translate:')
    word = input()
    print('You chose "{}" as the language to translate "{}" to.'.format(lang, word))


main()

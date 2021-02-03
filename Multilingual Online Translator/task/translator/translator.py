import requests
from bs4 import BeautifulSoup


def get_translations(from_lang, to_lang, word):
    address = f'https://context.reverso.net/translation/{from_lang}-{to_lang}/{word}'
    # header added to avoid getting blocked from ReversoContext due to multiple requests
    r = requests.get(address, headers={'User-Agent': 'Mozilla/5.0'})
    status = r.status_code
    if status == 200:
        print('200 OK\n')
    print('Context examples:\n')
    soup = BeautifulSoup(r.content, 'html.parser')
    word_translations = soup.find_all('div', {'id': 'translations-content'})
    for word in word_translations:
        word = word.text.replace('\n', ' ')
        words_list = word.split()
    print('French Translations:')
    for i in range(5):
        print(words_list[i])
    original_sentences = soup.find_all('div', {'class': 'src ltr'})
    translated_sentences = soup.find_all('div', {'class': 'trg ltr'})
    original_list = [original.text.strip() for original in original_sentences]
    translated_list = [translated.text.strip() for translated in translated_sentences]
    print('\nFrench Examples:')
    for i in range(5):
        print(original_list[i])
        print(translated_list[i] + '\n')


def main():
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
    lang = input()
    print('Type the word you want to translate:')
    word = input()
    print(f'You chose "{lang}" as a language to translate "{word}".')
    if lang == 'en':
        to_lang = 'english'
        from_lang = 'french'
    else:
        to_lang = 'french'
        from_lang = 'english'
    get_translations(from_lang, to_lang, word)


main()

import requests
from bs4 import BeautifulSoup


def get_translations(from_lang, to_lang, word):
    address = 'https://context.reverso.net/translation/{}-{}/{}'.format(from_lang, to_lang, word)
    # header added to avoid getting blocked from ReversoContext due to multiple requests
    r = requests.get(address, headers={'User-Agent': 'Mozilla/5.0'})
    status = r.status_code
    if status == 200:
        print('200 OK')
    print('Translations')
    soup = BeautifulSoup(r.content, 'html.parser')
    word_translations = soup.find_all('div', {'id': 'translations-content'})
    for word in word_translations:
        word = word.text.replace('\n', ' ')
        words_list = word.split()
    print(words_list)
    original_sentences = soup.find_all('div', {'class': 'src ltr'})
    translated_sentences = soup.find_all('div', {'class': 'trg ltr'})
    sentence_list = []
    for original in original_sentences:
        for translated in translated_sentences:
            sentence_list.append(original.text.strip())
            sentence_list.append(translated.text.strip())
    print(sentence_list)


def main():
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
    lang = input()
    print('Type the word you want to translate:')
    word = input()
    print('You chose "{}" as a language to translate "{}".'.format(lang, word))
    if lang == 'en':
        to_lang = 'english'
        from_lang = 'french'
    else:
        to_lang = 'french'
        from_lang = 'english'
    get_translations(from_lang, to_lang, word)


main()

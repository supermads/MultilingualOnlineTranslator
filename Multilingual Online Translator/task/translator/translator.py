import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.from_lang = ''
        self.to_lang = ''
        self.word = ''
        self.words_list = []
        self.original_list = []
        self.translated_list = []
        self.num_outputs = 3

    def get_translations(self):
        address = f'https://context.reverso.net/translation/{self.from_lang.lower()}-{self.to_lang.lower()}/{self.word}'
        # header added to avoid getting blocked from ReversoContext due to multiple requests
        s = requests.Session()
        r = s.get(address, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, 'html.parser')

        word_translations = soup.find_all('div', {'id': 'translations-content'})
        for word in word_translations:
            word = word.text.replace('\n', ' ').strip()
            self.words_list = word.split('       ')

        original_sentences = soup.find_all('div', {'class': 'src ltr'})
        if self.to_lang == 'Hebrew':
            translated_sentences = soup.find_all('div', {'class': 'trg rtl'})
        elif self.to_lang == 'Arabic':
            translated_sentences = soup.find_all('div', {'class': 'trg rtl arabic'})
        else:
            translated_sentences = soup.find_all('div', {'class': 'trg ltr'})

        self.original_list = [original.text.strip() for original in original_sentences]
        self.translated_list = [translated.text.strip() for translated in translated_sentences]

    def process_words(self, f):
        print(f'\n{self.to_lang} Translations:')
        f.write(f'\n{self.to_lang} Translations:\n')

        count = 0
        for i in range(len(self.words_list)):
            if count < self.num_outputs:
                if self.words_list[i]:
                    print(self.words_list[i].strip())
                    f.write(self.words_list[i].strip() + '\n')
                    count += 1

    def process_sentences(self, f):
        print(f'\n{self.to_lang} Examples:')
        f.write(f'\n{self.to_lang} Examples:\n')
        for i in range(self.num_outputs):
            print(self.original_list[i])
            f.write(self.original_list[i] + '\n')
            print(self.translated_list[i] + '\n')
            f.write(self.translated_list[i] + '\n\n')

    def menu(self):
        lang_options = {
            1: 'Arabic',
            2: 'German',
            3: 'English',
            4: 'Spanish',
            5: 'French',
            6: 'Hebrew',
            7: 'Japanese',
            8: 'Dutch',
            9: 'Polish',
            10: 'Portuguese',
            11: 'Romanian',
            12: 'Russian',
            13: 'Turkish'
        }

        print('Hello, you\'re welcome to the translator. Translator supports:')
        for key, value in lang_options.items():
            print(f'{key}. {value}')

        print('Type the number of your language:')
        self.from_lang = lang_options.get(int(input()))

        print('Type the number of language you want to translate to or \'0\' to translate to all languages:')
        choice = int(input())

        print('Type the word you want to translate:')
        self.word = input().lower()

        file_name = self.word + '.txt'
        with open(file_name, 'w') as f:
            if choice == 0:
                for i in range(1, 14):
                    self.to_lang = lang_options.get(i)
                    if self.to_lang != self.from_lang:
                        self.get_translations()
                        self.process_words(f)
                        self.process_sentences(f)
            else:
                self.to_lang = lang_options.get(choice)
                self.get_translations()
                self.process_words(f)
                self.process_sentences(f)


def main():
    Translator().menu()


main()

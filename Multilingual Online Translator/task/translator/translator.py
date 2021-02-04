import requests
from bs4 import BeautifulSoup
from sys import argv


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
        s = requests.Session()
        try:
            # header added to avoid getting blocked from ReversoContext due to multiple requests
            r = s.get(address, headers={'User-Agent': 'Mozilla/5.0'})
        except:
            print('Something wrong with your internet connection')
            return False
        soup = BeautifulSoup(r.content, 'html.parser')

        word_translations = soup.find_all('div', {'id': 'translations-content'})
        for word in word_translations:
            word = word.text.replace('\n', ' ').strip()
            self.words_list = word.split('       ')

        if len(self.words_list) == 0:
            print(f'Sorry, unable to find {self.word}')
            return False

        original_sentences = soup.find_all('div', {'class': 'src ltr'})
        if self.to_lang == 'Hebrew':
            translated_sentences = soup.find_all('div', {'class': 'trg rtl'})
        elif self.to_lang == 'Arabic':
            translated_sentences = soup.find_all('div', {'class': 'trg rtl arabic'})
        else:
            translated_sentences = soup.find_all('div', {'class': 'trg ltr'})

        self.original_list = [original.text.strip() for original in original_sentences]
        self.translated_list = [translated.text.strip() for translated in translated_sentences]
        return True

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
        lang_options = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
            'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
        self.from_lang = argv[1].capitalize()
        self.to_lang = argv[2].capitalize()
        self.word = argv[3].lower()

        if self.to_lang != 'All' and self.to_lang not in lang_options:
            print(f'Sorry, the program doesn\'t support {self.to_lang}')
            return

        file_name = self.word + '.txt'
        with open(file_name, 'w') as f:
            if self.to_lang == 'All':
                for i in range(len(lang_options)):
                    self.to_lang = lang_options[i]
                    if self.to_lang != self.from_lang:
                        if self.get_translations():
                            self.process_words(f)
                            self.process_sentences(f)
            else:
                if self.get_translations():
                    self.process_words(f)
                    self.process_sentences(f)


def main():
    Translator().menu()


main()

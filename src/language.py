import json
import string
import os

import state
from translation_manager import get_translations
from lemmatization_manager import spacy_model, lemmatize
from lesson import lessons, load_lessons

class VocabTerm:
    def __init__(self, term: str, translations: list[str], is_seen: bool = False, is_known: bool = False):
        self.term = term
        self.translations = translations
        self.is_seen = is_seen
        self.is_known = is_known

    def is_valid_translation(self, translation: str) -> bool:
        """
        Returns whether a given translation is a valid translation of the vocab term
        
        :type translation: str
        :rtype: bool
        """
        return translation in self.translations

class Language:
    def __init__(self, name: str, abbreviation: str, spacy_model: str, direction: str, 
                 translations: dict[str, list[str]], vocab: list[VocabTerm]):
        self.name = name
        self.abbreviation = abbreviation
        self.spacy_model = spacy_model
        self.direction = direction
        self.translation = translations
        self.vocab = vocab

    @staticmethod
    def load(language_name: str):
        """
        Loads a language object from the languages folder with the given name
        
        :type language_name: str
        :rtype: Language
        """
        # Load all .json data from the language folder (metadata, translations, & vocab)
        with open(f"{state.LANGUAGES_FP}\\{language_name}\\metadata.json", encoding='utf8') as metadata_file:
            metadata = json.load(metadata_file)
        with open(f"{state.LANGUAGES_FP}\\{language_name}\\translations.json", encoding='utf8') as translations_file:
            translations = json.load(translations_file)
        with open(f"{state.LANGUAGES_FP}\\{language_name}\\vocab.json", encoding='utf8') as vocab_file:
            vocab_dict = json.load(vocab_file)

        # Load user data for the specified language
        with open(f"{state.BIN_FP}\\user_data.json", encoding='utf8') as user_data_file:
            user_data = json.load(user_data_file)
            seen_vocab = user_data[language_name]['seen_vocab']
            known_vocab = user_data[language_name]['known_vocab']

        # Parse vocab dict into a list of VocabTerm objects
        vocab: list[VocabTerm] = []
        for term, translations in vocab_dict.items():
            vocab.append(VocabTerm(term, translations, term in seen_vocab, term in known_vocab))

        return Language(**metadata, translations = translations, vocab = vocab)
    
def install_language(language_name: str, language_abbreviation: str, direction: str):
    """Installs a given language to the languages folder"""

    print(f"Installing language \'{language_name}\':")
    metadata = {
        'name': language_name,
        'abbreviation': language_abbreviation,
        'spacy_model': spacy_model(language_abbreviation),
        'direction': direction
    }
    translations: dict[str, list[str]] = {}
    vocab: dict[str, list[str]] = {}

    # Run through all the lessons and add translations and vocab
    print("Constructing translations & vocab...")
    for lesson in lessons:

        print(f"\t\'{lesson.title}\'...")
        for line_number, line in enumerate(lesson.lines):

            print(f"\t\tLine {line_number + 1}/{len(lesson.lines)}...")
            translations[line] = get_translations(line, 'en', language_abbreviation)
            for translation in translations[line]:

                # Remove punctuation
                stripped_translation = translation.translate(str.maketrans('', '', string.punctuation))

                # Add lemmatized terms from the translation to vocab
                for lemmatization in lemmatize(stripped_translation, spacy_model(language_abbreviation)):
                    term = lemmatization.lemma
                    vocab[term] = get_translations(term, language_abbreviation, 'en')
    
    # Write data to json files
    print("Writing data to language folder...")

    # Create the language folder directory
    try:
        os.mkdir(f"{state.LANGUAGES_FP}\\{language_name}")
    except FileExistsError:
        pass

    with open(f"{state.LANGUAGES_FP}\\{language_name}\\metadata.json", 'w', encoding='utf8') as metadata_file:
        json.dump(metadata, metadata_file, ensure_ascii=False)
    with open(f"{state.LANGUAGES_FP}\\{language_name}\\translations.json", 'w', encoding='utf8') as translations_file:
        json.dump(translations, translations_file, ensure_ascii=False)
    with open(f"{state.LANGUAGES_FP}\\{language_name}\\vocab.json", 'w', encoding='utf8') as vocab_file:
        json.dump(vocab, vocab_file, ensure_ascii=False)

    print(f"Language \'{language_name}\' installed.")

# load_lessons()
# install_language("Russian", 'ru', 'right')
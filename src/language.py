import json

import state

class VocabTerm:
    def __init__(self, term: str, translations: list[str]):
        self.term = term
        self.translations = translations

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
        with open(f"{state.LANGUAGES_FP}\\{language_name}\\metadata.json") as metadata_file:
            metadata = json.load(metadata_file)
        with open(f"{state.LANGUAGES_FP}\\{language_name}\\translations.json") as translations_file:
            translations = json.load(translations_file)
        with open(f"{state.LANGUAGES_FP}\\{language_name}\\vocab.json") as vocab_file:
            vocab_dict = json.load(vocab_file)

        # Parse vocab dict into a list of VocabTerm objects
        vocab: list[VocabTerm] = []
        for vocab_term_data in vocab_dict['vocab']:
            vocab.append(VocabTerm(**vocab_term_data))

        return Language(**metadata, translations = translations, vocab = vocab)
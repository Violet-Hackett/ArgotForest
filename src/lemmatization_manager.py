import spacy

class Lemmatization:
    def __init__(self, lemma: str, part_of_speech: str):
        self.lemma = lemma
        self.part_of_speech = part_of_speech

def lemmatize(text: str, spacy_model: str) -> list[Lemmatization]:
    """
    Takes a string of text, divides it into tokens, and returns a list of lemmatizations of those tokens using
    the given spacy model.
    
    :param text: Text to lemmatize
    :type text: str
    :return: Description
    :rtype: list[Lemmatization]
    """
    # Load spacy model
    spacy_language_model = spacy.load(spacy_model)

    # Parse tokens
    tokens = spacy_language_model(text)

    return [Lemmatization(token.lemma_, token.pos_) for token in tokens]

INSTALLED_SPACY_MODELS: list[str] = [
    "ca_core_news_sm",
    "da_core_news_sm",
    "de_core_news_sm",
    "el_core_news_sm",
    "en_core_web_sm",
    "es_core_news_sm",
    "fi_core_news_sm",
    "fr_core_news_sm",
    "hr_core_news_sm",
    "it_core_news_sm",
    "ja_core_news_sm",
    "lt_core_news_sm",
    "nb_core_news_sm",
    "nl_core_news_sm",
    "pl_core_news_sm",
    "pt_core_news_sm",
    "ro_core_news_sm",
    "ru_core_news_sm",
    "sl_core_news_sm",
    "sv_core_news_sm",
    "uk_core_news_sm",
    "xx_ent_wiki_sm",
    "xx_sent_ud_sm",
    "zh_core_web_sm"
]

def spacy_model(language_abbreviation: str) -> str:
    """
    Returns the spacy model name for the given language abbreviation
    
    :type language_abbreviation: str
    :rtype: str
    """
    for model in INSTALLED_SPACY_MODELS:
        if model[:2] == language_abbreviation:
            return model
    raise IndexError(f"No spacy model for language \'{language_abbreviation}\' is installed.")
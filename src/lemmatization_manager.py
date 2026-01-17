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
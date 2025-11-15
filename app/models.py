import spacy
from sentence_transformers import SentenceTransformer

class NLPModels:
    def __init__(self):
        # Load MiniLM model
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Load spaCy NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model not installed. Run: python -m spacy download en_core_web_sm"
            )

import re

def classify_question_type(question: str) -> str:
    q = question.lower()

    if "how many" in q:
        return "count"
    if "favorite" in q and "restaurant" in q:
        return "favorite_restaurants"
    if "when" in q or "date" in q or "plan" in q:
        return "date"
    return "generic"


def extract_target_person(question: str, nlp):
    """
    Extract PERSON name from question using spaCy NER.
    Returns the full name (e.g., 'Lorenzo Cavalli') or None.
    """
    doc = nlp(question)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    if persons:
        return persons[0].strip()

    m = re.search(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b", question)
    return m.group(1).strip() if m else None

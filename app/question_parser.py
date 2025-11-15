# app/question_parser.py

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
    doc = nlp(question)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return persons[0] if persons else None

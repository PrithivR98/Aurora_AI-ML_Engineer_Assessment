# app/rule_engine.py

import re

def extract_date(text, nlp):
    doc = nlp(text)
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    if dates:
        return dates[0]

    # regex fallback
    match = re.search(
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b",
        text,
    )
    return match.group(0) if match else None


def extract_count(text, nlp):
    doc = nlp(text)
    nums = [ent.text for ent in doc.ents if ent.label_ == "CARDINAL"]
    if nums:
        return nums[0]

    match = re.search(r"\b\d+\b", text)
    return match.group(0) if match else None


def extract_item_from_question(question):
    q = question.lower()
    m = re.search(r"how many (.+?) (does|do|has|have)\b", q)
    return m.group(1).strip() if m else None


def extract_restaurants(text):
    m = re.search(r"favorite restaurants?\s+(?:are|is)\s+(.*)", text, re.IGNORECASE)
    if not m:
        return []

    rest_str = m.group(1).split(".")[0]
    parts = re.split(r",| and ", rest_str)
    return [p.strip() for p in parts if p.strip()]

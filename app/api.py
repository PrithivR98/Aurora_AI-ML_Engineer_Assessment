from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.models import NLPModels
from app.data_loader import fetch_messages
from app.utils import semantic_search
from app.question_parser import classify_question_type, extract_target_person
from app.rule_engine import (
    extract_date, extract_count, extract_item_from_question, extract_restaurants
)

router = APIRouter()
models = NLPModels()

class AskResponse(BaseModel):
    answer: str

@router.get("/ask", response_model=AskResponse)
async def ask(question: str = Query(...)):
    # Fetch all messages once
    all_messages = await fetch_messages()

    # ---- NEW: Extract PERSON ----
    target_person = extract_target_person(question, models.nlp)

    # ---- NEW: Filter messages for that user ----
    if target_person:
        messages = [m for m in all_messages if m.get("user_name") == target_person]

        # If no messages for that user → fallback
        if not messages:
            messages = all_messages
    else:
        messages = all_messages

    # ---- Continue with semantic search only within filtered subset ----
    q_type = classify_question_type(question)
    ranked = semantic_search(question, messages, models.embedder, top_k=5)

    # ---- Extract answer as before ----
    for msg in ranked:
        text = msg["message"]

        if q_type == "date":
            date = extract_date(text, models.nlp)
            if date:
                name = target_person or msg["user_name"]
                return AskResponse(answer=f"{name} is planning their trip on {date}.")

        if q_type == "count":
            count = extract_count(text, models.nlp)
            if count:
                item = extract_item_from_question(question) or "items"
                name = target_person or msg["user_name"]
                return AskResponse(answer=f"{name} has {count} {item}.")

        if q_type == "favorite_restaurants":
            rests = extract_restaurants(text)
            if rests:
                name = target_person or msg["user_name"]
                rest_list = ", ".join(rests)
                return AskResponse(answer=f"{name}'s favorite restaurants are {rest_list}.")

    # fallback: return best matched message
    return AskResponse(answer=ranked[0]["message"])

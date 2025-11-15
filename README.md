BONUS 1 — Design Notes (Alternative Approaches)

Several architectural options were evaluated during development:

1. Pure Rule-Based System (Rejected)

Simple but brittle

Cannot understand paraphrases

Large variety of message types makes rule maintenance difficult

2. spaCy-Only NLP Pipeline (Rejected)

NER is strong

But no semantic relevance scoring

Hard to identify which message answers the question

3. Embedding-Only Retrieval (Rejected)

Great at semantic similarity

But cannot extract structured data (dates/counts)

4. LLM-Based QA System (Rejected)

High accuracy but:

Expensive

Slower

Risk of hallucinations

Unnecessary for this narrow task

Final Architecture Chosen: Hybrid System

✔ SentenceTransformer MiniLM → semantic retrieval
✔ spaCy NER → extract structured entities
✔ Regex + rule engine → deterministic extraction
✔ FastAPI → simple API endpoint
✔ Cloud Run → scalable & serverless

This hybrid approach balances accuracy, simplicity, speed, and explainability.

BONUS 2 — Data Insights & Anomalies

Analysis of ~3349 messages revealed several noteworthy patterns:

1. Inconsistent User IDs / Multiple IDs per Name

Some users have repeated names but varying IDs (e.g., “Armand Dupont”).
→ Likely CRM duplication or synthetic generation.

2. Timestamps Out of Order

Dataset mixes messages from 2024 and 2025 in inconsistent order.
→ Requires sorting before time-based logic.

3. Template-Style Repetition

Message patterns repeat with small variations:
restaurant bookings, flight seat preferences, billing issues, etc.
→ Indicates synthetic or semi-synthetic data.

4. Inconsistent Phone Number Formats

Formats vary:
555-349-7841, 212-555-6051, 001-235-789, etc.
→ Extraction requires flexible regex.

5. PII Appears in Free Text

Users share:

phone numbers

addresses

loyalty numbers

credit card endings

→ Needs masking in production.

6. Mixed Intent Types

Messages include:

travel requests

billing concerns

preferences

personal information

confirmations
→ Reinforces need for semantic search before extraction.

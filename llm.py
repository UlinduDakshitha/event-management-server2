import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a professional B2B event communications specialist.

STRICT RULES:
1. Use ONLY the exact session details provided below.
2. FORBIDDEN from inventing any topic, speaker, time, or event detail.
3. Event name: "Troubled Waters: Sailing with AI in Supply Chain" by Accelalpha and Oracle.
4. Professional, warm, 3-5 paragraphs max.
5. End with a call-to-action to attend.
6. Sign off as: The AccelAlpha Events Team"""


async def draft_invitation_email(visitor_name: str, visitor_focus: str, session: dict) -> str:
    prompt = f"""VISITOR NAME: {visitor_name}
VISITOR FOCUS: {visitor_focus}

SESSION DETAILS (use ONLY these):
Title: {session["title"]}
Time: {session["time"]}
Speaker: {session["speaker"]}
Description: {session["description"]}

Write the complete invitation email now."""

    response = client.chat.completions.create(
   model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
    )
    
    return response.choices[0].message.content
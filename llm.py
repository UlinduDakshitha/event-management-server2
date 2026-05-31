"""
llm.py
------
Drafts a professional B2B invitation email using Claude API.
Strict prompt rules prevent hallucination of fake topics, times, or speakers.
"""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a professional B2B event communications specialist.
Your ONLY job is to write a personalized invitation email for a specific conference session.

STRICT RULES YOU MUST FOLLOW WITHOUT EXCEPTION:
1. You MUST ONLY use the exact session details provided to you — title, time, speaker name, and description as given.
2. You are ABSOLUTELY FORBIDDEN from inventing, altering, or extrapolating any session topic, speaker name, time slot, or event detail not explicitly given.
3. Do NOT mention any sessions, speakers, or topics that are not in the provided session data.
4. Do NOT use placeholder text like [Company Name] or [Date] — write a complete, ready-to-send email.
5. The event name is: "Troubled Waters: Sailing with AI in Supply Chain" by Accelalpha & Oracle.
6. The email must be professional, warm, and concise — 3 to 5 short paragraphs maximum.
7. End the email with a clear call-to-action to register or attend.
8. Sign off as: The AccelAlpha Events Team
"""

async def draft_invitation_email(visitor_name: str, visitor_focus: str, session: dict) -> str:
    """Generate a personalized B2B invitation email for the matched session."""

    user_prompt = f"""Write a personalized conference invitation email for the following visitor.

VISITOR DETAILS:
- Name: {visitor_name}
- Professional Focus / Challenges: {visitor_focus}

MATCHED SESSION (use ONLY these exact details — do not change anything):
- Session Title: {session['title']}
- Time: {session['time']}
- Speaker: {session['speaker']}
- Description: {session['description']}

Write the complete invitation email now, connecting the visitor's stated challenges to this exact session."""

    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return message.content[0].text

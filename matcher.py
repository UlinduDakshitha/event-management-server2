"""
matcher.py
----------
Reads agenda.txt and finds the best-matching session for a visitor's
professional focus using keyword overlap scoring (no external ML needed).
"""

import re
import os
from pathlib import Path

AGENDA_PATH = Path(__file__).parent / "agenda.txt"

def parse_agenda(path: Path) -> list[dict]:
    """Parse agenda.txt into a list of session dicts."""
    text = path.read_text(encoding="utf-8")
    sessions = []

    # Split by [SESSION_N] blocks
    blocks = re.split(r"\[SESSION_\d+\]", text)
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        session = {}

        time_match = re.search(r"Time:\s*(.+)", block)
        title_match = re.search(r"Title:\s*(.+)", block)
        speaker_match = re.search(r"Speaker:\s*(.+)", block)
        keywords_match = re.search(r"Focus Keywords:\s*(.+)", block)
        desc_match = re.search(r"Description:\s*([\s\S]+)", block)

        if not (time_match and title_match and speaker_match):
            continue

        session["time"] = time_match.group(1).strip()
        session["title"] = title_match.group(1).strip()
        session["speaker"] = speaker_match.group(1).strip()
        session["keywords"] = keywords_match.group(1).strip() if keywords_match else ""
        session["description"] = desc_match.group(1).strip() if desc_match else ""

        # Skip purely logistical sessions (coffee, lunch, registration)
        skip_titles = ["registrations", "coffee break", "lunch", "networking"]
        if any(s in session["title"].lower() for s in skip_titles):
            continue

        sessions.append(session)

    return sessions


def score_session(session: dict, query: str) -> float:
    """Score a session against the visitor's query using keyword overlap."""
    query_words = set(re.findall(r"\b\w+\b", query.lower()))

    # Build searchable text from session fields with weights
    session_text = (
        session["keywords"].lower() + " " +
        session["keywords"].lower() + " " +   # double weight for keywords
        session["title"].lower() + " " +
        session["description"].lower()
    )
    session_words = set(re.findall(r"\b\w+\b", session_text))

    # Remove common stop words
    stop_words = {"the", "a", "an", "and", "or", "in", "on", "at", "to", "for",
                  "of", "with", "is", "are", "how", "we", "our", "my", "i", "it"}
    query_words -= stop_words

    if not query_words:
        return 0.0

    overlap = query_words & session_words
    score = len(overlap) / len(query_words)
    return score


def find_best_session(visitor_focus: str) -> dict | None:
    """Return the single best-matching session for the visitor's focus."""
    sessions = parse_agenda(AGENDA_PATH)
    if not sessions:
        return None

    scored = [(score_session(s, visitor_focus), s) for s in sessions]
    scored.sort(key=lambda x: x[0], reverse=True)

    best_score, best_session = scored[0]

    # If nothing matches at all, return the most relevant general session
    if best_score == 0:
        # Return the industry keynote as a sensible default
        for s in sessions:
            if "keynote" in s["title"].lower():
                return s
        return sessions[0]

    return best_session

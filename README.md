# Accelalpha Oracle — Backend

FastAPI backend for AI-powered session matching and invitation drafting.

## Tech Stack
- Python 3.12
- FastAPI
- Groq API (llama-3.3-70b-versatile)

## Local Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Set GROQ_API_KEY=gsk_...
python -m uvicorn main:app --reload --port 8000
```

API runs at: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

## Live URL
`https://your-api.onrender.com` *(update after deploy)*

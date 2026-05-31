from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from matcher import find_best_session
from llm import draft_invitation_email
from mcp import send_draft_via_mcp

app = FastAPI(title="AccelAlpha Oracle Event API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, restrict to your Vercel domain
    allow_methods=["*"],
    allow_headers=["*"],
)

class VisitorRequest(BaseModel):
    name: str
    email: str
    focus: str  # Professional Focus / Career Challenges

class InvitationResponse(BaseModel):
    matched_session_title: str
    matched_session_time: str
    matched_speaker: str
    email_body: str

@app.get("/")
def root():
    return {"status": "AccelAlpha Oracle Backend is live ✅"}

@app.post("/match-session", response_model=InvitationResponse)
async def match_session(visitor: VisitorRequest):
    # Step 1: Match session from agenda.txt
    session = find_best_session(visitor.focus)
    if not session:
        raise HTTPException(status_code=404, detail="No matching session found.")

    # Step 2: Draft personalized invitation via LLM
    email_body = await draft_invitation_email(
        visitor_name=visitor.name,
        visitor_focus=visitor.focus,
        session=session
    )

    # Step 3: MCP Simulation — log the action
    send_draft_via_mcp(visitor.email, email_body)

    return InvitationResponse(
        matched_session_title=session["title"],
        matched_session_time=session["time"],
        matched_speaker=session["speaker"],
        email_body=email_body
    )

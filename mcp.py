"""
mcp.py
------
MCP Simulation: send_draft_via_mcp()
Logs the email recipient, body, and UTC timestamp to server logs.
In a real integration, this would trigger an actual email send via an MCP server.
"""

import logging
from datetime import datetime, timezone

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [MCP] %(levelname)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ"
)
logger = logging.getLogger("mcp_trigger")


def send_draft_via_mcp(email_address: str, email_body: str) -> None:
    """
    MCP Simulation trigger.
    Prints recipient email, email body, and UTC timestamp to server logs.
    
    In production, this function would call an MCP server endpoint
    (e.g., Gmail MCP, SendGrid MCP) to dispatch the drafted email.
    """
    utc_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    logger.info("=" * 60)
    logger.info("MCP TRIGGER FIRED")
    logger.info(f"TIMESTAMP (UTC): {utc_timestamp}")
    logger.info(f"RECIPIENT: {email_address}")
    logger.info("EMAIL BODY:")
    logger.info("-" * 40)
    for line in email_body.split("\n"):
        logger.info(line)
    logger.info("=" * 60)

    # Also print to stdout for Render/HuggingFace log visibility
    print("\n" + "="*60)
    print("[MCP TRIGGER] Draft email dispatched")
    print(f"  Recipient : {email_address}")
    print(f"  Timestamp : {utc_timestamp}")
    print(f"  Body Preview: {email_body[:120].strip()}...")
    print("="*60 + "\n")

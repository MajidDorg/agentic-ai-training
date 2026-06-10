"""
LEVEL-UP (optional / advanced): the Inbox Agent on your REAL Gmail.

This is the same agent as project/inbox_agent.py, but the read tool reads your
actual Gmail, and "send" creates a real DRAFT in your Gmail Drafts folder
(safe: it does NOT auto-send to real people — you review and hit send yourself).

⚠️  This requires extra setup that the main class does NOT need:
    - a Google Cloud project + Gmail API + OAuth credentials  (see connect-your-gmail.md)
    - extra Python packages:
        uv add google-api-python-client google-auth-oauthlib google-auth-httplib2

Do NOT attempt this during the class unless you've finished the main project.
Full step-by-step instructions are in connect-your-gmail.md.

Run from the project root with:   uv run level-up/gmail_inbox_agent.py
"""

import base64
import json
import sys
from email.mime.text import MIMEText
from pathlib import Path

# Windows terminals default to a non-UTF-8 codepage that can't print emoji.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool, trace

# These imports only work after you run the `uv add ...` line above.
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv(override=True)

# gmail.modify lets us read messages and create drafts with one scope.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
HERE = Path(__file__).parent
CREDENTIALS_PATH = HERE / "credentials.json"  # you download this from Google Cloud
TOKEN_PATH = HERE / "token.json"              # created automatically on first sign-in


def get_gmail_service():
    """Sign in to Gmail (opens a browser the first time) and return an API client."""
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds)


def _extract_body(payload) -> str:
    """Pull readable text out of a Gmail message payload."""
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", "ignore")
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", "ignore")
    return ""


@function_tool
def read_emails() -> str:
    """Read the latest 5 emails from the user's real Gmail inbox and return them as JSON."""
    service = get_gmail_service()
    listed = service.users().messages().list(userId="me", maxResults=5, labelIds=["INBOX"]).execute()
    emails = []
    for ref in listed.get("messages", []):
        msg = service.users().messages().get(userId="me", id=ref["id"], format="full").execute()
        headers = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
        emails.append({
            "id": ref["id"],
            "from_name": headers.get("from", ""),
            "from_email": headers.get("from", ""),
            "date": headers.get("date", ""),
            "subject": headers.get("subject", ""),
            "body": _extract_body(msg["payload"])[:1500],
        })
    return json.dumps(emails, ensure_ascii=False)


class EmailTriage(BaseModel):
    email_id: str = Field(description="The id of the email this entry is about.")
    from_name: str = Field(description="Who the email is from.")
    subject: str = Field(description="The subject line of the email.")
    needs_reply: bool = Field(description="True if this email genuinely needs a reply.")
    reason: str = Field(description="A short reason for the needs_reply decision.")
    suggested_reply: str = Field(description="A ready-to-send draft reply, or empty string.")


class InboxReport(BaseModel):
    summary: str = Field(description="A 2-3 sentence summary of the whole inbox.")
    items: list[EmailTriage] = Field(description="One triage entry per email.")


INSTRUCTIONS = """
You are a helpful email assistant. Use the read_emails tool to fetch the inbox,
write a short summary, then for each email decide if it needs a reply and why,
and draft a polite concise reply for the ones that do. Leave suggested_reply
empty for emails that do not need one. Do not invent facts.
"""

triage_agent = Agent(
    name="Gmail Inbox Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[read_emails],
    output_type=InboxReport,
)


def create_draft(to_address: str, subject: str, body: str) -> str:
    """Create a REAL draft in the user's Gmail Drafts folder (does not auto-send)."""
    service = get_gmail_service()
    message = MIMEText(body)
    message["to"] = to_address
    message["subject"] = f"Re: {subject}"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
    return "draft created"


async def main() -> None:
    print("Reading your real Gmail inbox...\n")
    with trace("Gmail inbox triage"):
        result = await Runner.run(triage_agent, "Review my inbox and draft replies where needed.")
    report: InboxReport = result.final_output

    print("INBOX SUMMARY")
    print(report.summary)
    print("\n" + "=" * 60)

    for item in report.items:
        flag = "NEEDS REPLY" if item.needs_reply else "no reply needed"
        print(f"\n{item.from_name} — {item.subject}  ({flag})")
        print(f"    why: {item.reason}")
        if not item.needs_reply:
            continue
        print(f"\n    Suggested reply:\n    {item.suggested_reply}\n")
        if input("    Create this as a Gmail draft? [y/n]: ").strip().lower() == "y":
            create_draft(item.from_email, item.subject, item.suggested_reply)
            print("    ✅ Draft created in your Gmail.")

    print("\nDone. Open Gmail and check your Drafts folder.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

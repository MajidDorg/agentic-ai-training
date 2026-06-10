"""
Inbox Agent — your first agentic-AI project.

What it does:
  1. Reads your inbox (a sample inbox for now — your real Gmail is the level-up exercise).
  2. Summarizes the emails.
  3. Decides which ones need a reply, and WHY.
  4. Drafts a suggested reply for each one that needs it.
  5. Hands control back to YOU to approve / edit / skip before anything is "sent".

This single file teaches the three core ideas of the OpenAI Agents SDK:
  - tools          -> @function_tool  (read_emails)
  - structured output -> a Pydantic model the agent must fill in (InboxReport)
  - human-in-the-loop -> the agent drafts, but a human approves the send

Run it from the project root with:   uv run project/inbox_agent.py
"""

import json
import sys
from pathlib import Path

# Windows terminals default to a non-UTF-8 codepage that can't print emoji.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool, trace

# Load OPENAI_API_KEY from the .env file in the project root.
load_dotenv(override=True)

# The sample inbox lives next to this file.
INBOX_PATH = Path(__file__).parent / "sample_inbox.json"


# ---------------------------------------------------------------------------
# 1. A TOOL — the agent can call this to read the inbox.
#    @function_tool turns a normal Python function into something the agent
#    can decide to call on its own. No JSON boilerplate needed.
# ---------------------------------------------------------------------------
@function_tool
def read_emails() -> str:
    """Read the most recent emails from the user's inbox and return them as JSON."""
    emails = json.loads(INBOX_PATH.read_text(encoding="utf-8"))
    return json.dumps(emails, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 2. STRUCTURED OUTPUT — we force the agent to answer in this exact shape.
#    Instead of free text, the agent must fill in these fields for every email.
# ---------------------------------------------------------------------------
class EmailTriage(BaseModel):
    email_id: str = Field(description="The id of the email this entry is about.")
    from_name: str = Field(description="Who the email is from.")
    subject: str = Field(description="The subject line of the email.")
    needs_reply: bool = Field(description="True if this email genuinely needs a reply from the user.")
    reason: str = Field(description="A short reason explaining the needs_reply decision.")
    suggested_reply: str = Field(
        description="A ready-to-send draft reply. Empty string if needs_reply is False."
    )


class InboxReport(BaseModel):
    summary: str = Field(description="A 2-3 sentence summary of the whole inbox.")
    items: list[EmailTriage] = Field(description="One triage entry per email.")


# ---------------------------------------------------------------------------
# 3. THE AGENT — name + instructions + which model + its tools + its output shape.
# ---------------------------------------------------------------------------
INSTRUCTIONS = """
You are a helpful email assistant. When asked to review the inbox:
1. Use the read_emails tool to fetch the emails.
2. Write a short, friendly summary of the whole inbox.
3. For EACH email, decide whether it genuinely needs a reply from the user.
   - Real people asking questions, requests, overdue invoices, meeting requests -> usually need a reply.
   - Automated notifications, newsletters, calendar reminders, promotions -> usually do NOT.
4. For each email that needs a reply, write a polite, concise draft reply in the user's voice.
   For emails that do not need a reply, leave suggested_reply as an empty string.
Be honest and practical. Do not invent facts that are not in the emails.
"""

triage_agent = Agent(
    name="Inbox Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[read_emails],
    output_type=InboxReport,
)


async def run_triage(user_request: str = "Review my inbox and draft replies where needed.") -> InboxReport:
    """Run the agent and return a structured InboxReport. Used by both the CLI and the GUI."""
    with trace("Inbox triage"):
        result = await Runner.run(triage_agent, user_request)
    return result.final_output


# ---------------------------------------------------------------------------
# 4. SEND — mocked for the class. In the level-up exercise this calls real Gmail.
# ---------------------------------------------------------------------------
def send_email_mock(to_name: str, subject: str, body: str) -> str:
    """Pretend to send an email. Prints what WOULD be sent."""
    print("\n----- (MOCK) EMAIL SENT -----")
    print(f"To:      {to_name}")
    print(f"Subject: Re: {subject}")
    print(f"Body:\n{body}")
    print("-----------------------------\n")
    return "sent (mock)"


# ---------------------------------------------------------------------------
# 5. HUMAN-IN-THE-LOOP — the agent drafts, but YOU decide what gets sent.
#    This terminal loop is the simplest version. app.py wraps the same idea in a GUI.
# ---------------------------------------------------------------------------
async def main() -> None:
    print("Checking your inbox...\n")
    report = await run_triage()

    print("INBOX SUMMARY")
    print(report.summary)
    print("\n" + "=" * 60)

    for item in report.items:
        flag = "NEEDS REPLY" if item.needs_reply else "no reply needed"
        print(f"\n[{item.email_id}] {item.from_name} — {item.subject}  ({flag})")
        print(f"    why: {item.reason}")

        if not item.needs_reply:
            continue

        print(f"\n    Suggested reply:\n    {item.suggested_reply}\n")
        choice = input("    Send this reply? [y]es / [e]dit / [s]kip: ").strip().lower()

        if choice == "y":
            send_email_mock(item.from_name, item.subject, item.suggested_reply)
        elif choice == "e":
            new_body = input("    Type your edited reply, then Enter:\n    ")
            send_email_mock(item.from_name, item.subject, new_body)
        else:
            print("    Skipped.")

    print("Done. (Nothing was really sent — this is the mock inbox.)")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

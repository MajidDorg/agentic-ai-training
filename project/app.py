"""
Inbox Agent — GUI version (the showcase).

This wraps the SAME agent from inbox_agent.py in a simple web interface using Gradio.
Students can click a button to run the agent, read the drafts, edit them, and "send".

Run it from the project root with:   uv run project/app.py
Then open the local URL it prints (something like http://127.0.0.1:7860).

Want to show it to family/friends? Change `demo.launch()` at the bottom to
`demo.launch(share=True)` and Gradio gives you a temporary public link you can send.
"""

import asyncio

import gradio as gr

from inbox_agent import run_triage, send_email_mock, InboxReport

# We keep the latest report in memory so the "send" step can find the right draft.
LATEST: dict[str, InboxReport] = {}


def check_inbox():
    """Run the agent and return (summary_markdown, list of email ids that need a reply)."""
    report: InboxReport = asyncio.run(run_triage())
    LATEST["report"] = report

    # Build a readable markdown report of everything the agent found.
    lines = [f"### Inbox summary\n{report.summary}\n", "### Emails"]
    reply_choices = []
    for item in report.items:
        badge = "🟢 needs reply" if item.needs_reply else "⚪ no reply needed"
        lines.append(f"**[{item.email_id}] {item.from_name} — {item.subject}**  ·  {badge}")
        lines.append(f"> {item.reason}")
        if item.needs_reply:
            lines.append(f"\n_Suggested reply:_\n\n{item.suggested_reply}\n")
            reply_choices.append(f"{item.email_id} — {item.from_name}: {item.subject}")
        lines.append("")

    report_md = "\n".join(lines)
    # Update the dropdown of emails you can reply to, and clear the draft box.
    return report_md, gr.update(choices=reply_choices, value=None), ""


def load_draft(choice: str):
    """When the user picks an email in the dropdown, load its draft into the editable box."""
    if not choice or "report" not in LATEST:
        return ""
    email_id = choice.split(" — ")[0]
    for item in LATEST["report"].items:
        if item.email_id == email_id:
            return item.suggested_reply
    return ""


def send_selected(choice: str, edited_body: str):
    """Send (mock) the edited draft for the selected email."""
    if not choice or "report" not in LATEST:
        return "Pick an email first."
    email_id = choice.split(" — ")[0]
    for item in LATEST["report"].items:
        if item.email_id == email_id:
            send_email_mock(item.from_name, item.subject, edited_body)
            return f"✅ (Demo) Reply sent to {item.from_name} — Re: {item.subject}"
    return "Could not find that email."


with gr.Blocks(title="Inbox Agent") as demo:
    gr.Markdown("# 📬 Inbox Agent\nYour first AI agent — it reads your inbox, decides what needs a reply, and drafts it. You stay in control of what gets sent.")

    with gr.Row():
        run_btn = gr.Button("Check my inbox", variant="primary")

    report_out = gr.Markdown()

    gr.Markdown("---\n### Review & send")
    with gr.Row():
        with gr.Column(scale=1):
            picker = gr.Dropdown(label="Pick an email to reply to", choices=[], interactive=True)
        with gr.Column(scale=2):
            draft_box = gr.Textbox(label="Draft reply (edit before sending)", lines=8)
    send_btn = gr.Button("Send reply (demo)")
    status = gr.Markdown()

    # Wiring: button -> agent -> report + dropdown
    run_btn.click(check_inbox, outputs=[report_out, picker, draft_box])
    picker.change(load_draft, inputs=picker, outputs=draft_box)
    send_btn.click(send_selected, inputs=[picker, draft_box], outputs=status)


if __name__ == "__main__":
    # Change to demo.launch(share=True) to get a public link you can share.
    demo.launch()

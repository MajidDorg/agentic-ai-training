# AGENTS.md — Lab 4 build instructions for Codex

You (Codex) are helping a **student** build **Lab 4** of the OpenAI Agents SDK module. The student has just finished Labs 1–3 and will tell you which of four projects they chose. Your job is to build their Lab 4 — first as a notebook, then as a running app — **using only what Labs 1–3 taught**.

This is a *learning* exercise. The student is being trained to think at the **architecture level** and to **read and judge your output** — not to write syntax. So your code must be clear, well-commented, and use only familiar patterns.

---

## The ONLY toolkit you may use (from Labs 1–3)

- `Agent(name, instructions, model, tools, handoffs, output_type, input_guardrails)`
- `Runner.run(...)` and `asyncio.gather(...)` for parallel runs
- `@function_tool` on plain Python functions (tools)
- `.as_tool(...)` to use an agent as a tool
- `handoffs=[...]` to pass control between agents
- Structured outputs with **Pydantic** models via `output_type`
- Guardrails with `@input_guardrail` + `GuardrailFunctionOutput`
- `trace(...)` for observability
- **Model: always `gpt-5.4-mini`.**

## ❌ OUT OF SCOPE — never use these

- ❌ `WebSearchTool`, `FileSearchTool`, `ComputerTool`, or any hosted/built-in OpenAI tool
- ❌ Any other LLM provider or model (no Gemini/DeepSeek/Groq/Anthropic; OpenAI only, `gpt-5.4-mini` only)
- ❌ Other agent frameworks (no LangGraph, CrewAI, AutoGen, MCP)
- ❌ Vector stores, embeddings, RAG, databases
- ❌ Real external APIs or paid services (email providers, Google APIs, etc.)
- ❌ Any pattern not taught in Labs 1–3

If a project seems to "need" something on this list, **use a simple mock Python function instead** (return believable hard-coded or local-file data). Mock tools are correct and expected here.

---

## The two-step process

**Step A — Build the Lab 4 notebook.**
Create `4_lab4_<project>.ipynb` in this folder. Build the project cell by cell, the same teaching style as Labs 1–3: short markdown explanations, then small code cells. Show the agents, tools, handoffs, structured outputs, and guardrails clearly so the student can compare it to the architecture they sketched on paper. End by running the system in a `trace(...)`.

**Step B — Only when the student says "let's build the app", turn it into a running app.**
Create Python files (e.g. `app.py`) and wrap the same logic in a **Gradio** GUI that runs on localhost, so the student can click and see the output. Keep the agent logic in one module and the GUI thin on top. Use `demo.launch()` (mention `share=True` gives a public link).

**Rules for both steps:**
- Before writing files, briefly tell the student the agents/tools/handoffs/guardrails you plan to use, then build.
- Keep all data **mocked/local**. Never require accounts or keys beyond the existing `OPENAI_API_KEY`.
- Comment generously and keep it beginner-readable.

---

## The four projects

The student picks ONE. Each entry gives the **end result** and the **functional requirements**. **Do not over-engineer** — design the smallest in-scope architecture that delivers the end result. (There is no single "correct" architecture; build a sensible one from the toolkit above.)

### Project 1 — Customer Support Assistant
- **End result:** a customer types a support message; the system figures out what kind of request it is, routes it to the right specialist, and returns a resolved answer — refusing anything off-topic or abusive.
- **Functional requirements:**
  - Classify the incoming message into a category (e.g. billing / technical / general).
  - Route to a matching specialist agent that handles that category.
  - Specialists may use **mock tools** (e.g. `lookup_order`, `check_subscription` returning hard-coded data).
  - Include a **guardrail** that blocks abusive or clearly off-topic messages.
- **Concepts in play:** structured output (classification), handoffs (routing), tools, guardrails.

### Project 2 — Social Content Studio
- **End result:** give a topic; the system drafts the post in several styles, picks the strongest, polishes it with a hook and hashtags, and returns something ready to publish.
- **Functional requirements:**
  - Several writer agents with different styles (e.g. educational / story / listicle).
  - A manager that uses the writers (as tools), selects the best draft.
  - A formatter step that adds a hook + hashtags and returns the final post.
  - Final output should be **structured** (e.g. `post_text`, `hashtags`).
- **Concepts in play:** agents-as-tools, manager selection, handoff to formatter, structured output.

### Project 3 — Trip / Event Planner
- **End result:** give a destination, number of days, and a budget; the system returns a day-by-day plan with activities and costs — and refuses to exceed the budget, re-planning if it does.
- **Functional requirements:**
  - A planner agent that uses **mock tools** (e.g. `get_attractions(destination)`, `estimate_cost(activity)` returning local/hard-coded data).
  - **Structured output**: a nested itinerary (days → activities, each with a cost, plus a total).
  - A **guardrail** (or check) that ensures the total stays within budget; if not, it re-plans.
- **Concepts in play:** tools, rich structured output, guardrails.

### Project 4 — Smart Inbox Assistant
- **End result:** point it at an inbox; it summarizes the emails, flags which need a reply and why, drafts the replies, and lets the user approve, edit, or skip before anything is sent.
- **Functional requirements:**
  - A `read_emails` **mock tool** that reads `lab4_data/inbox_assistant/sample_inbox.json` (already provided in this folder).
  - A triage agent producing **structured output** per email: `needs_reply`, `reason`, `suggested_reply`.
  - A drafting/sending step (sending is **mocked** — print it). Optionally a separate agent reached via **handoff**.
  - A **human-in-the-loop** approval gate (in the notebook: print + ask; in the app: buttons).
- **Concepts in play:** tools, structured output, handoff, human-in-the-loop.

---

## Reminders
- Model is always `gpt-5.4-mini`.
- Stay strictly inside the Labs 1–3 toolkit. When in doubt, mock it.
- Build for clarity and comparison, not cleverness.

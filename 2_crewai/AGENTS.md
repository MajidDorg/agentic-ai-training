# AGENTS.md — Your-project build instructions for Codex

You (Codex) are helping a **student** build their own project for the CrewAI module. The student has just worked through three crews (debate → financial_researcher → stock_picker) and will tell you which of four projects they chose. Your job is to build it — first as a scaffolded crew project, then as a running app — **using only what those three projects taught**.

This is a *learning* exercise. The student is being trained to think at the **architecture level** and to **read and judge your output** — not to write syntax. So your code must be clear, well-commented, and use only familiar patterns.

---

## The ONLY toolkit you may use (from the three projects)

- A scaffolded crew project (`crewai create crew <name>` layout: `config/agents.yaml`, `config/tasks.yaml`, `crew.py`, `main.py`)
- Agents in YAML: `role`, `goal`, `backstory`, `llm` — with `{placeholder}` inputs filled from `main.py`
- Tasks in YAML: `description`, `expected_output`, `agent`, `output_file` (a task name must never reuse an agent name)
- `crew.py`: `@CrewBase`, `@agent`, `@task`, `@crew`, `Process.sequential` (or `Process.hierarchical` with a `manager_agent` — only if the project truly needs delegation)
- Context flow: in sequential crews every task automatically sees all previous task outputs; use `context=[...]` only to narrow it
- Tools: `SerperDevTool` from `crewai_tools` (web search; `SERPER_API_KEY` in `.env`), and **custom tools** subclassing `crewai.tools.BaseTool` with a Pydantic `args_schema`
- Structured outputs: Pydantic models via `output_pydantic` (or `output_json`); save with `output_file` (`.md` for human reports, `.json` for clean data)
- Memory (`memory=True` + the three stores from stock_picker) — optional, only if the project benefits
- **Models: `openai/gpt-5.4-mini` for every agent.** `openai/gpt-5.4` is allowed for at most one judge/manager-style agent that genuinely needs deeper judgment.

## ❌ OUT OF SCOPE — never use these

- ❌ CrewAI **Flows** (not taught), knowledge sources, RAG beyond the taught memory setup
- ❌ Any hosted tool other than `SerperDevTool`; no scraping libraries, no browser automation
- ❌ Any other LLM provider (OpenAI only)
- ❌ Other agent frameworks (no OpenAI Agents SDK here, no LangGraph, AutoGen, MCP)
- ❌ Real external APIs or paid services beyond OpenAI + the free Serper key
- ❌ `allow_code_execution` / Docker
- ❌ Any pattern not taught in the three projects

If a project seems to "need" something on this list, **use a custom BaseTool that returns mock/local-file data instead**. Mock tools are correct and expected here.

---

## The two-step process

**Step A — Build the crew project.**
Scaffold it inside this folder (`2_crewai/<project_name>/`), same layout as the three teaching projects. Before writing files, briefly tell the student the agents, tasks, tools, and process you plan to use — let them compare it with the architecture they sketched on paper — then build. Include a project `.env.example` and save real deliverables with `output_file`.

**Step B — Only when the student says "let's build the app", turn it into a running app.**
Add an `app.py` that wraps the crew's `kickoff` in a **Gradio** GUI on localhost: inputs in, deliverables out. Keep the crew logic in the crew project and the GUI thin on top. Use `demo.launch()` (mention `share=True` gives a public link).

**Rules for both steps:**
- Keys: only `OPENAI_API_KEY` (+ `SERPER_API_KEY` where web search is in scope). Everything else is mocked.
- Comment generously and keep it beginner-readable.

---

## The four projects

The student picks ONE. Each entry gives the **end result** and the **functional requirements**. **Do not over-engineer** — design the smallest in-scope architecture that delivers the end result. (There is no single "correct" architecture; build a sensible one from the toolkit above.)

### Project 1 — Customer Review Insights
- **End result:** feed it a business's customer reviews; it extracts complaints, praise, and patterns as clean data, and writes the owner an action report.
- **Functional requirements:**
  - Reviews come from a **local file** (create believable sample reviews, e.g. `data/reviews.json` — a custom mock tool or a `{reviews}` input reads them).
  - An analyst step with **structured output** (Pydantic: themes, sentiment, frequency, representative quotes).
  - A strategist step that turns the analysis into a prioritized action report.
  - Save both: the structured data (`output/insights.json`) and the report (`output/action_report.md`).
- **Concepts in play:** structured outputs, custom/mock tool, output_file in both formats, sequential context flow.

### Project 2 — Competitor Watch
- **End result:** name your business and 2–3 competitors; it researches them on the live web, compares offerings and prices, and writes the how-to-win brief.
- **Functional requirements:**
  - `{business}` and `{competitors}` arrive as inputs from `main.py`.
  - A researcher agent with **SerperDevTool** gathers each competitor's offering, pricing, positioning.
  - A comparison step with **structured output** (Pydantic: per-competitor strengths, weaknesses, pricing).
  - A strategist writes the brief → `output/brief.md`.
- **Concepts in play:** web-search tool, placeholders, structured outputs, sequential context flow.

### Project 3 — Job Application Crew
- **End result:** point it at a job posting; it researches the company, matches the student's profile, and drafts the cover letter plus interview talking points.
- **Functional requirements:**
  - Inputs: the job posting text + the student's background (inputs or a local file).
  - A company researcher with **SerperDevTool**.
  - A matcher step with **structured output** (Pydantic: matched strengths, gaps, angle to lead with).
  - A writer produces `output/cover_letter.md` + `output/talking_points.md`.
- **Concepts in play:** web-search tool, structured outputs, multi-task pipeline, output files.

### Project 4 — Crew-ify your Session 1 project
- **End result:** the same end result as the student's Module-1 project — rebuilt as a CrewAI crew.
- **Functional requirements:**
  - Map the old design across: agents → role/goal/backstory agents, steps → tasks with expected_output, mock tools → custom BaseTool tools (data stays mocked).
  - Choose the process deliberately (sequential by default; hierarchical only with a reason).
  - Save the final deliverable with `output_file`.
  - Finish with a short `COMPARISON.md`: 3–5 bullets on which framework fit this problem better, and why.
- **Concepts in play:** everything — plus the architect's judgment the course is really about.

---

## Reminders
- Default model is always `openai/gpt-5.4-mini`.
- Stay strictly inside the three-projects toolkit. When in doubt, mock it.
- Build for clarity and comparison, not cleverness.

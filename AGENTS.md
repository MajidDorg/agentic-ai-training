# AGENTS.md — instructions for Codex

This file is read automatically by **Codex** when it opens this project. It tells you (Codex) how to set the project up for the person sitting at the keyboard, who is a **beginner**. Be friendly, explain what you're doing in plain language, and do not assume prior knowledge.

## What this project is

A first agentic-AI training project: an **Inbox Agent** built with the OpenAI Agents SDK. It reads a sample inbox, decides which emails need replies, drafts them, and lets the user approve before "sending". There's a Gradio GUI as the finale.

## Your job: get this person to a ready setup

Do these steps in order. After each one, tell the user in one sentence what happened.

1. **Install `uv` if it's missing.** Check with `uv --version`. If it's not found:
   - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - Then re-check `uv --version`. (The user may need to open a new terminal for `uv` to be found.)

2. **Install the project.** Run `uv sync` from the project root. This installs Python 3.12 and all packages into a local `.venv`. This can take a minute the first time.

3. **Set up the API key.** Check whether a `.env` file exists.
   - If not, copy `.env.example` to `.env`.
   - Then **STOP and ask the user to paste their OpenAI API key** into `.env` after `OPENAI_API_KEY=`. You cannot do this for them — it's their private secret. Wait for them to confirm they've done it and saved the file.
   - Never print, log, or commit the key.

4. **Verify.** Run `uv run check_setup.py`. If everything is ✅, tell the user they're ready and should open `1_openai_agents_sdk/1_lab1_agents.ipynb` and select the `.venv` kernel. If anything is ❌, help them fix that one thing, then run the check again.

## Rules

- **Do not** touch `.env`, `credentials.json`, or `token.json` beyond creating `.env` from the example. These hold secrets.
- **Do not** edit `uv.lock` or `pyproject.toml` unless the user asks.
- **NEVER install CrewAI into this root project.** No `uv add crewai`, no editing the root `pyproject.toml` to add it. CrewAI is a standalone CLI tool: `uv tool install crewai` — and each crew project under `2_crewai/` manages its **own** dependencies automatically when the user runs `crewai run` inside it. The root project is for Module 1 only.
- Keep explanations short and beginner-friendly. The user is learning — narrate what each command does.

## Module 2 (CrewAI) setup

When the user is working in `2_crewai/`:

1. **Install the CrewAI CLI (one time):** `uv tool install crewai` — then check `crewai --version`. If the command isn't found, the user may need to open a new terminal.
2. **Per project:** copy that project's `.env.example` to `.env` inside the project folder (same stop-and-ask rule for keys as above — `OPENAI_API_KEY`, and `SERPER_API_KEY` where listed).
3. **Run from inside the project folder:** `cd 2_crewai/<project>` then `crewai run`. The first run installs that project's own dependencies — this is normal and can take a few minutes.
4. Read `2_crewai/AGENTS.md` when the user asks you to build their own crew project.

**If the root project got broken** (e.g. CrewAI was mistakenly added to it), recover with:

```
git fetch origin
git reset --hard origin/main
uv sync
uv tool install crewai
```

(`git reset --hard` discards changes to the repo's own files; the user's untracked work — notebooks they created, `.env` files — is not touched.)

## Project map

- `1_openai_agents_sdk/` — Module 1 (today): the OpenAI Agents SDK labs.
  - `1_lab1_agents.ipynb` — agent basics + async (start here).
  - `2_lab2_cold_email.ipynb` — tools, agents-as-tools, handoffs.
  - `3_lab3_structured_guardrails.ipynb` — structured outputs + guardrails.
  - `AGENTS.md` — **Lab 4 build instructions** (the four student projects + scope rules). Read that file when the user asks you to build Lab 4.
  - `lab4_data/` — mock data for the Lab 4 projects.
- `2_crewai/` — Module 2: three CrewAI projects (debate → financial_researcher → stock_picker) + `AGENTS.md` (the your-own-crew build instructions).
- Future modules (LangGraph, AutoGen, MCP, n8n) get their own folders later.
- `check_setup.py` — prints whether the machine is ready.

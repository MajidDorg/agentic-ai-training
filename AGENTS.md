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
- Keep explanations short and beginner-friendly. The user is learning — narrate what each command does.

## Project map

- `1_openai_agents_sdk/` — Module 1 (today): the OpenAI Agents SDK labs.
  - `1_lab1_agents.ipynb` — agent basics + async (start here).
  - `2_lab2_cold_email.ipynb` — tools, agents-as-tools, handoffs.
  - `3_lab3_structured_guardrails.ipynb` — structured outputs + guardrails.
  - `AGENTS.md` — **Lab 4 build instructions** (the four student projects + scope rules). Read that file when the user asks you to build Lab 4.
  - `lab4_data/` — mock data for the Lab 4 projects.
- Future modules (AutoGen, LangGraph, CrewAI, MCP, n8n) get their own folders later.
- `check_setup.py` — prints whether the machine is ready.

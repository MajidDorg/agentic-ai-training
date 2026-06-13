# Module 3 — LangGraph

The third framework. LangGraph models an agent system as a **graph**: a **State** that flows through **Nodes** (Python functions) connected by **Edges** (which decide what runs next). Two short labs teach it; then **Lab 3 is yours**.

This module is a **self-contained project** with its own environment (like the CrewAI module) — so its packages stay separate from Module 1.

---

## Setup — one time, inside this folder

**The easy way:** open Codex in this folder and say:
> Read AGENTS.md and set up this module for me. I'm a beginner.

**Or do it yourself:**
1. `cd 3_langgraph`
2. `uv sync` — installs Python + LangGraph into `3_langgraph/.venv` (takes a minute the first time).
3. Copy `.env.example` to `.env`, then paste your keys:
   - `OPENAI_API_KEY` — the LLM (both labs).
   - `SERPER_API_KEY` — free web-search key from https://serper.dev (Lab 2's search tool).
   - macOS: `cp .env.example .env` · Windows: `copy .env.example .env`
4. Open a lab notebook → **Select Kernel** (top-right) → choose the **`3_langgraph/.venv`** option.

Run cells with **Shift + Enter**.

---

## The labs

| Lab | File | What you learn |
|---|---|---|
| **1** | [1_lab1_graphs.ipynb](1_lab1_graphs.ipynb) | State, the `add_messages` reducer, nodes, edges, compile, **invoke** — build a graph from scratch, then a real-LLM chatbot |
| **2** | [2_lab2_tools_memory.ipynb](2_lab2_tools_memory.ipynb) | **Tools** + conditional edges (`ToolNode`, `tools_condition`), **super-steps**, **checkpointing** (memory between turns), **SQLite** persistence, **LangSmith** tracing |
| **3** | *you build it* | Pick a project, sketch the graph on paper, let **Codex** build it, compare |

---

## Lab 3 — your project

After Lab 2 you'll have the full toolkit: state + reducers, nodes, edges, conditional routing, tools, checkpointed memory, SQLite persistence.

1. Your instructor presents project options (by their end result).
2. You **sketch the graph** — which state, nodes, edges, tools, where memory lives.
3. You tell **Codex** your choice; it builds the Lab 3 notebook within what Labs 1–2 taught — see [AGENTS.md](AGENTS.md).
4. You **compare** your sketch with Codex's build.
5. Then Codex wraps it in a **Gradio** GUI → your third CV demo.

The point: think like an **architect** and learn to **read and judge** what the AI builds — not memorize syntax.

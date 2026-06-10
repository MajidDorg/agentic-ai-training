# Agentic AI — Training Project

Welcome! In this session you'll build your **first AI agent** with the **OpenAI Agents SDK**: an **Inbox Agent** that reads your inbox, decides which emails need a reply (and *why*), drafts the replies, and lets *you* approve before anything is sent — finished off with a clickable web app you can show your friends and family.

By the end you'll understand the three building blocks every agent is made of: **agents, tools, and structured output** — plus the idea of keeping a **human in the loop**.

---

## 🚀 Start here

1. **Set up your machine** → follow **[SETUP.md](SETUP.md)** (works on Mac & Windows; you can let Codex do most of it).
2. **Learn the concepts** → open **[notebooks/01_concepts.ipynb](notebooks/01_concepts.ipynb)**.
3. **Build the project** → **[project/inbox_agent.py](project/inbox_agent.py)**.
4. **Show it off** → run the GUI: `uv run project/app.py`.

Confirm your setup any time with:

```
uv run check_setup.py
```

---

## What's in this repo

| Path | What it is |
|---|---|
| `notebooks/01_concepts.ipynb` | Teaching notebook: agent → tool → structured output, one idea at a time. |
| `project/inbox_agent.py` | The Inbox Agent: reads a sample inbox, triages, drafts, and asks you before sending. |
| `project/sample_inbox.json` | A realistic sample inbox the agent reads (no email account needed). |
| `project/app.py` | The **Gradio GUI** — the showcase version you can share. |
| `level-up/` | **Optional / advanced:** connect the agent to your **real Gmail**. Try it after class. |
| `check_setup.py` | Tells you if your machine is ready. |
| `SETUP.md` | Full setup instructions (Mac + Windows). |
| `AGENTS.md` | Instructions Codex reads to set the project up for you. |

---

## How the Inbox Agent works

```
You ask  ──▶  Inbox Agent
                 │  1. calls the read_emails tool        (TOOL)
                 │  2. summarizes the inbox
                 │  3. per email: needs reply? why?      (STRUCTURED OUTPUT)
                 │  4. drafts a reply for the ones that do
                 ▼
            You review ──▶ approve / edit / skip         (HUMAN IN THE LOOP)
                 ▼
            Send  (mocked in class · real Gmail draft in the level-up exercise)
```

During the class the agent reads `sample_inbox.json`, so everyone can build and run it with no email setup. Connecting it to your real Gmail is the optional **[level-up exercise](level-up/connect-your-gmail.md)**.

---

*Built for the Agentic AI training program. Instructor: Majid Dorgham.*

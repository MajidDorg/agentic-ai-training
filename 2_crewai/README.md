# Module 2 — CrewAI

The second framework of the course. No notebooks this time — CrewAI works in **real project files**. Each project below is a complete, scaffolded crew: you'll read it, run it, and change it.

## One-time setup

```
uv tool install crewai
```

Then, **inside each project folder** you want to run:

1. Copy `.env.example` to `.env` and paste your key(s). The researcher projects also need a free [serper.dev](https://serper.dev) key for web search.
2. Run it:
   ```
   crewai run
   ```
   (The first run installs that project's dependencies automatically.)

## If your setup broke — reset to a safe point

If CrewAI got installed into the root project by mistake (or anything else went sideways), run from the **repo root**:

```
git fetch origin
git reset --hard origin/main
uv sync
uv tool install crewai
```

This restores the repo's own files to the clean published state and reinstalls correctly. Your untracked work (notebooks you created, your `.env` files) is not touched. Then `cd` into a project and `crewai run`.

## The projects

| # | Project | New concepts |
|---|---|---|
| **1** | [debate/](debate/) | Agents (role · goal · backstory), tasks (description · expected_output), the crew, sequential process, automatic context flow |
| **2** | [financial_researcher/](financial_researcher/) | **Tools** (SerperDevTool web search), saving outputs with output_file |
| **3** | [stock_picker/](stock_picker/) | **Structured outputs** (Pydantic schemas), a **custom tool**, **hierarchical process** (manager agent), **memory** (short-term, long-term, entity) |

Work them in order — each project adds concepts on top of the previous one.

## Where the action is (every project, same five files)

```
<project>/
  src/<project>/
    config/
      agents.yaml     <- who the agents are
      tasks.yaml      <- what they must do
    crew.py           <- wiring: agents + tasks + process
    main.py           <- inputs + kickoff
```

Five steps to any crew: create the project → define agents + tasks in YAML → complete crew.py → set inputs in main.py → `crewai run`.

## Your project

After the three projects you'll have the full CrewAI toolkit. You pick ONE of the four options, sketch the architecture on paper (agents, tasks, tools, outputs, process), build your own crew, and wrap a **Gradio GUI** on top. That's your second CV demo.

The four options are: **Customer Review Insights · Competitor Watch · Job Application Crew · Crew-ify your Session 1 project.** Full specs are in [AGENTS.md](AGENTS.md) (that's the file Codex reads).

---

*Note: the debate runs on `gpt-5.4-mini` agents with a `gpt-5.4` judge — one OpenAI key covers everything. The stock picker's push-notification tool writes to `output/notifications.md` (in production you'd point the same tool at a real push service).*

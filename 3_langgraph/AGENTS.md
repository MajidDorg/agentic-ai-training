# AGENTS.md — instructions for Codex (Module 3 — LangGraph)

You (Codex) are helping a **beginner** student with the LangGraph module. This file has two jobs:
**(1)** set the module up so they can run the labs, and **(2)** when they ask, build their own Lab 3 project — **using only what Labs 1–2 taught**.

Be friendly, explain each step in one plain sentence, and don't assume prior knowledge.

---

## Part 1 — Get this person to a ready setup

This module is a **self-contained uv project** (its own `.venv` and `.env`, separate from Module 1). Do these in order, inside the `3_langgraph/` folder.

1. **Check `uv`.** Run `uv --version`. If missing:
   - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - Re-check (a new terminal may be needed).
2. **Install the module.** From inside `3_langgraph/`, run `uv sync`. This creates `3_langgraph/.venv` with Python 3.12 + LangGraph. First run can take a couple of minutes.
3. **Set up keys.** If there's no `.env`, copy `.env.example` to `.env`. Then **STOP and ask the user** to paste their keys after the `=` signs and save:
   - `OPENAI_API_KEY` (required, both labs)
   - `SERPER_API_KEY` (required for Lab 2's search tool — free at https://serper.dev)
   - You cannot do this for them — these are private secrets. Never print, log, or commit them.
4. **Point them at the labs.** Tell the user to open `1_lab1_graphs.ipynb`, click **Select Kernel** (top-right), and choose the **`3_langgraph/.venv`** option. Run cells with Shift+Enter.

**If the module's environment breaks**, recover with:
```
git fetch origin
git reset --hard origin/main
cd 3_langgraph
uv sync
```
(`git reset --hard` discards changes to the repo's own files; the user's `.env` and any notebooks they created are untracked and not touched.)

## Rules

- **Do not** touch `.env` beyond creating it from `.env.example`. It holds secrets.
- **Do not** edit `uv.lock` or `pyproject.toml` unless the user asks.
- This module is **separate from Module 1** — run `uv sync` from inside `3_langgraph/`, and use the `3_langgraph/.venv` kernel for these notebooks.
- Keep explanations short and beginner-friendly. Narrate what each command does.

---

## Part 2 — Building the student's Lab 3 project

The student has finished Labs 1–2 and will tell you which project they chose. Build it — first as a notebook, then (only when they ask) as a running app — **using only the toolkit below.** This is a *learning* exercise: clear, well-commented code, familiar patterns only, so the student can compare it with the graph they sketched on paper.

### The ONLY toolkit you may use (from Labs 1–2)

- A **State** as a `TypedDict` or Pydantic `BaseModel` with `messages: Annotated[list, add_messages]` (add other fields if the project needs them)
- `StateGraph(State)`, `graph_builder.add_node(name, fn)`, `add_edge(START/END, ...)`, `.compile(...)`
- **Nodes** = plain Python functions: take the state, return a partial state update (e.g. `{"messages": [...]}`)
- The LLM via `ChatOpenAI(model="gpt-5.4-mini")` and `llm.bind_tools(tools)`
- **Tools:** `Tool(name=..., func=..., description=...)`. Web search via `GoogleSerperAPIWrapper` (needs `SERPER_API_KEY`). **Custom tools = plain Python functions** that return local/mock data or write to a local file (e.g. `output/...`).
- **Conditional routing:** `ToolNode(tools)` + `tools_condition` + `add_conditional_edges(...)`, with the tools node looping back to the chatbot
- **Memory:** `MemorySaver` (in-RAM) or `SqliteSaver` (persistent) passed as `checkpointer=` at compile, plus a `config = {"configurable": {"thread_id": ...}}` on every `invoke`
- A **Gradio** GUI on top (`gr.ChatInterface(...).launch()`) — only at Step B

### ❌ OUT OF SCOPE — never use these

- ❌ Any other LLM provider or model (OpenAI only, `gpt-5.4-mini` only)
- ❌ Other agent frameworks (no OpenAI Agents SDK, CrewAI, AutoGen, MCP here)
- ❌ **LangGraph Platform / Studio / any cloud deploy** — local framework only
- ❌ Real external paid APIs or accounts beyond OpenAI + the free Serper key — **mock everything else** with a local Python function
- ❌ Vector stores, embeddings, RAG, databases beyond the taught SQLite checkpointer
- ❌ Any pattern not taught in Labs 1–2

If a project seems to "need" something on this list, **use a simple Python function that returns believable local/mock data instead.** Mock tools are correct and expected here.

### The two-step process

**Step A — Build the Lab 3 notebook.** Create `3_lab3_<project>.ipynb` in this folder. Build it the same teaching style as Labs 1–2: short markdown explanation, then a small code cell. Show the state, nodes, edges, tools, and where memory lives clearly, so the student can compare it to their sketch. Before writing, tell the student the state/nodes/edges/tools you plan to use; then build.

**Step B — Only when the student says "let's build the app",** wrap the same graph in a Gradio GUI in an `app.py` (keep the graph logic in one module, the GUI thin on top). `demo.launch()` runs locally; mention `share=True` gives a public link.

**Rules for both steps:**
- Keys: only `OPENAI_API_KEY` (+ `SERPER_API_KEY` if web search is in scope). Everything else mocked/local.
- Comment generously, keep it beginner-readable.

### The project options

The student picks ONE. Each gives the **end result** + the **functional requirements**. **Do not over-engineer** — build the smallest in-scope graph that delivers the result.

#### Project 1 — Research-and-notify assistant
- **End result:** the user asks something that needs current info; the agent searches the web, summarizes the answer, and "notifies" the user (writes it to a local file).
- **Requirements:** a `search` tool (Serper) + a custom `notify` tool that appends to `output/notifications.md`; conditional routing so the model calls tools when needed; checkpointed memory so it remembers the conversation.

#### Project 2 — Personal assistant with persistent memory
- **End result:** a chatbot that remembers you across restarts — your name, preferences, and past chat.
- **Requirements:** `SqliteSaver` persistence keyed by a `thread_id`; show that after a kernel restart it still knows you. Tools optional.

#### Project 3 — Tool-using Q&A agent
- **End result:** an agent that answers questions by deciding which of its tools to use.
- **Requirements:** at least two tools (e.g. `search` + one custom mock tool of your design); `ToolNode` + `tools_condition` routing; the loop back to the chatbot.

#### Project 4 — LangGraph-ify an earlier project
- **End result:** the same end result as the student's Module-1 or Module-2 project — rebuilt as a LangGraph graph.
- **Requirements:** map the old design across (steps → nodes, routing → conditional edges, tools → Tools/mock functions). Add a short `COMPARISON.md`: 3–5 bullets on which framework fit this problem better, and why.

---

## Reminders
- Model is always `gpt-5.4-mini`.
- Stay strictly inside the Labs 1–2 toolkit. When in doubt, mock it.
- Build for clarity and comparison, not cleverness.

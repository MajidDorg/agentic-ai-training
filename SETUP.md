# Setup — get ready for class

Works on **macOS** and **Windows**. The whole point: by the end you can open `1_openai_agents_sdk/1_lab1_agents.ipynb` and run the first cell.

You have two ways to do this. **Way A (recommended)** lets Codex do most of it for you. **Way B** is the manual version if you'd rather type the commands yourself.

---

## Before you start — the three prerequisites

1. **VS Code** installed — https://code.visualstudio.com/
2. **Codex extension** installed in VS Code and **signed in** with your ChatGPT account.
   - Also install the **Python** and **Jupyter** extensions (search them in the Extensions panel).
3. **An OpenAI API key** — create one at https://platform.openai.com/api-keys (it starts with `sk-proj-`). Add a few dollars of credit at https://platform.openai.com/settings/organization/billing — the class uses only a small amount.

> You do **not** need to install Python or `uv` yourself — the setup handles that.

---

## Way A — let Codex set it up (recommended)

1. **Clone the repo.** In VS Code, open a terminal (`Terminal → New Terminal`) and run:
   ```
   git clone https://github.com/MajidDorg/agentic-ai-training.git
   ```
   Then `File → Open Folder` and open the `agentic-ai-training` folder.

2. **Ask Codex to set it up.** Open Codex in VS Code and send it this message:
   > Read AGENTS.md and set up this project for me. I'm a beginner.

   Codex will install `uv`, run `uv sync`, and create your `.env` file. When it asks, **paste your OpenAI API key** into the `.env` file after `OPENAI_API_KEY=` and save it.

3. **Confirm you're ready.** In the terminal run:
   ```
   uv run check_setup.py
   ```
   When you see **🎉 All set**, open `1_openai_agents_sdk/1_lab1_agents.ipynb`, click **Select Kernel** (top right), and choose the `.venv` option.

---

## Way B — manual setup

1. **Install `uv`** (the tool that manages Python for us):
   - **macOS:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - Close and reopen the terminal, then check: `uv --version`

2. **Clone and enter the project:**
   ```
   git clone https://github.com/MajidDorg/agentic-ai-training.git
   cd agentic-ai-training
   ```

3. **Install everything:**
   ```
   uv sync
   ```

4. **Create your `.env` file:** copy `.env.example` to `.env`, then paste your key after `OPENAI_API_KEY=` and save.
   - macOS: `cp .env.example .env`
   - Windows: `copy .env.example .env`

5. **Check:**
   ```
   uv run check_setup.py
   ```
   See **🎉 All set**? You're ready.

---

## Running things

- **The labs:** open the notebooks in `1_openai_agents_sdk/` (start with `1_lab1_agents.ipynb`), pick the `.venv` kernel, run cells with **Shift + Enter**.
- **Lab 4 (your project):** you'll build this with Codex during class — pick a project, sketch the architecture, then let Codex build the notebook and a GUI app.
- **Running a GUI app** (once you've built one): `uv run <path>/app.py`, then open the link it prints. To share it, change the last line to `demo.launch(share=True)`.

## Common snags (Windows)

- **Long path errors:** Windows has an old 260-character filename limit. If you hit it, enable long paths (search "enable long paths Windows") and restart.
- **Antivirus / VPN / firewall** can block installs or the OpenAI connection — pause them if a step mysteriously fails.

## Common snags (everyone)

- **`uv: command not found`** right after installing — open a brand new terminal window.
- **No `.venv` kernel in the notebook** — make sure `uv sync` finished, then click Select Kernel again and look under "Python Environments".
- **`OPENAI_API_KEY missing`** — your file must be named exactly `.env` (not `env` or `.env.txt`), and the key goes right after the `=` with no spaces.

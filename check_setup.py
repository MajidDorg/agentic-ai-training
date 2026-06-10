"""
Setup check — run this to confirm your machine is ready before class.

    uv run check_setup.py

It prints a clear ✅ or ❌ for each thing the project needs.
"""

import os
import sys

# Windows terminals default to a non-UTF-8 codepage that can't print emoji.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    ok = True

    # 1. Python version (uv should give us 3.12+)
    if sys.version_info >= (3, 12):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} — need 3.12+")
        ok = False

    # 2. The packages are installed
    try:
        import agents  # noqa: F401
        print("✅ openai-agents installed")
    except ImportError:
        print("❌ openai-agents not installed — run: uv sync")
        ok = False

    try:
        import gradio  # noqa: F401
        print("✅ gradio installed")
    except ImportError:
        print("❌ gradio not installed — run: uv sync")
        ok = False

    # 3. The API key is present
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
    except ImportError:
        print("❌ python-dotenv not installed — run: uv sync")
        ok = False

    key = os.environ.get("OPENAI_API_KEY", "")
    if key.startswith("sk-"):
        print(f"✅ OPENAI_API_KEY found (starts with {key[:6]}...)")
    else:
        print("❌ OPENAI_API_KEY missing — copy .env.example to .env and paste your key")
        ok = False

    print()
    if ok:
        print("🎉 All set. You're ready — open 1_openai_agents_sdk/1_lab1_agents.ipynb to begin.")
        return 0
    print("Some checks failed. Fix the ❌ items above, then run this again.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

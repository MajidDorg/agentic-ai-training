# Level up 🚀 — connect the agent to your real Gmail

> **This is an optional, advanced exercise.** Do it *after* you finish the main project. It is **not** part of the class, and you do **not** need it to complete or showcase your Inbox Agent. Take it on if you want to push the project to the next level.

In the class, your agent read a **sample inbox** (`project/sample_inbox.json`). Here you'll point the *same* agent at your **real Gmail**, and have it create real draft replies in your Drafts folder.

To keep you safe, this version creates **drafts** — it does *not* auto-send emails to real people. You review each draft in Gmail and send it yourself.

---

## Why this needs extra setup

Reading your inbox means using the **Gmail API**, and Google requires you to authorize that through a **Google Cloud project** with OAuth. (This is exactly why the class used a sample inbox instead — so everyone could finish without this step.) It's very doable; just follow along carefully.

---

## Step 1 — Install the extra Python packages

From the project root, run:

```bash
uv add google-api-python-client google-auth-oauthlib google-auth-httplib2
```

## Step 2 — Create a Google Cloud project + enable Gmail

1. Go to https://console.cloud.google.com/ and sign in with the Gmail you want to use.
2. Top bar → project dropdown → **New Project** → name it `inbox-agent` → **Create**, then select it.
3. Search bar → **Gmail API** → **Enable**.

## Step 3 — Configure the OAuth consent screen

1. Left menu → **APIs & Services → OAuth consent screen**.
2. User type: **External** → **Create**.
3. Fill in app name (`Inbox Agent`), your email for the support + developer fields → **Save and Continue**.
4. **Scopes** page → just **Save and Continue** (we set the scope in code).
5. **Test users** → **Add Users** → add **your own Gmail address** → **Save and Continue**.
   - This keeps the app in "Testing" mode, which is all you need for yourself.

## Step 4 — Create credentials

1. Left menu → **APIs & Services → Credentials**.
2. **Create Credentials → OAuth client ID**.
3. Application type: **Desktop app** → name it → **Create**.
4. Click **Download JSON**. Rename the file to **`credentials.json`** and put it in the **`level-up/`** folder (next to `gmail_inbox_agent.py`).
   - `credentials.json` and `token.json` are already gitignored, so they will not be pushed.

## Step 5 — Run it

From the project root:

```bash
uv run level-up/gmail_inbox_agent.py
```

- The first run opens your browser to sign in and approve. You may see a **"Google hasn't verified this app"** warning — because it's your own test app, click **Advanced → Go to Inbox Agent (unsafe)** → **Continue**. This is expected for a personal app in Testing mode.
- After you approve, a `token.json` is saved so you won't have to sign in again.
- The agent reads your last 5 emails, summarizes them, and offers to create drafts. Approve the ones you like, then open Gmail → **Drafts** to see them.

---

## Ideas to go even further

- Switch drafts to real sending (change `create_draft` to a send call) — only once you trust it.
- Have the agent label or archive newsletters automatically.
- Filter to only unread emails, or only emails from real people.
- Wrap this Gmail version in the Gradio GUI, just like `project/app.py`.

# ReachFlow — Setup Guide

Welcome to **ReachFlow**, your personal AI-powered cold email generator. This guide will get you up and running in about five minutes — no technical experience required.

---

## What Is ReachFlow?

ReachFlow is a desktop app that runs locally on your computer. Open it in your browser, fill in a few details about your prospect, and it writes a polished, personalized cold email for you in seconds.

Everything runs on your machine. Your data never leaves your computer, and the AI that powers it is completely free to use.

---

## What You Need

Before you start, make sure you have two things:

**1. Python 3.8 or later**

Python is free software that ReachFlow needs to run. Check if you already have it:

- **Mac:** Open Terminal and type `python3 --version`, then press Enter.
- **Windows:** Open Command Prompt and type `python --version`, then press Enter.

If you see a version number like `3.10.4`, you're good. If not, download Python for free at [python.org/downloads](https://www.python.org/downloads/). During installation on Windows, make sure to check the box that says **"Add Python to PATH"** before clicking Install.

**2. A Free Groq API Key**

Groq provides the AI that powers ReachFlow. Their free tier gives you 14,400 requests per day — more than enough for any outreach campaign. No credit card is required.

---

## Getting Your Free Groq API Key

1. Go to **[console.groq.com](https://console.groq.com)**
2. Click **Sign Up** and create a free account
3. Once logged in, click **API Keys** in the left sidebar
4. Click **Create API Key**, give it any name (e.g. "ReachFlow"), and click **Submit**
5. Copy the key — it starts with `gsk_`

Keep that key handy. You'll paste it into ReachFlow on first launch.

---

## Running ReachFlow

### Mac

1. Open the **ReachFlow** folder
2. **Double-click `start.command`**
3. A Terminal window will open and your browser will launch automatically at `http://localhost:5000`

> **First time on Mac?** macOS may block the script because it was downloaded from the internet. If nothing happens when you double-click, **right-click `start.command`** and choose **Open**. Click **Open** again in the dialog that appears. You only need to do this once.

### Windows

1. Open the **ReachFlow** folder
2. **Double-click `start.bat`**
3. A command window will open and your browser will launch automatically at `http://localhost:5000`

---

## First Run: The Setup Wizard

The first time ReachFlow starts, it will open a **Setup** page in your browser instead of the main app. This is completely normal.

1. Paste your Groq API key (the one starting with `gsk_`) into the field
2. Click **Save and Continue**
3. ReachFlow verifies the key and takes you straight to the main app

Your key is saved locally in a file called `config.json` inside the ReachFlow folder. You will never need to enter it again.

---

## Using ReachFlow

Once you're on the main screen:

1. Fill in the fields — your name, your offer, your prospect's name, company, and anything relevant about them
2. Click **Generate Email**
3. The email streams in word by word, just like a live response
4. Copy it, paste it into your email client, and send

Repeat as many times as you like. There's no usage limit on your end.

---

## Tips for Great Cold Emails

The more detail you give, the better the output. A few habits that make a real difference:

- **Be specific about the prospect.** Instead of "they run a marketing agency," try "they run a 12-person B2B marketing agency focused on SaaS companies." Specificity produces specificity.
- **Describe your offer clearly.** Don't just say "I do SEO." Say "I help B2B SaaS companies rank for bottom-of-funnel keywords and book more demo calls through organic search."
- **Mention a pain point.** If you know something about their situation — recent funding, a job posting, a podcast they appeared on — put it in the notes field. ReachFlow will work it in naturally.
- **Regenerate freely.** Not happy with the first result? Hit Generate again. Each run produces a different version. Try two or three and choose the one that fits your voice.
- **Trim before sending.** AI-written emails are a strong starting point. Read it out loud — if anything sounds stiff or over-polished, soften it to match how you actually talk.

---

## Troubleshooting

### "I double-clicked `start.command` and nothing happened" (Mac)

macOS blocks scripts downloaded from the internet by default. **Right-click `start.command`**, choose **Open**, and click **Open** in the security dialog. You only have to do this the very first time.

### "`pip` is not recognized" or "`python` is not recognized" (Windows)

Python isn't installed or wasn't added to your system PATH.

1. Uninstall Python if it's already on your machine
2. Download it fresh from [python.org/downloads](https://www.python.org/downloads/)
3. During installation, check **"Add Python to PATH"** before clicking Install
4. Restart your computer, then try `start.bat` again

### "Port 5000 is already in use"

Another application is using the same network port. Try these steps:

- Close any other browser tabs or apps that might be running a local server
- Wait 30 seconds and run `start.command` / `start.bat` again
- If the problem persists, restart your computer and try again before opening anything else

### "The app opened but emails aren't generating"

This is almost always an API key issue. Check the following:

1. Log in to [console.groq.com](https://console.groq.com) and confirm your API key is active
2. Open the `config.json` file inside the ReachFlow folder and confirm the key starts with `gsk_` and has no extra spaces
3. Delete the key from `config.json`, restart the app, and paste it in fresh via the setup wizard

If you're still stuck, make sure your internet connection is active — ReachFlow runs locally, but it does need internet access to reach the Groq API.

---

## That's Everything

You're set up and ready to go. Open ReachFlow whenever you need it, fill in your prospect details, and let the AI do the heavy lifting on the first draft.

Happy prospecting.

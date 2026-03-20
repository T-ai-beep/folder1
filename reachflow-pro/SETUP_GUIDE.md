# ReachFlow Pro — Setup Guide

Welcome to **ReachFlow Pro**, your complete AI-powered outreach suite. This guide will get you up and running in about five minutes — no technical experience required.

---

## What Is ReachFlow Pro?

ReachFlow Pro is a desktop app that runs locally on your computer. Open it in your browser and you get six dedicated tools for writing every type of outreach content — cold emails, follow-up sequences, LinkedIn messages, objection responses, subject lines, and opening hooks.

Everything runs on your machine. Your data never leaves your computer, and the AI that powers every tool is completely free to use.

---

## The Six Tools

**Cold Email Generator**
Fill in a few details about yourself and your prospect and get a personalized cold email that sounds like it was written specifically for that person — because it was.

**Follow-up Sequence Builder**
Turn a single outreach thread into a multi-touch sequence. Tell it your offer and the situation, and it writes a complete follow-up chain timed for maximum reply rates.

**LinkedIn Outreach**
Generate connection requests and LinkedIn DMs that don't feel copy-pasted. Short, natural, and calibrated to the platform where people's inboxes are less crowded.

**Objection Crusher**
Paste in an objection you got back ("We already have someone for that" / "Not in the budget right now") and get a confident, non-pushy response that keeps the conversation alive.

**Subject Line Lab**
Enter your email topic and audience and get a batch of subject lines to test — ranging from curiosity-driven to direct to benefit-led. Better subject lines mean more opens.

**Opener Generator**
The first sentence is the hardest part. Feed in what you know about the prospect and get a set of personalized openers you can drop into any email or message.

---

## What You Need

Before you start, make sure you have two things:

**1. Python 3.8 or later**

Python is free software that ReachFlow Pro needs to run. Check if you already have it:

- **Mac:** Open Terminal and type `python3 --version`, then press Enter.
- **Windows:** Open Command Prompt and type `python --version`, then press Enter.

If you see a version number like `3.10.4`, you're good. If not, download Python for free at [python.org/downloads](https://www.python.org/downloads/). During installation on Windows, make sure to check the box that says **"Add Python to PATH"** before clicking Install.

**2. A Free Groq API Key**

Groq provides the AI that powers every tool in ReachFlow Pro. Their free tier gives you 14,400 requests per day — more than enough for any outreach campaign. No credit card is required.

---

## Getting Your Free Groq API Key

1. Go to **[console.groq.com](https://console.groq.com)**
2. Click **Sign Up** and create a free account
3. Once logged in, click **API Keys** in the left sidebar
4. Click **Create API Key**, give it any name (e.g. "ReachFlow Pro"), and click **Submit**
5. Copy the key — it starts with `gsk_`

Keep that key handy. You'll paste it into ReachFlow Pro on first launch.

---

## Running ReachFlow Pro

### Mac

1. Open the **ReachFlow Pro** folder
2. **Double-click `start.command`**
3. A Terminal window will open and your browser will launch automatically at `http://localhost:5001`

> **First time on Mac?** macOS may block the script because it was downloaded from the internet. If nothing happens when you double-click, **right-click `start.command`** and choose **Open**. Click **Open** again in the dialog that appears. You only need to do this once.

### Windows

1. Open the **ReachFlow Pro** folder
2. **Double-click `start.bat`**
3. A command window will open and your browser will launch automatically at `http://localhost:5001`

---

## First Run: The Setup Wizard

The first time ReachFlow Pro starts, it will open a **Setup** page in your browser instead of the main app. This is completely normal.

1. Paste your Groq API key (the one starting with `gsk_`) into the field
2. Click **Save and Continue**
3. ReachFlow Pro verifies the key and takes you straight to the main dashboard

Your key is saved locally in a file called `config.json` inside the ReachFlow Pro folder. You will never need to enter it again.

---

## Using the Tools

Once you're on the main dashboard:

1. Click the tool you want from the navigation
2. Fill in the fields for that tool — the labels tell you exactly what goes where
3. Click **Generate**
4. Your content streams in word by word, just like a live response
5. Copy it, paste it wherever you need it, and go

Every tool is independent. You can use them in any order, as many times as you like.

---

## Tips for Great Outreach

The more detail you give, the better the output. A few habits that make a real difference across all six tools:

- **Be specific about the prospect.** Instead of "they run an agency," try "they run a 15-person performance marketing agency focused on e-commerce brands." Specificity produces specificity.
- **Describe your offer in outcome terms.** Don't say what you do — say what the other person gets. "I save e-commerce brands an average of 12 hours a week on customer support" is stronger than "I do customer support automation."
- **Use the Opener Generator first.** If you're crafting a cold email from scratch, start there. A strong opener makes everything else easier to write.
- **Let the Follow-up Sequence Builder do the heavy lifting.** Most replies come from follow-ups, not first emails. Build the full sequence upfront so you're not scrambling to write it later.
- **Test subject lines before you commit.** Run three or four through the Subject Line Lab and pick the one that makes you most curious to open — that's usually the winner.
- **Regenerate freely.** Each run produces a different result. If the first version isn't quite right, hit Generate again or tweak a field and try once more.

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

### "Port 5001 is already in use"

Another application is using the same network port. Try these steps:

- Close any other browser tabs or apps that might be running a local server
- Wait 30 seconds and run `start.command` / `start.bat` again
- If the problem persists, restart your computer and try again before opening anything else

### "The app opened but content isn't generating"

This is almost always an API key issue. Check the following:

1. Log in to [console.groq.com](https://console.groq.com) and confirm your API key is active
2. Open the `config.json` file inside the ReachFlow Pro folder and confirm the key starts with `gsk_` and has no extra spaces
3. Delete the key from `config.json`, restart the app, and paste it in fresh via the setup wizard

If you're still stuck, make sure your internet connection is active — ReachFlow Pro runs locally, but it does need internet access to reach the Groq API.

---

## That's Everything

You're set up and ready to go. Open ReachFlow Pro whenever you need it, pick a tool, fill in the fields, and let the AI do the heavy lifting.

Happy prospecting.

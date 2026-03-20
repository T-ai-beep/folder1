# Cold Email Generator — Setup Guide

Welcome! This guide walks you through everything you need to get the Cold Email Generator running — even if you have never written a line of code. Take it one step at a time and you will be generating professional cold emails in under 20 minutes.

---

## What Is This Tool?

The Cold Email Generator is a web app that runs on your computer (or optionally on the internet as a real website). You open it in your browser, fill in a simple form, click a button, and get **3 ready-to-send cold email variations** written by Claude AI.

Each email includes:
- A punchy subject line
- A personalized opening
- A clear call to action
- Under 150 words — short enough that people actually read it

**What you get in the download:**
- `app.py` — the Python backend
- `templates/index.html` — the web interface
- `requirements.txt` — the list of Python packages needed
- This setup guide

---

## Prerequisites

You need three things before starting. Do not skip this section.

### 1. Python 3.8 or newer

Python is the programming language this app runs on. Check if you already have it:

Open **Terminal** (Mac: press `Cmd + Space`, type "Terminal", press Enter) or **Command Prompt** (Windows: press `Win + R`, type "cmd", press Enter), then type:

```
python --version
```

If you see something like `Python 3.11.2`, you are good. If you see an error or a version starting with `2.`, you need to install Python.

**To install Python:** Go to [https://www.python.org/downloads](https://www.python.org/downloads) and click the big yellow "Download Python" button. Run the installer. On Windows, make sure to check the box that says **"Add Python to PATH"** before clicking Install.

### 2. pip (Python's package installer)

pip usually comes with Python automatically. Check it with:

```
pip --version
```

If you see a version number, you are ready. If not, try `pip3 --version`. If neither works, reinstall Python from the link above.

### 3. An Anthropic API Key

This is what connects the app to Claude AI. Here is how to get one:

1. Go to [https://console.anthropic.com](https://console.anthropic.com)
2. Click **"Sign Up"** and create a free account (just an email and password)
3. Once logged in, look for **"API Keys"** in the left sidebar and click it
4. Click the **"Create Key"** button
5. Give your key a name (anything works, e.g. "cold-email-tool")
6. Your key will appear on screen — it looks like this: `sk-ant-api03-...`
7. **Copy it immediately and save it somewhere safe** (a notes app, a text file). You will not be able to see the full key again after you leave this page.

> **Cost:** Anthropic charges roughly **$0.003 per email generation** (that is less than half a cent). Generating 100 batches of 3 emails costs around $0.30. You will need to add a payment method in the Anthropic console, but there is a free trial credit when you sign up.

---

## Local Setup (Step by Step)

### Step 1: Get the files into a folder

Unzip the download. You should have a folder called `cold-email-generator` with these files inside:

```
cold-email-generator/
  app.py
  requirements.txt
  templates/
    index.html
```

Move this folder somewhere easy to find, like your Desktop or Documents.

### Step 2: Open Terminal in that folder

**Mac:**
1. Open Terminal
2. Type `cd ` (with a space after it), then drag and drop the `cold-email-generator` folder from Finder into the Terminal window — it will paste the path automatically
3. Press Enter

**Windows:**
1. Open the `cold-email-generator` folder in File Explorer
2. Click the address bar at the top (where it shows the folder path)
3. Type `cmd` and press Enter — this opens Command Prompt directly in that folder

You should now see a prompt ending with something like `cold-email-generator %` or `cold-email-generator>`.

### Step 3: Create your `.env` file

The app reads your API key from a file called `.env`. Create it now:

**Mac/Linux:** In Terminal, type:
```
touch .env
open -e .env
```
This creates the file and opens it in TextEdit.

**Windows:** In Command Prompt, type:
```
copy NUL .env
notepad .env
```

In the text editor, type exactly this (replace the placeholder with your real key):

```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

Save and close the file. There should be no spaces around the `=` sign.

### Step 4: Install the required packages

In your Terminal/Command Prompt (still in the project folder), run:

```
pip install -r requirements.txt
```

You will see a bunch of text scroll by as packages download. Wait for it to finish. If `pip` does not work, try `pip3 install -r requirements.txt`.

### Step 5: Run the app

```
python app.py
```

Or if that does not work:
```
python3 app.py
```

You should see a message like:
```
Cold Email Generator running at http://localhost:5000
```

### Step 6: Open it in your browser

Open any web browser (Chrome, Firefox, Safari) and go to:

```
http://localhost:5000
```

The app will load. You are ready to generate cold emails.

> To stop the app, go back to Terminal and press `Ctrl + C`.

---

## How to Use the App

The form has three sections.

### About You

| Field | What to enter | Example |
|---|---|---|
| **Your Name** | Your first and last name | `Alex Johnson` |
| **Your Service / Offer** | What you are selling or offering | `Freelance web design` |
| **Your Value Proposition** | The result or benefit you deliver | `I help local businesses get 2x more leads with modern websites` |

**Tip for Value Proposition:** Do not describe what you do — describe what the client *gets*. Instead of "I build websites," write "I help restaurants get more reservations through their website."

### About Your Target

| Field | What to enter | Example |
|---|---|---|
| **Their Name** | The person you are emailing | `Sarah Lee` |
| **Their Company** | The name of their business | `Bloom Bakery` |
| **Why You're Reaching Out** | Their specific problem or pain point | `Their website looks outdated and has no contact form or online ordering` |

**Tip:** The more specific the pain point, the better the email. Look at their website or social media before filling this in.

### Options

| Field | What to enter |
|---|---|
| **Tone** | Choose from: Professional, Casual & Friendly, Direct & Bold, or Warm & Conversational |
| **Number of Variations** | How many email versions to generate (1, 2, or 3) |

Click **Generate Emails** and wait about 5–10 seconds. Three email variations will appear below the form, each with a **Copy** button.

---

## Option A: Run Locally (Personal Use)

If you just want to use this tool yourself on your own computer, you are already done. Every time you want to use it:

1. Open Terminal
2. Navigate to the `cold-email-generator` folder (Step 2 above)
3. Run `python app.py`
4. Open `http://localhost:5000` in your browser
5. When done, press `Ctrl + C` to stop

This is the simplest setup and costs nothing extra.

---

## Option B: Deploy to Railway.app (Make It a Real Website)

Want the app to run 24/7 at a real URL you can open from any device or share with others? Railway.app offers free hosting that is perfect for this.

**What you will need:** A free GitHub account and a free Railway account.

### Step 1: Create a GitHub account

Go to [https://github.com](https://github.com) and sign up for a free account if you do not have one.

### Step 2: Create a new GitHub repository

1. Once logged in, click the **"+"** icon in the top right corner
2. Click **"New repository"**
3. Name it `cold-email-generator`
4. Leave it set to **Public**
5. Do NOT check "Add a README file"
6. Click **"Create repository"**

### Step 3: Push your code to GitHub

GitHub will show you setup instructions. You need to run these commands in your Terminal (inside your `cold-email-generator` folder):

```
git init
git add app.py requirements.txt templates/index.html
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/cold-email-generator.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

> Important: Do NOT run `git add .env` — your `.env` file contains your secret API key and should never be uploaded to GitHub.

### Step 4: Add a Procfile

Railway needs to know how to start your app. Create a file called `Procfile` (no extension) in your project folder with this content:

```
web: python app.py
```

Then also update `app.py` to read the port from Railway's environment. Open `app.py` and find the last line:

```python
app.run(debug=True)
```

Change it to:

```python
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
```

Then commit and push these changes:

```
git add Procfile app.py
git commit -m "Add Railway config"
git push
```

### Step 5: Create a Railway account and deploy

1. Go to [https://railway.app](https://railway.app) and sign up with your GitHub account
2. Click **"New Project"**
3. Click **"Deploy from GitHub repo"**
4. Select your `cold-email-generator` repository
5. Railway will detect it is a Python app and start deploying automatically

### Step 6: Add your API key as an environment variable

Your `.env` file is not on GitHub (good — it is a secret). You need to add the API key directly in Railway:

1. In your Railway project dashboard, click on your service
2. Click the **"Variables"** tab
3. Click **"New Variable"**
4. Set the name to `ANTHROPIC_API_KEY`
5. Set the value to your actual API key (the `sk-ant-api03-...` string)
6. Click **"Add"**

Railway will redeploy automatically.

### Step 7: Get your live URL

1. Click the **"Settings"** tab in your Railway service
2. Look for **"Domains"** — click **"Generate Domain"**
3. Railway gives you a URL like `cold-email-generator-production.up.railway.app`
4. Click it — your app is live on the internet!

---

## Tips for Getting the Best Emails

The quality of the output depends heavily on the quality of your inputs. Here is what works:

**Be specific about their pain point.** Vague: "Their website is bad." Specific: "Their website has no mobile version and loads in 8 seconds — I checked on GTmetrix."

**Make your value proposition outcome-focused.** "I design websites" is weak. "I build websites that convert visitors into paying customers, typically within 3 weeks" is strong.

**Match tone to context.** Use "Professional" for corporate or B2B targets. Use "Casual & Friendly" for small business owners or creators. Use "Direct & Bold" if you want a no-nonsense pitch.

**Try all 3 variations.** Read each one and pick the one that sounds most like you. Tweak a word or two if needed — these are starting points, not final drafts.

**Do some research first.** Spend 2 minutes looking at the person's LinkedIn or website before generating. The more real detail you put in the pain point field, the more personal the email feels.

---

## How to Use This Tool to Make Money

The simplest way to profit from this tool is to use it yourself to land freelance clients.

**The basic playbook:**

1. Pick one service you can offer (web design, copywriting, social media management, video editing, bookkeeping, etc.)
2. Find 20–30 small local businesses in your city with an obvious problem (bad website, no social presence, no reviews, etc.)
3. Find the owner's email (often on their website, Google Maps listing, or LinkedIn)
4. Use this tool to generate 3 email variations for each person
5. Pick the best one, tweak it slightly to add one personal detail, and send it
6. Follow up once after 4–5 days if no reply

**Realistic expectations:** A well-targeted cold email campaign to 50 local businesses might get 5–10 replies and 1–3 clients. One client paying $500–$2,000 for a project makes the whole effort worthwhile.

**What makes this tool valuable:** Writing cold emails manually is slow and painful. This tool lets you go from "found a lead" to "email ready to send" in under 60 seconds.

---

## Troubleshooting

### "Missing ANTHROPIC_API_KEY" error when starting the app

Your `.env` file is either missing, in the wrong folder, or has a typo. Make sure:
- The file is named exactly `.env` (not `.env.txt` or `env`)
- It is in the same folder as `app.py`
- It contains exactly: `ANTHROPIC_API_KEY=your-key-here` with no spaces around the `=`

On Mac, files starting with `.` are hidden by default. In Finder, press `Cmd + Shift + .` to show hidden files.

### "Port 5000 is already in use"

Something else is already running on port 5000 (often another Python app or AirPlay on Mac). Fix it by either:
- Stopping the other app
- Or changing the port: open `app.py`, find `app.run(debug=True)` and change it to `app.run(debug=True, port=5001)`, then go to `http://localhost:5001`

### "pip not found" or "python not found"

Python did not get added to your system PATH during installation. The quickest fix:
- On Windows: uninstall Python and reinstall it, making sure to check "Add Python to PATH"
- On Mac: try using `python3` and `pip3` instead of `python` and `pip`

### The app loads but "Generate Emails" returns an error

Check the Terminal window where you ran `python app.py` — it will show the exact error message. The most common causes:
- Invalid or expired API key
- No payment method on your Anthropic account (add one at console.anthropic.com)
- No internet connection

### The app worked before but now says "Something went wrong"

Your API key may have been deleted or expired. Log in to [console.anthropic.com](https://console.anthropic.com), go to API Keys, and confirm your key is still active. If not, create a new one and update your `.env` file.

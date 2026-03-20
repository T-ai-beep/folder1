# How to Sell ReachFlow — Complete Guide

Delete this entire setup-for-sale/ folder once you've launched.

---

## Step 1 — Package the files (1 minute)

Run this once from Terminal:

```bash
bash ~/setup-for-sale/package.sh
```

This creates two clean ZIP files in `setup-for-sale/dist/`:
- `ReachFlow.zip` — the basic cold email tool ($12)
- `ReachFlowPro.zip` — the 6-tool outreach suite ($25)

---

## Step 2 — Set up Gumroad (15 minutes)

1. Go to **gumroad.com** → Create account (free)
2. Click **"New Product"** → choose **"Digital product"**
3. Give it a name, upload the ZIP, set the price
4. Repeat for the second product

**Gumroad's cut:** 10% flat fee per sale. No monthly charge.
They handle all payment processing, VAT collection, and payouts.

---

## Step 3 — Fill in the product listings

Copy from `cold-email-generator/GUMROAD_LISTING.md`.

**ReachFlow (basic) — suggested price: $12**
- Upload: `ReachFlow.zip`

**ReachFlow Pro (suite) — suggested price: $25**
- Title: "ReachFlow Pro — 6-Tool Outreach Suite (Cold Email, LinkedIn, Objections & More)"
- Features: Cold Email, Follow-up Sequences, LinkedIn Outreach, Objection Crusher, Subject Line Lab, Opener Generator
- Same format as the basic listing but emphasize the suite angle

**Tip:** Gumroad lets you set a "suggested price" with "pay what you want" — useful early on to get reviews.

---

## Step 4 — Set a refund policy

Gumroad default is 30 days. Keep it. Digital product refunds are rare if the product works as described. Honoring them builds trust.

---

## Step 5 — Publish and get your links

Hit Publish. Gumroad gives you a link like:
`https://yourname.gumroad.com/l/reachflow`

Share that link everywhere.

---

## Step 6 — Get your first sales

**Fastest paths to $100:**

**Reddit** (free, works fast):
- r/entrepreneur — "I built a cold email generator that runs locally for free. Here's what I learned."
- r/SideProject — "Launched my first paid tool: AI cold email generator using Groq (free API)"
- r/freelance — "Tool I built to write cold emails for my own clients, now selling it"
- DO NOT post "buy my thing" — post value, mention the product at the end

**Twitter/X:**
- Post a short video of the tool generating an email in real time (streaming looks impressive)
- Tag it #buildinpublic #indiedev #solopreneur

**Product Hunt:**
- Best for a bigger push. Submit at midnight PST on a Tuesday/Wednesday for max exposure.
- Prepare: a tagline, 3 screenshots (or a GIF), and a short video

**Use it yourself:**
- Generate cold emails for your own freelance outreach
- When you land a client, mention "I used this tool to write the email" — natural marketing

---

## Things You Must Know Before Selling

### What buyers need (the "system requirements")
Buyers need Python 3.8+ installed. This is NOT pre-installed on most Windows machines. Your setup guide covers it, but expect some support requests about this.

**Most common support question:** "I double-clicked start.command and nothing happened."
**Answer:** On Mac, right-click → Open (the first time), because macOS blocks downloaded apps.

**Second most common:** "pip is not recognized" on Windows.
**Answer:** Reinstall Python and check "Add Python to PATH" during install.

### The Groq free API
Each buyer gets their own free Groq key at console.groq.com. Free tier: 14,400 requests/day. This is effectively unlimited for personal use.

**Risk:** If Groq changes their pricing or shuts down the free tier, buyers would need to switch to a paid Groq plan or a different provider. The code is easy to update (change the model name and Groq client to another OpenAI-compatible provider). This is a low risk — Groq is well-funded and the free tier is their growth strategy.

### Pricing strategy
- Launch at lower prices to get the first 5–10 reviews fast
- Example: $7 for ReachFlow, $15 for Pro for the first week
- Then raise to $12 / $25
- You can always raise prices. You can't easily lower them without annoying existing buyers.

### Protecting the code
The current build uses Python source files. To protect it:
1. Run `python build.py` in either app folder
2. Distribute the compiled `dist/` folder (no Python files visible)
3. See `OBFUSCATION_GUIDE.md` for details

### Taxes
Gumroad collects and remits sales tax (VAT/GST) for most countries automatically. You're responsible for income tax on your revenue. Keep records.

### Licensing / terms
You don't technically need terms of service for a basic Gumroad product, but it helps to include one sentence in the product description:

> "Personal use license. Do not resell or redistribute."

### What to do when buyers report bugs
- Groq API errors: usually rate limits or expired keys — tell them to check their Groq dashboard
- "Nothing happens when I click Generate" — usually a CORS or server error, ask them to open the browser console and share the error
- Python/pip errors — covered in the setup guide troubleshooting section

### Scaling up later
If you get traction:
1. Host it online (Railway or Render) and sell subscriptions via Stripe
2. Add user accounts so people don't need to manage their own API key
3. Build a team feature (multiple users per account)
4. Partner with outreach-heavy communities (sales, recruiting, agency owners)

---

## File structure (what's in each ZIP)

```
ReachFlow/
├── app.py              ← Flask server
├── license.py          ← License check (returns True for now)
├── requirements.txt    ← flask, groq
├── start.bat           ← Windows double-click launcher
├── start.command       ← Mac double-click launcher
├── SETUP_GUIDE.md      ← Step-by-step setup for buyers
└── templates/
    ├── setup.html      ← First-run API key wizard
    └── index.html      ← Main app UI
```

ReachFlowPro/ — same structure, 6 streaming endpoints in app.py.

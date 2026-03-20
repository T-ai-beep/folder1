# ReachFlow — Project Briefing

Use this to resume the project in any Claude session.

---

## What This Is

Two paid digital products built to sell on Gumroad. Both are local Python/Flask apps that use the **Groq API (free tier)** to generate cold email and outreach content. Buyers download a ZIP, double-click a launcher, and the app opens in their browser. Zero ongoing API cost for buyers — they get their own free Groq key at console.groq.com.

---

## Products

### ReachFlow — $12
- **Folder:** `~/cold-email-generator/`
- **Port:** 5000
- **Tool:** Cold email generator (1–5 variations, 4 tones: Professional / Casual / Direct / Warm)
- **Run:** `bash ~/run.sh`

### ReachFlow Pro — $25
- **Folder:** `~/reachflow-pro/`
- **Port:** 5001
- **Tools (6):** Cold Email, Follow-up Sequence, LinkedIn Outreach, Objection Crusher, Subject Line Lab, Opener Generator
- **Run:** `bash ~/run.sh pro`

---

## File Structure (both apps, same pattern)

```
app.py                  ← Flask server, Groq SSE streaming
license.py              ← Stub: check_license() returns True
requirements.txt        ← flask, groq
start.bat               ← Windows double-click launcher
start.command           ← Mac double-click launcher
templates/
  setup.html            ← First-run API key wizard (/setup route)
  index.html            ← Main app UI
SETUP_GUIDE.md          ← Buyer-facing setup instructions (Groq-based)
GUMROAD_LISTING.md      ← Ready-to-paste Gumroad product listing
.gitignore              ← Excludes config.json, __pycache__, dist/
build.py                ← PyInstaller packaging (for obfuscation later)
```

**config.json** is created on first run when buyer saves their Groq key. Never committed.

---

## How It Works

1. Buyer double-clicks `start.command` (Mac) or `start.bat` (Windows)
2. Flask starts, browser opens automatically
3. On first run: redirects to `/setup` — buyer pastes their free Groq key (starts with `gsk_`)
4. Key saved to `config.json` — never asked again
5. Main UI loads — fill form, click Generate, emails stream in real time word-by-word

---

## Tech Stack

- **Backend:** Python 3.8+, Flask, Groq Python SDK
- **AI model:** `llama-3.3-70b-versatile` via Groq (free tier: 14,400 req/day)
- **Streaming:** Server-Sent Events (SSE) via Flask `stream_with_context`
- **Frontend:** Vanilla HTML/CSS/JS, Inter font, localStorage persistence
- **No database, no auth, no cloud — runs entirely on buyer's machine**

---

## Packaging & Selling

```bash
# Create the ZIPs (run once before uploading to Gumroad)
bash ~/setup-for-sale/package.sh
# → creates: ~/setup-for-sale/dist/ReachFlow.zip
# → creates: ~/setup-for-sale/dist/ReachFlowPro.zip

# Delete this folder after uploading:
rm -rf ~/setup-for-sale/
```

**Gumroad:** gumroad.com — 10% flat fee, handles VAT/payments/payouts
**Pricing strategy:** Launch at $7/$15 for first 5–10 reviews, then raise to $12/$25

---

## UI Details

- **Layout:** Dark sidebar (form inputs) + light main panel (output cards)
- **Color:** Purple brand (`#7c3aed`), dark sidebar (`#0d0d10` basic / `#0c0c0f` pro)
- **Font:** Inter (Google Fonts)
- **Features:** Streaming output, localStorage persistence, ⌘+Enter shortcut, Copy buttons, Copy All, tab title updates during generation, purple lightning bolt favicon
- **Basic app sidebar fields:**
  - Your name
  - What you sell
  - What do they get?
  - Their name / Company (side by side)
  - Why you're reaching out
  - Tone selector (Professional / Casual / Direct / Warm)
  - Variations stepper (1–5)

---

## Prompt Quality

Prompts are structured to produce **full 120–180 word professional emails** with:
1. Subject line (`Subject: ...`)
2. Greeting (`Hi [Name],`)
3. Personalized opening referencing their specific business
4. 2–3 sentences on their problem + your solution
5. Concrete outcome/result
6. Single CTA
7. Sign-off

Emails separated by `---` in output (used to split into individual cards).

---

## What's Already Done

- [x] Both apps fully built and working
- [x] Prompts rewritten for full professional emails
- [x] First-run setup wizard (Groq key validation)
- [x] Streaming SSE output (word-by-word)
- [x] All UI labels polished
- [x] Favicon on all 4 HTML pages
- [x] Tab title updates during generation
- [x] Subject Line Lab: 10 individual cards with type badge + char count
- [x] SETUP_GUIDE.md (Groq-based, no Anthropic refs) in both apps
- [x] GUMROAD_LISTING.md in both apps
- [x] .gitignore in both apps
- [x] Mac + Windows launchers (tested)
- [x] package.sh packaging script (produces clean ZIPs)
- [x] `~/run.sh` for local testing
- [x] Obfuscation-ready: license.py stub + build.py (PyInstaller)
- [x] OBFUSCATION_GUIDE.md at `~/OBFUSCATION_GUIDE.md`

---

## Potential Next Steps

- [ ] Test a real end-to-end generation with the new prompts
- [ ] Set up Gumroad listings and upload ZIPs
- [ ] Run `package.sh` and verify ZIP contents
- [ ] Optionally obfuscate with PyArmor before selling (see OBFUSCATION_GUIDE.md)
- [ ] Launch marketing: Reddit posts, Twitter/X, Product Hunt

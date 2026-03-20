"""
ReachFlow Pro — Multi-tool outreach suite
Powered by Groq (free tier). Run with: python app.py
"""
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, redirect
from groq import Groq
import os, json, threading, webbrowser, time, sys
import urllib.request
from html.parser import HTMLParser
app = Flask(__name__)
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# ── License ───────────────────────────────────────────────────────────────────
from license import check_license
if not check_license():
    print("\n  ✗ License invalid. Please contact support.\n")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(data):
    cfg = load_config()
    cfg.update(data)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def get_api_key():
    return load_config().get("groq_api_key") or os.getenv("GROQ_API_KEY", "")

def make_client():
    key = get_api_key()
    return Groq(api_key=key) if key else None

# ── Shared streaming helper ───────────────────────────────────────────────────
def streamed(prompt, temperature=0.75):
    """Generator: yields SSE data lines from Groq streaming."""
    client = make_client()
    if not client:
        yield f"data: {json.dumps({'error': 'No API key configured.'})}\n\n"
        return
    try:
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=temperature,
            stream=True,
        )
        for chunk in stream:
            text = chunk.choices[0].delta.content or ""
            if text:
                yield f"data: {json.dumps({'t': text})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

def sse_response(prompt, temperature=0.75):
    return Response(
        stream_with_context(streamed(prompt, temperature)),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

def require_fields(data, *fields):
    """Returns cleaned dict or raises ValueError."""
    out = {}
    for f in fields:
        val = data.get(f, "").strip()
        if not val:
            raise ValueError(f"Field '{f}' is required.")
        out[f] = val
    return out

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if not get_api_key():
        return redirect("/setup")
    return render_template("index.html")

@app.route("/setup", methods=["GET"])
def setup():
    return render_template("setup.html")

@app.route("/setup", methods=["POST"])
def setup_save():
    key = (request.json or {}).get("key", "").strip()
    if not key or not key.startswith("gsk_"):
        return jsonify({"error": "That doesn't look like a valid Groq key (should start with gsk_)."}), 400
    try:
        client = Groq(api_key=key)
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5,
        )
    except Exception:
        return jsonify({"error": "Key is invalid or couldn't connect. Please check and try again."}), 400
    save_config({"groq_api_key": key})
    return jsonify({"ok": True})

@app.route("/reset")
def reset():
    save_config({"groq_api_key": ""})
    return redirect("/setup")

# ── Tool: Reply Handler ───────────────────────────────────────────────────────
@app.route("/stream/reply", methods=["POST"])
def stream_reply():
    d = request.json or {}
    try:
        v = require_fields(d, "original_email", "their_reply", "your_service")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    prompt = f"""Someone responded to my cold email. Write 3 reply options.

MY ORIGINAL EMAIL:
{v['original_email']}

THEIR REPLY:
{v['their_reply']}

WHAT I SELL: {v['your_service']}

Analyze their reply tone — are they interested, skeptical, objecting, or just asking a question? Then write 3 different responses:

REPLY 1 — Direct and confident
REPLY 2 — Soft and consultative  
REPLY 3 — Bold and assumptive close

Rules:
- Each reply under 100 words
- Never start with "Thank you for your response" or "Great to hear from you"
- Match their energy — if they're brief, be brief
- Each ends with a clear next step
- Ready to copy and send as-is

Separate with ---"""

    return sse_response(prompt, temperature=0.7)

# ── Tool: Cold Email ──────────────────────────────────────────────────────────
@app.route("/stream/email", methods=["POST"])
def stream_email():
    d = request.json or {}
    try:
        v = require_fields(d, "sender_name", "sender_service", "sender_value",
                              "target_name", "target_company", "target_pain")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    num  = min(int(d.get("num_variations", 3)), 5)
    tone = d.get("tone", "professional")

    prompt = f"""Write {num} complete cold email(s). Each must be a full, ready-to-send professional email — not a fragment, not an outline.

SENDER:
- Name: {v['sender_name']}
- What they offer: {v['sender_service']}
- The result clients get: {v['sender_value']}

RECIPIENT:
- Name: {v['target_name']}
- Company: {v['target_company']}
- Why reaching out: {v['target_pain']}

TONE: {tone}

STRUCTURE OF EACH EMAIL:
1. Subject line — format: "Subject: [subject here]"
2. Greeting — "Hi [Name]," or "Hey [Name],"
3. Opening sentence — reference something specific and real about their business
4. 2–3 sentences connecting their problem to your solution
5. One concrete outcome or result they can expect
6. A single clear call to action (book a 15-min call, reply to this email, etc.)
7. Sign-off with the sender's name

LENGTH: 120–180 words per email body (not counting subject line)

NEVER USE:
- "hope this finds you well"
- "I wanted to reach out"
- "my name is"
- "I came across your"
- "I noticed that"
- "Just following up"
- Generic filler openers

Each variation must open from a completely different angle.
Separate emails with a line containing only: ---"""

    return sse_response(prompt)

# ── Tool: Follow-up Sequence ──────────────────────────────────────────────────
@app.route("/stream/sequence", methods=["POST"])
def stream_sequence():
    d = request.json or {}
    try:
        v = require_fields(d, "original_email", "recipient_name", "recipient_company")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    length = min(int(d.get("length", 4)), 6)
    days   = int(d.get("days_between", 3))

    prompt = f"""Create a {length}-email follow-up sequence for someone who didn't respond to this cold email:

--- ORIGINAL EMAIL ---
{v['original_email']}
--- END ORIGINAL ---

RECIPIENT: {v['recipient_name']} at {v['recipient_company']}
DAYS BETWEEN EACH EMAIL: {days}

Rules for the sequence:
- Each email shorter than the last
- Completely different hook/angle — never "just following up" or "bumping this"
- No "I wanted to circle back" or "checking in"
- Each has its own subject line (or "Re: [original subject]" where natural)
- Email {length} is the breakup email: ultra-short, no hard feelings, leaves door open
- Max 80 words per body

Format each email as:
EMAIL [N] — Day [X]:
Subject: ...
[body]
---"""

    return sse_response(prompt)

# ── Tool: LinkedIn Outreach ───────────────────────────────────────────────────
@app.route("/stream/linkedin", methods=["POST"])
def stream_linkedin():
    d = request.json or {}
    try:
        v = require_fields(d, "your_name", "your_role", "target_name", "target_context", "goal")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    prompt = f"""Write a LinkedIn connection request and 2 follow-up DMs.

MY INFO:
- Name: {v['your_name']}
- What I do: {v['your_role']}

THEIR INFO:
- Name: {v['target_name']}
- Context: {v['target_context']}

MY GOAL: {v['goal']}

CONNECTION REQUEST:
- MUST be under 290 characters (LinkedIn hard limit — count carefully)
- Personal, specific, genuine
- No "I'd like to add you to my network"
- No pitch — just a reason to connect
- After writing it, state the character count in brackets: [X chars]

FOLLOW-UP DM 1 (send 2-3 days after they accept):
- Thank them, add real value or an insight
- Soft question to open conversation
- Under 120 words

FOLLOW-UP DM 2 (send 5 days later if no reply):
- Under 70 words
- Different angle
- Clear, direct ask

Label each section clearly."""

    return sse_response(prompt)

# ── Tool: Objection Crusher ───────────────────────────────────────────────────
@app.route("/stream/objection", methods=["POST"])
def stream_objection():
    d = request.json or {}
    try:
        v = require_fields(d, "service", "objection")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    context = d.get("context", "").strip()
    context_line = f"Additional context: {context}" if context else ""

    prompt = f"""I'm selling: {v['service']}
The prospect said: "{v['objection']}"
{context_line}

Write 3 ready-to-send responses, each using a different tactic:

RESPONSE 1 — Acknowledge + Reframe
(Validate their concern, then shift perspective)

RESPONSE 2 — Social Proof + Specificity
(Use a real-sounding example or result to neutralize the objection)

RESPONSE 3 — Challenge + Flip
(Politely challenge the assumption behind the objection)

Rules:
- Each response under 100 words
- Ready to copy and send/say as-is
- No hollow phrases like "I totally understand your concern"
- Confident, not defensive
- Each ends with a forward-moving question or next step

Separate with ---"""

    return sse_response(prompt, temperature=0.7)

# ── Tool: Subject Line Lab ────────────────────────────────────────────────────
@app.route("/stream/subjects", methods=["POST"])
def stream_subjects():
    d = request.json or {}
    try:
        v = require_fields(d, "purpose", "audience", "service")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    prompt = f"""Generate 10 email subject lines.

Email purpose: {v['purpose']}
Target audience: {v['audience']}
Product/service: {v['service']}

Write exactly 2 subject lines of each type:
1. CURIOSITY — makes them stop and wonder
2. DIRECT BENEFIT — clearly states what they get
3. PERSONALIZED — feels written just for them
4. QUESTION — challenges an assumption they hold
5. PATTERN INTERRUPT — unexpected phrasing that breaks the scroll

Rules:
- Under 52 characters each (fits all email clients without cutting off)
- No spam words: free, guaranteed, act now, limited time, click here
- No emojis
- No question marks on non-question types
- Label each with its TYPE

Format: numbered 1-10, with [TYPE] tag on each line."""

    return sse_response(prompt, temperature=0.8)

# ── Tool: Opener Generator ────────────────────────────────────────────────────
@app.route("/stream/opener", methods=["POST"])
def stream_opener():
    d = request.json or {}
    try:
        v = require_fields(d, "target_name", "context")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    prompt = f"""Write 5 personalized email opening lines for {v['target_name']}.

What I know about them:
{v['context']}

Rules:
- Each opener is ONLY the first 1-2 sentences — just the hook
- Must reference something SPECIFIC from the context above
- Sound like genuine research, not flattery
- Each takes a completely different angle
- Flows naturally into a pitch (but don't pitch yet)
- No "I came across your profile", "I noticed your website", "I saw on LinkedIn"
- No starting with "I" on the first word

5 openers, numbered. Nothing else."""

    return sse_response(prompt, temperature=0.85)


# ── Tool: URL Scraper ─────────────────────────────────────────────────────────
@app.route("/scrape", methods=["POST"])
def scrape():
    url = (request.json or {}).get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided."}), 400

    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw_bytes = resp.read()
            try:
                import gzip
                raw = gzip.decompress(raw_bytes).decode("utf-8", errors="ignore")
            except Exception:
                raw = raw_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        return jsonify({"error": f"Could not fetch that URL: {str(e)}"}), 400

    import re
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()[:3000]
    print(f"DEBUG extracted text length: {len(text)}")
    print(f"DEBUG first 200 chars: {text[:200]}")

    client = make_client()
    if not client:
        return jsonify({"error": "No API key configured."}), 401

    try:
        result = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""Extract the following from this webpage text. Return ONLY valid JSON, nothing else.

{{
  "company": "company name or empty string",
  "what_they_do": "one sentence description or empty string",
  "pain_points": "likely business pain points based on their industry and content or empty string",
  "contact_name": "person's name if found or empty string"
}}

Webpage text:
{text}"""}],
            max_tokens=300,
            temperature=0.2,
        )
        import json as _json
        # Safely extract message content (model may return None)
        content = None
        try:
            content = getattr(result.choices[0].message, "content", None)
        except Exception:
            # If structure is unexpected, attempt direct access then fallback to None
            try:
                content = result.choices[0].message.content
                print(f"DEBUG scrape response: '{content}'")

            except Exception:
                content = None
        if not content:
            raise ValueError("Model returned empty content.")
        extracted = _json.loads(content.strip())
        return jsonify({"ok": True, "data": extracted})
    except Exception as e:
        return jsonify({"error": f"Could not extract data: {str(e)}"}), 400
    # ── Tool: A/B Subject Tester ──────────────────────────────────────────────────
@app.route("/stream/abtester", methods=["POST"])
def stream_abtester():
    d = request.json or {}
    try:
        v = require_fields(d, "email_body", "audience", "goal")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    prompt = f"""You are an email marketing expert. Analyze this email and write 2 subject line variations optimized for different psychological angles.

EMAIL BODY:
{v['email_body']}

TARGET AUDIENCE: {v['audience']}
GOAL: {v['goal']}

Write exactly this format:

VERSION A — [psychological angle name]
Subject: [subject line]
Why it works: [2 sentences explaining the psychology behind it and why this audience would open it]
Best for: [type of prospect most likely to respond]

---

VERSION B — [psychological angle name]
Subject: [subject line]
Why it works: [2 sentences explaining the psychology behind it and why this audience would open it]
Best for: [type of prospect most likely to respond]

Rules:
- Both under 52 characters
- No spam words
- No emojis
- Completely different psychological angles — not just rewordings of each other
- Be specific about why each works for THIS audience"""

    return sse_response(prompt, temperature=0.75)
# ── Tool: Company Research (Tavily) ──────────────────────────────────────────
import itertools
from dotenv import load_dotenv
load_dotenv()

_tavily_keys = [k for k in [
    os.getenv("TAVILY_KEY_1"),
    os.getenv("TAVILY_KEY_2"),
    os.getenv("TAVILY_KEY_3"),
] if k]
_tavily_cycle = itertools.cycle(_tavily_keys) if _tavily_keys else None

@app.route("/research", methods=["POST"])
def research():
    if not _tavily_cycle:
        return jsonify({"error": "No Tavily API keys configured."}), 400

    query = (request.json or {}).get("query", "").strip()
    if not query:
        return jsonify({"error": "No search query provided."}), 400

    last_error = None
    for _ in range(len(_tavily_keys)):
        key = next(_tavily_cycle)
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=key)
            results = client.search(
                query=f"{query} company about contact team",
                max_results=5,
                search_depth="basic",
            )
            combined = "\n\n".join(
                r.get("content", "") for r in results.get("results", [])
            )[:3000]
            break
        except Exception as e:
            last_error = str(e)
            combined = None

    if not combined:
        return jsonify({"error": f"Search failed: {last_error}"}), 400

    groq_client = make_client()
    if not groq_client:
        return jsonify({"error": "No Groq API key configured."}), 401

    try:
        result = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""Extract the following from these search results. Return ONLY valid JSON, nothing else.

{{
  "company": "company name or empty string",
  "what_they_do": "one sentence description or empty string",
  "pain_points": "likely business pain points based on their industry or empty string",
  "contact_name": "owner or key person's name if found or empty string"
}}

Search results:
{combined}"""}],
            max_tokens=300,
            temperature=0.2,
        )
        import json as _json
        import re as _re
        # Safely extract message content (model may return None)
        content = None
        try:
            content = getattr(result.choices[0].message, "content", None)
        except Exception:
            # If structure is unexpected, attempt direct access then fallback to None
            try:
                content = result.choices[0].message.content
            except Exception:
                content = None
        if not content:
            return jsonify({"error": "Could not extract data from search results."}), 400
        content = content.strip()
        content = _re.sub(r"^```json\s*", "", content)
        content = _re.sub(r"^```\s*", "", content)
        content = _re.sub(r"\s*```$", "", content).strip()
        if not content:
            return jsonify({"error": "Could not extract data from search results."}), 400
        extracted = _json.loads(content)
        return jsonify({"ok": True, "data": extracted})
    except Exception as e:
        return jsonify({"error": f"Could not extract data: {str(e)}"}), 400
# ── Tool: Email Audit ─────────────────────────────────────────────────────────
@app.route("/stream/audit", methods=["POST"])
def stream_audit():
    d = request.json or {}
    try:
        v = require_fields(d, "email")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    prompt = f"""You are a cold email expert. Audit this cold email ruthlessly.

EMAIL:
{v['email']}

Score it on each dimension from 1-10 and explain exactly what's wrong and how to fix it:

SUBJECT LINE — /10
Score, what works or doesn't, specific fix

OPENING LINE — /10
Score, what works or doesn't, specific fix

PITCH — /10
Score, is the value clear, is it about them or about you, specific fix

CALL TO ACTION — /10
Score, is it clear, is it low friction, specific fix

LENGTH & TONE — /10
Score, too long/short, tone match, specific fix

OVERALL SCORE — /10
One paragraph verdict

REWRITTEN VERSION:
Rewrite the entire email fixing every issue identified above. Make it significantly better.

Be brutal. Most cold emails are bad. Don't sugarcoat."""

    return sse_response(prompt, temperature=0.5)
# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))

    def open_browser():
        time.sleep(1.2)
        webbrowser.open(f"http://localhost:{port}")

    threading.Thread(target=open_browser, daemon=True).start()
    print(f"\n  ReachFlow Pro → http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port)

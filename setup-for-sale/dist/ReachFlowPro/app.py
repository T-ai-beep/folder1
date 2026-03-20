"""
ReachFlow Pro — Multi-tool outreach suite
Powered by Groq (free tier). Run with: python app.py
"""
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, redirect
from groq import Groq
import os, json, threading, webbrowser, time, sys

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

    prompt = f"""Write {num} cold email variation(s).

FROM:
- Name: {v['sender_name']}
- Service: {v['sender_service']}
- Value delivered: {v['sender_value']}

TO:
- Name: {v['target_name']}
- Company: {v['target_company']}
- Why reaching out: {v['target_pain']}

TONE: {tone}

Rules:
- First line: "Subject: ..."
- Body under 130 words
- Personalized opening referencing something specific about THEM
- Exactly one CTA (book a call, reply to chat, etc.)
- Zero filler phrases ("hope this finds you well", "my name is", "I wanted to reach out")
- Human, not AI-sounding

Separate each email with exactly: ---"""

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

# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))

    def open_browser():
        time.sleep(1.2)
        webbrowser.open(f"http://localhost:{port}")

    threading.Thread(target=open_browser, daemon=True).start()
    print(f"\n  ReachFlow Pro → http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port)

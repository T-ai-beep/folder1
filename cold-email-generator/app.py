from flask import Flask, render_template, request, jsonify, Response, stream_with_context, redirect
from groq import Groq
import os, json, threading, webbrowser, time, sys

app = Flask(__name__)
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

from license import check_license
if not check_license():
    print("\n  ✗ License invalid. Please contact support.\n")
    sys.exit(1)

# ── Config helpers ────────────────────────────────────────────────────────────

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(data):
    cfg = load_config()
    cfg.update(data)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)

def get_api_key():
    return load_config().get("groq_api_key") or os.getenv("GROQ_API_KEY", "")

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
        return jsonify({"error": "That doesn't look like a valid Groq key. It should start with gsk_"}), 400
    # Quick validation: make a tiny API call
    try:
        client = Groq(api_key=key)
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
    except Exception as e:
        return jsonify({"error": "API key is invalid or couldn't connect. Please check and try again."}), 400
    save_config({"groq_api_key": key})
    return jsonify({"ok": True})

@app.route("/reset")
def reset():
    save_config({"groq_api_key": ""})
    return redirect("/setup")

@app.route("/stream", methods=["POST"])
def stream():
    key = get_api_key()
    if not key:
        return jsonify({"error": "No API key configured."}), 401

    data = request.json or {}
    fields = ["sender_name", "sender_service", "sender_value", "target_name", "target_company", "target_pain"]
    vals = {f: data.get(f, "").strip() for f in fields}

    if not all(vals.values()):
        return jsonify({"error": "All fields are required."}), 400

    num = min(int(data.get("num_variations", 3)), 5)
    tone = data.get("tone", "professional")

    prompt = f"""You are writing cold emails on behalf of {vals['sender_name']}.

CONTEXT:
- Sender offers: {vals['sender_service']}
- The result the recipient gets: {vals['sender_value']}
- Recipient name: {vals['target_name']}
- Recipient company: {vals['target_company']}
- Reason for reaching out: {vals['target_pain']}
- Tone: {tone}

Write {num} cold email variation(s). Each must be complete and ready to send.

STRICT RULES — violating any of these makes the email unusable:
- Subject line first, format exactly: Subject: [subject]
- Greeting next: Hi {vals['target_name']}, or Hey {vals['target_name']},
- EMAIL BODY: 75–110 words MAX. Not a word more. Count carefully.
- One paragraph only. No bullet points. No line breaks mid-email.
- First sentence must be about THEM — their business, their situation, their problem. Not about the sender.
- Never mention the sender's name until the sign-off.
- End with one CTA — a question or a specific ask. Not two options.
- Sign off: {vals['sender_name']}

BANNED PHRASES (do not use any of these):
"hope this finds you well", "I wanted to reach out", "my name is", "I came across",
"I noticed that", "as a leading", "in today's competitive", "I am writing to",
"just following up", "touching base", "I believe", "leverage", "synergy",
"innovative solutions", "optimize your", "streamline your"

Each variation must use a completely different opening angle and hook.

Separate each email with exactly: ---"""

    def event_stream():
        try:
            client = Groq(api_key=key)
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.75,
                stream=True,
            )
            for chunk in stream:
                text = chunk.choices[0].delta.content or ""
                if text:
                    yield f"data: {json.dumps({'t': text})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

# ── Launch ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))

    def open_browser():
        time.sleep(1.2)
        webbrowser.open(f"http://localhost:{port}")

    threading.Thread(target=open_browser, daemon=True).start()
    print(f"\n  ReachFlow is running → http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port)
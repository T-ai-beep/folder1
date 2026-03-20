from flask import Flask, render_template, request, jsonify, Response, stream_with_context, redirect
from groq import Groq
import os, json, threading, webbrowser, time

app = Flask(__name__)
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

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

    prompt = f"""Write {num} complete cold email(s). Each must be a full, ready-to-send professional email — not a fragment, not an outline.

SENDER:
- Name: {vals['sender_name']}
- What they offer: {vals['sender_service']}
- The result clients get: {vals['sender_value']}

RECIPIENT:
- Name: {vals['target_name']}
- Company: {vals['target_company']}
- Why reaching out: {vals['target_pain']}

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
- Generic filler openers

Each variation must open from a completely different angle.
Separate emails with a line containing only: ---"""

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

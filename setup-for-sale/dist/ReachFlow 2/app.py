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

    prompt = f"""Write {num} cold email variation(s) for the situation below.

FROM:
- Name: {vals['sender_name']}
- Service: {vals['sender_service']}
- Value: {vals['sender_value']}

TO:
- Name: {vals['target_name']}
- Company: {vals['target_company']}
- Why reaching out: {vals['target_pain']}

TONE: {tone}

Rules:
- First line of each email: "Subject: ..."
- Body under 130 words
- Open with something specific to THEM (not "I came across your company")
- One CTA only (book a call, reply, etc.)
- Zero filler ("hope this finds you well", "my name is", "I wanted to reach out")
- Sound like a real human wrote it, not AI

Separate each email with exactly this on its own line: ---"""

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

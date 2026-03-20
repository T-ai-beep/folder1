# Code Protection & Distribution Guide
## ReachFlow / ReachFlow Pro — Gumroad Products

This guide explains how to protect your Python source code before distributing
your Flask apps to paying customers, and how to evolve the stub `license.py`
into real license enforcement.

---

## 1. Overview of Protection Options

| Tool | What it does | Skill required | Platform support | Source hidden from customer? |
|---|---|---|---|---|
| **PyInstaller** | Bundles Python + dependencies into a native executable folder | Low | Windows, macOS, Linux | Partially — bytecode is bundled but extractable with tools |
| **PyArmor** | Obfuscates Python bytecode before bundling; adds a runtime decryption layer | Medium | Windows, macOS, Linux | Yes — source logic is not recoverable in any practical sense |
| **Nuitka** | Compiles Python to C, then to a native binary | High | Windows, macOS, Linux | Yes — output is true compiled C; very hard to reverse |

### When to use each

- **PyInstaller alone** — good enough for most indie Gumroad products. The
  average customer will not bother to unpack the bundle.  Use `build.py` in
  each project to produce the distributable with one command.

- **PyInstaller + PyArmor** — recommended if you have paying customers who are
  technically sophisticated, or if the core prompt/logic is your primary
  competitive advantage.  Obfuscate first with PyArmor, then bundle with
  PyInstaller.

- **Nuitka** — overkill for most use-cases, but useful if you later move to a
  SaaS offering where performance matters.  Build times are much longer and
  you need a C compiler installed.

---

## 2. Recommended Approach: PyInstaller (what `build.py` does)

Each project ships with a `build.py` that automates the full PyInstaller
workflow.  Running it is the only step needed for a basic distribution-ready
build.

```bash
# In cold-email-generator/ or reachflow-pro/
python build.py
```

After the script finishes you will find:

```
dist/
  ReachFlow/          ← distribute this entire folder (zip it)
    ReachFlow         ← the executable (no extension on macOS/Linux)
    ReachFlow.exe     ← on Windows
    _internal/        ← Python runtime, dependencies, templates
    config.json       ← copied automatically if it existed in the project root
```

**Important:** zip and upload the entire `dist/ReachFlow/` folder to Gumroad,
not just the executable.  The executable relies on files inside `_internal/`.

### Key PyInstaller flags used

| Flag | Reason |
|---|---|
| `--onedir` | Flask's Jinja2 template loader resolves paths relative to the bundle directory; `--onefile` breaks this |
| `--windowed` | Hides the terminal window from the end user on macOS and Windows |
| `--add-data templates`+`os.pathsep`+`templates` | Ensures HTML templates are copied into the bundle; `os.pathsep` is `:` on macOS/Linux and `;` on Windows |
| `--hidden-import` (repeated) | PyInstaller's static analysis misses many Flask/Groq sub-modules; listing them explicitly prevents `ModuleNotFoundError` at runtime |

---

## 3. Adding Source Obfuscation with PyArmor

Do this **before** running `build.py` if you want the strongest protection.

### 3.1 Install PyArmor

```bash
pip install pyarmor
```

### 3.2 Obfuscate the project

Run from the project root (e.g. `cold-email-generator/`):

```bash
# Obfuscate the entire project into a new dist/pyarmor/ folder
pyarmor gen -O dist/pyarmor app.py license.py
```

PyArmor rewrites every `.py` file into an obfuscated form and adds a small
runtime bootstrap.  The obfuscated files have the same module API as the
originals, so nothing else needs to change.

### 3.3 Run PyInstaller on the obfuscated output

```bash
cd dist/pyarmor
python ../../build.py
```

Or, more explicitly, point PyInstaller at the obfuscated `app.py`:

```bash
python -m PyInstaller dist/pyarmor/app.py \
    --name=ReachFlow \
    --onedir \
    --windowed \
    --add-data "dist/pyarmor/templates:templates" \
    --hidden-import flask \
    --hidden-import groq \
    # ... (same hidden imports as build.py)
```

### 3.4 Verify the build

```bash
./dist/ReachFlow/ReachFlow   # macOS/Linux
dist\ReachFlow\ReachFlow.exe  # Windows
```

Open a browser to `http://127.0.0.1:5000` and confirm the app works normally.

---

## 4. How `license.py` Works and How to Activate Real Licensing

### 4.1 Current stub behaviour

Both projects ship an identical `license.py` with two public functions:

```python
get_machine_id() -> str   # SHA-256 of hostname + MAC address
check_license()  -> bool  # always returns True (stub)
```

The `check_license()` stub lets you ship and test the product immediately
without any licensing infrastructure.  Your `app.py` should call it at startup:

```python
from license import check_license
if not check_license():
    print("License invalid. Please purchase a valid license.")
    sys.exit(1)
```

### 4.2 Upgrading to real license enforcement

**Option A — File-based license (simplest)**

1. Generate a license file for each customer.  The file can be as simple as a
   signed JSON blob:

   ```json
   {
     "customer": "Jane Smith",
     "machine_id": "a3f9...",
     "expires": "2027-01-01",
     "signature": "base64encodedHMACorRSAsignature"
   }
   ```

2. In `check_license()`, read `license.json` from the same directory as the
   executable, verify the signature with a public key embedded in the source,
   and compare `machine_id` against `get_machine_id()`.

3. Obfuscate `license.py` with PyArmor so customers cannot inspect the
   verification logic or swap in a fake `license.json`.

**Option B — Server-based license (stronger)**

1. Stand up a lightweight endpoint (even a free Vercel function works):

   ```
   POST https://your-api.vercel.app/api/validate
   Body: { "machine_id": "...", "key": "XXXX-XXXX-XXXX" }
   Response: { "valid": true, "expires": "2027-01-01" }
   ```

2. In `check_license()`, call this endpoint with `httpx` (already a transitive
   dependency through Groq).  Cache the response locally for offline grace
   periods.

3. Obfuscate `license.py` with PyArmor so customers cannot find and bypass the
   HTTP call.

**Option C — PyArmor's built-in licensing (no server needed)**

PyArmor can bake a license directly into the obfuscated bytecode:

```bash
# Generate a license that expires in 365 days and is locked to this machine
pyarmor gen key --expired 365 --bind-device

# Obfuscate with that license embedded
pyarmor gen --with-license dist/pyarmor.rkey app.py license.py
```

The obfuscated runtime will refuse to execute after the expiry date or on a
different machine without any code you have to write.  See the
[PyArmor documentation](https://pyarmor.readthedocs.io/) for full details.

### 4.3 Replacing the stub

Once your real `check_license()` is written and obfuscated:

1. Delete `license.py` from the project root.
2. Copy the PyArmor-obfuscated `license.py` (from `dist/pyarmor/`) into the
   project root.
3. Run `build.py` as normal — it will bundle the obfuscated version.

---

## 5. What NOT to Do

- **Do not distribute the raw project folder.** Customers should receive only
  the zipped `dist/ReachFlow/` or `dist/ReachFlowPro/` folder.

- **Do not commit `config.json` to git.** It contains your (or the customer's)
  Groq API key.  It is already listed in the `.gitignore` recommendations below.

- **Do not commit `dist/` or `build/` to git.** These are large binary
  artifacts that belong in a release, not in source control.

- **Do not distribute `build.py` or `license.py` (unobfuscated) to customers.**
  These are developer tools.  They reveal your build process and, once you add
  real license logic, your validation approach.

- **Do not use `--onefile` with Flask.** Jinja2's template loader cannot find
  templates inside a single-file bundle at runtime.  Always use `--onedir`.

- **Do not rely on Python `compile()` / `.pyc` files alone for protection.**
  Bytecode is trivially decompiled with tools like `decompile3` or `uncompyle6`.
  PyArmor or Nuitka are necessary if source protection matters.

- **Do not store the PyArmor project key in a public repository.** If someone
  has your PyArmor key they can re-obfuscate your source and strip the license
  checks.

---

## 6. Recommended `.gitignore`

Add the following to `.gitignore` in each project root and in this directory:

```gitignore
# Secrets and user configuration — never commit these
config.json
*.env
.env
secrets.json

# PyInstaller build artifacts
dist/
build/
*.spec

# PyArmor output and key material
.pyarmor/
pyarmor.rkey
pyarmor_runtime_*/

# Python bytecode
__pycache__/
*.py[cod]
*.pyo

# macOS metadata
.DS_Store

# Virtual environments
venv/
.venv/
env/
.env/

# IDE files
.vscode/
.idea/
*.swp
```

For the top-level `/Users/aidan/` directory (if you ever initialise a repo
there), also ignore the built products:

```gitignore
cold-email-generator/dist/
cold-email-generator/build/
reachflow-pro/dist/
reachflow-pro/build/
OBFUSCATION_GUIDE.md   # remove this line if you want to track the guide
```

---

## Quick-Reference Checklist Before Each Gumroad Upload

- [ ] Run `python build.py` from the project root
- [ ] Verify the app launches correctly from `dist/ReachFlow/` (or `ReachFlowPro/`)
- [ ] Confirm `config.json` is present in the dist folder (or document that customers must create it)
- [ ] Zip the entire `dist/ReachFlow/` folder — not just the executable
- [ ] Upload the zip to Gumroad
- [ ] Test the download and install flow on a clean machine or VM before publishing

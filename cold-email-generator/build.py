"""
build.py — PyInstaller packaging script for ReachFlow (cold-email-generator)

Usage:
    python build.py

What this script does:
  1. Ensures PyInstaller is installed, installing it if missing.
  2. Removes stale dist/ and build/ directories so the build is clean.
  3. Invokes PyInstaller with the correct flags for a Flask-based app:
       --onedir   : produces a folder (not a single file) so Flask can locate
                    its internal resources at runtime.
       --windowed : suppresses the terminal/console window on Windows and macOS.
  4. Bundles the templates/ folder so Jinja2 can find its HTML files at runtime.
  5. Adds hidden imports for Flask and Groq and their commonly-needed sub-packages
     (PyInstaller's static analysis often misses these).
  6. Copies config.json (if present) into the finished distributable folder so
     the user's API key is available on first launch.

Distribute the entire dist/ReachFlow/ folder to customers — do not distribute
only the executable inside it, as it depends on the other files in that folder.
"""

import os
import shutil
import subprocess
import sys


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
APP_NAME = "ReachFlow"
ENTRY_POINT = "app.py"
TEMPLATES_DIR = "templates"

# Sub-packages that PyInstaller cannot discover through static import analysis.
HIDDEN_IMPORTS = [
    "flask",
    "flask.templating",
    "flask.json",
    "flask.logging",
    "flask.signals",
    "flask.views",
    "flask.wrappers",
    "flask.debughelpers",
    "flask.cli",
    "jinja2",
    "jinja2.ext",
    "jinja2.runtime",
    "werkzeug",
    "werkzeug.serving",
    "werkzeug.middleware.shared_data",
    "werkzeug.debug",
    "click",
    "groq",
    "groq._client",
    "groq._streaming",
    "groq.types",
    "groq.types.chat",
    "httpx",
    "httpcore",
    "anyio",
    "certifi",
    "charset_normalizer",
    "idna",
    "sniffio",
    "distutils",
]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    """Run a subprocess, streaming its output to the terminal."""
    print(f"\n>>> {' '.join(cmd)}\n")
    return subprocess.run(cmd, check=check)


def ensure_pyinstaller() -> None:
    """Install PyInstaller into the current Python environment if absent."""
    try:
        import PyInstaller  # noqa: F401
        print("PyInstaller is already installed.")
    except ImportError:
        print("PyInstaller not found — installing now...")
        run([sys.executable, "-m", "pip", "install", "pyinstaller"])


def clean_previous_build() -> None:
    """Remove dist/ and build/ directories left over from a previous run."""
    for directory in ("dist", "build"):
        if os.path.exists(directory):
            print(f"Removing existing {directory}/...")
            shutil.rmtree(directory)


def build_add_data_arg() -> str:
    """
    Return the correct --add-data argument for the current platform.

    PyInstaller uses ':' as the source:dest separator on macOS/Linux and
    ';' on Windows.  os.pathsep gives us the right character automatically.
    """
    return f"{TEMPLATES_DIR}{os.pathsep}{TEMPLATES_DIR}"


def build_pyinstaller_command() -> list[str]:
    """Assemble the full PyInstaller command."""
    hidden_import_flags: list[str] = []
    for pkg in HIDDEN_IMPORTS:
        hidden_import_flags += ["--hidden-import", pkg]

    return [
        sys.executable,
        "-m",
        "PyInstaller",
        ENTRY_POINT,
        f"--name={APP_NAME}",
        "--onedir",          # Flask needs a folder layout, not a single binary.
        "--windowed",        # No terminal window for the end user.
        "--noconfirm",       # Overwrite output without prompting.
        "--add-data", build_add_data_arg(),
        *hidden_import_flags,
    ]


def copy_config() -> None:
    """
    If config.json exists in the project root, copy it into the distributable
    folder so that the app can find its settings on first launch.
    """
    config_src = "config.json"
    config_dst = os.path.join("dist", APP_NAME, "config.json")

    if os.path.isfile(config_src):
        print(f"Copying {config_src} -> {config_dst}")
        shutil.copy2(config_src, config_dst)
    else:
        print(
            f"Note: {config_src} not found in project root — "
            "skipping copy.  Customers will need to create config.json "
            "manually before first run."
        )


def print_success() -> None:
    dist_path = os.path.abspath(os.path.join("dist", APP_NAME))
    print("\n" + "=" * 60)
    print(f"  BUILD SUCCESSFUL")
    print(f"  Distributable located at:")
    print(f"    {dist_path}")
    print()
    print("  Zip the entire dist/ReachFlow/ folder and upload that")
    print("  archive to Gumroad — do NOT distribute only the executable.")
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    # Make sure we run from the directory that contains this script so that
    # relative paths (templates/, config.json, app.py) resolve correctly.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print(f"Building {APP_NAME}...")
    print(f"Working directory: {script_dir}\n")

    ensure_pyinstaller()
    clean_previous_build()
    run(build_pyinstaller_command())
    copy_config()
    print_success()


if __name__ == "__main__":
    main()

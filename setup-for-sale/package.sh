#!/bin/bash
# ─────────────────────────────────────────────────────────────
# package.sh — Creates clean ZIP files ready for Gumroad upload
# Run once: bash package.sh
# Then upload the two .zip files to Gumroad.
# ─────────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$HOME"
OUT="$SCRIPT_DIR/dist"

mkdir -p "$OUT"

echo ""
echo "  Packaging ReachFlow products..."
echo ""

# ── Helper: clean-copy a folder, excluding junk ──────────────
package_app() {
  local SRC="$1"
  local DEST_NAME="$2"
  local DEST="$OUT/$DEST_NAME"

  rm -rf "$DEST"
  mkdir -p "$DEST/templates"

  # Copy core files
  cp "$SRC/app.py"           "$DEST/"
  cp "$SRC/license.py"       "$DEST/"
  cp "$SRC/requirements.txt" "$DEST/"
  cp "$SRC/start.bat"        "$DEST/"
  cp "$SRC/start.command"    "$DEST/"

  # Copy SETUP_GUIDE if it exists (customer-facing)
  [ -f "$SRC/SETUP_GUIDE.md" ] && cp "$SRC/SETUP_GUIDE.md" "$DEST/"

  # Copy templates
  cp "$SRC/templates/setup.html" "$DEST/templates/"
  cp "$SRC/templates/index.html" "$DEST/templates/"

  # Make the mac launcher executable inside the zip
  chmod +x "$DEST/start.command"

  # Zip it
  cd "$OUT"
  rm -f "${DEST_NAME}.zip"
  zip -r "${DEST_NAME}.zip" "$DEST_NAME" --exclude "*.DS_Store" --exclude "*__pycache__*" --exclude "*.pyc" > /dev/null
  cd "$SCRIPT_DIR"

  local SIZE=$(du -sh "$OUT/${DEST_NAME}.zip" | cut -f1)
  echo "  ✓  $OUT/${DEST_NAME}.zip  ($SIZE)"
}

# ── Package both products ────────────────────────────────────
package_app "$BASE/cold-email-generator" "ReachFlow"
package_app "$BASE/reachflow-pro"        "ReachFlowPro"

echo ""
echo "  Done! Two files ready to upload to Gumroad:"
echo ""
echo "    $OUT/ReachFlow.zip"
echo "    $OUT/ReachFlowPro.zip"
echo ""
echo "  Delete this setup-for-sale/ folder after you've uploaded."
echo ""

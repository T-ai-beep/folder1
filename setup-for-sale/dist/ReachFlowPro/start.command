#!/bin/bash
cd "$(dirname "$0")"
echo ""
echo "  Starting ReachFlow Pro..."
echo ""
pip3 install -r requirements.txt --quiet --disable-pip-version-check 2>/dev/null \
  || pip install -r requirements.txt --quiet --disable-pip-version-check
python3 app.py 2>/dev/null || python app.py

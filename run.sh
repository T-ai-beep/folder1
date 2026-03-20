#!/bin/bash
# ReachFlow local test launcher
# Usage: bash run.sh        → basic app (port 5000)
#        bash run.sh pro    → pro app (port 5001)

if [ "$1" = "pro" ]; then
  DIR="$HOME/reachflow-pro"
  NAME="ReachFlow Pro"
  PORT=5001
else
  DIR="$HOME/cold-email-generator"
  NAME="ReachFlow"
  PORT=5000
fi

echo ""
echo "  Starting $NAME on http://localhost:$PORT"
echo ""

cd "$DIR"
pip install -r requirements.txt --quiet --disable-pip-version-check
python app.py

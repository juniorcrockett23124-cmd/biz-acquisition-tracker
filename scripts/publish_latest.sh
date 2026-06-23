#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/macminiagent/Documents/projects/biz-acquisition-tracker"

cd "$ROOT"

python3 scripts/build_dashboard_json.py

(
  cd app
  npm run build
)

if git diff --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo "No changes to publish."
  exit 0
fi

git add data app/public/data docs/workflow.md README.md jobs/refresh-dashboard.md scripts/publish_latest.sh
git commit -m "${1:-Publish latest tracker updates}"
git push origin main

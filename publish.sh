#!/bin/bash
# Usage: ./publish.sh "commit message"   (run from the root of the `source` branch checkout)
# Builds the site, saves the source to the `source` branch and publishes the built site to `main` (Cloudflare auto-deploys main).
set -e
MSG="${1:-Update website}"
cd src && python3 build.py && cd ..
git add -A && git commit -qm "$MSG" || true
git push -q origin HEAD:source
TMP=$(mktemp -d)
git fetch -q origin main
git worktree add -q -f "$TMP" origin/main
find "$TMP" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -r worker/public/. "$TMP"/
( cd "$TMP" && git add -A && git commit -qm "$MSG" && git push -q origin HEAD:main )
git worktree remove --force "$TMP"
echo "published"

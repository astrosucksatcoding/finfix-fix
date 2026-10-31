#!/usr/bin/env bash
# Re-mirror financialfixationllc.com and rebuild ./site from it.
# Overwrites site/ (except site/assets/), so commit or back up your edits first.
# Usage: ./scripts/mirror.sh [url]
set -euo pipefail
URL="${1:-https://financialfixationllc.com/}"
HOST="$(echo "$URL" | awk -F/ '{print $3}')"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"

wget --mirror --page-requisites --convert-links --adjust-extension \
     --no-parent --restrict-file-names=windows -e robots=off \
     --span-hosts --domains="$HOST,www.$HOST" \
     --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36" \
     -P "$TMP" "$URL" || true   # wget exits non-zero on any 404; keep what we got

SRC="$TMP/$HOST"; [ -d "$SRC" ] || SRC="$TMP/www.$HOST"
python3 "$ROOT/scripts/clean_mirror.py" "$SRC" "$ROOT/site"
rm -rf "$TMP"
"$ROOT/scripts/fetch_missing.sh"

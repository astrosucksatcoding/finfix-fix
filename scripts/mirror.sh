#!/usr/bin/env bash
# Mirror financialfixationllc.com into ./site as plain static files.
# Usage: ./scripts/mirror.sh [url]
set -euo pipefail
URL="${1:-https://financialfixationllc.com/}"
HOST="$(echo "$URL" | awk -F/ '{print $3}')"
OUT="$(cd "$(dirname "$0")/.." && pwd)/site"
TMP="$(mktemp -d)"

wget --mirror --page-requisites --convert-links --adjust-extension \
     --no-parent --restrict-file-names=windows -e robots=off \
     --span-hosts --domains="$HOST,www.$HOST" \
     --user-agent="Mozilla/5.0 (static-demo mirror)" \
     -P "$TMP" "$URL" || true   # wget exits non-zero on any 404; keep what we got

SRC="$TMP/$HOST"; [ -d "$SRC" ] || SRC="$TMP/www.$HOST"
rm -rf "$OUT" && mkdir -p "$OUT" && cp -R "$SRC"/. "$OUT"/
rm -rf "$TMP"
echo "Mirrored into $OUT ($(find "$OUT" -type f | wc -l) files)"
echo "Preview: npx serve site"

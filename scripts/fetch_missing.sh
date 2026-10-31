#!/usr/bin/env bash
# Download the files the static copy is missing: Elementor loads these on demand after
# the page opens, so page-saving tools never see them. Run from a machine that can
# open financialfixationllc.com in a browser.
# Usage: ./scripts/fetch_missing.sh
set -uo pipefail
BASE="https://financialfixationllc.com"
SITE="$(cd "$(dirname "$0")/.." && pwd)/site"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
FILES=(
  wp-content/plugins/elementor/assets/js/chunks/background-slideshow.min.js
  wp-content/plugins/elementor/assets/js/chunks/background-video.min.js
  wp-content/plugins/elementor/assets/js/chunks/counter.min.js
  wp-content/plugins/elementor/assets/js/chunks/nested-accordion.min.js
  wp-content/plugins/elementor/assets/js/chunks/section-stretched-section.min.js
  wp-content/plugins/elementor/assets/js/chunks/text-editor.min.js
  wp-content/plugins/elementor/assets/js/chunks/toggle.min.js
  wp-content/plugins/elementor-pro/assets/js/carousel.3620fca501cb18163600.bundle.min.js
  wp-content/plugins/elementor-pro/assets/js/form.71055747203b48a65a24.bundle.min.js
  wp-content/plugins/elementor-pro/assets/js/nav-menu.8521a0597c50611efdc6.bundle.min.js
  wp-content/plugins/elementor-pro/assets/js/popup.f7b15b2ca565b152bf98.bundle.min.js
  wp-content/uploads/2025/11/1110211_Finance_Businesswomen_1920x1080-video-converter.com_.mp4
)
ok=0; bad=0
for f in "${FILES[@]}"; do
  mkdir -p "$SITE/$(dirname "$f")"
  tmp="$(mktemp)"
  if curl -fsSL -A "$UA" -e "$BASE/" -o "$tmp" "$BASE/$f" && ! head -c 200 "$tmp" | grep -qi '<html\|<!doctype'; then
    mv "$tmp" "$SITE/$f"; echo "ok    $f"; ok=$((ok+1))
  else
    rm -f "$tmp"; echo "FAIL  $BASE/$f"; bad=$((bad+1))
  fi
done
echo "$ok downloaded, $bad failed."
[ "$bad" -eq 0 ] || echo "For each FAIL, open the URL in your browser, save the file, and put it at site/<same path>."

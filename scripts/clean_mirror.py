#!/usr/bin/env python3
"""Turn a raw wget/HTTrack mirror of financialfixationllc.com into a clean static site.

Usage:  python3 scripts/clean_mirror.py <raw-mirror-dir> [<output-dir>=site]

What it does (all changes are mechanical; page copy is left untouched):
  1. Copies the mirror into the output dir.
  2. Renames asset files whose names contain "?ver=..." (e.g. main.min.css?ver=4.14.0.css
     -> main.min.css) so static hosts serve them with the right content type.
  3. Rewrites links to match: "%3Fver=..." suffixes are stripped, WordPress "?p=<id>"
     page links become "/<slug>/", and "../index.html" style links become clean URLs.
  4. Points absolute https://financialfixationllc.com/ references at the demo's own root,
     so the demo never loads anything from (or sends anything to) the live site.
  5. Removes the WordPress emoji loader and adds a noindex tag plus /assets/demo.js
     (which stops the contact forms from trying to post to WordPress).
"""
import re
import shutil
import sys
from pathlib import Path

LIVE = "financialfixationllc.com"

# WordPress page ID -> clean URL. IDs come from each page's <body class="page-id-N">.
PAGES = {
    47: "/",
    50: "/about-us/",
    52: "/services/",
    56: "/tax-advisory/",
    58: "/compliance/",
    60: "/contact/",
    64: "/client-testimonials/",
    567: "/virtual-chief-financial-strategist/",
    1785: "/consultation/",
    2231: "/about-founder/",
    2972: "/faq/",
}

# Mirror copies that duplicate another page; served as redirects in vercel.json instead.
DUPLICATES = ["tax-advisory-planning"]

TEXT_EXT = {".html", ".css", ".js"}
INJECT_HEAD = '<meta name="robots" content="noindex, nofollow">\n'
INJECT_BODY = '<script src="/assets/demo.js" defer></script>\n'


def rename_query_files(root: Path) -> int:
    n = 0
    for p in list(root.rglob("*")):
        if not p.is_file() or "?" not in p.name:
            continue
        target = p.with_name(p.name.split("?", 1)[0])
        if target.exists():
            p.unlink()  # e.g. "fa-solid-900.eot?" next to "fa-solid-900.eot"
        else:
            p.rename(target)
        n += 1
    return n


def page_link(m: re.Match) -> str:
    pid = int(m.group(1))
    if pid not in PAGES:
        raise SystemExit(f"Unknown WordPress page id {pid}: add it to PAGES")
    return PAGES[pid]


def clean_text(text: str, is_html: bool) -> str:
    # LinkedIn "authwall" redirect captured by the crawler -> the plain profile URL.
    text = re.sub(
        r"https://www\.linkedin\.com/authwall\?[^\"']*?sessionRedirect=https%3A%2F%2Fwww\.linkedin\.com%2Fin%2F([\w-]+)[^\"']*",
        r"https://www.linkedin.com/in/\1/",
        text,
    )
    # WordPress ?p=<id> page links saved by wget as index.html%3Fp=<id>.html
    text = re.sub(r"(?:\.\./)*index\.html%3Fp=(\d+)\.html", page_link, text)
    # ../index.html, about-us/index.html, ../faq/index.html -> clean URLs
    text = re.sub(
        r"(?<=[\"'])(?:\.\./)*((?:[a-z0-9-]+/)?)index\.html(?=[\"'#])",
        lambda m: "/" + m.group(1),
        text,
    )
    for dup in DUPLICATES:
        text = text.replace(f"/{dup}/", "/tax-advisory/")
    # Asset cache-busting suffixes: foo.css%3Fver=1.2.css -> foo.css
    text = re.sub(r"(\.[A-Za-z0-9]{2,5})%3F[^\"'\s)<>]*", r"\1", text)
    # Absolute links to the live site -> demo root
    text = text.replace(f"https:\\/\\/{LIVE}\\/", "\\/").replace(f"https://{LIVE}/", "/")
    if is_html:
        # WordPress emoji loader (pure polyfill; would 404)
        text = re.sub(r'<script id="wp-emoji-settings"[\s\S]*?</script>\s*<script type="module">[\s\S]*?</script>\s*', "", text)
        if INJECT_HEAD not in text:
            text = text.replace("<head>", "<head>\n" + INJECT_HEAD, 1)
        if INJECT_BODY not in text:
            text = text.replace("</body>", INJECT_BODY + "</body>", 1)
    return text


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    src = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "site").resolve()
    keep = out / "assets"
    saved = None
    if keep.exists():
        saved = out.parent / ".assets-keep"
        shutil.rmtree(saved, ignore_errors=True)
        shutil.copytree(keep, saved)
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(src, out)
    if saved:
        shutil.copytree(saved, keep, dirs_exist_ok=True)
        shutil.rmtree(saved)
    (out / "vercel.json").unlink(missing_ok=True)  # repo-root vercel.json is the one Vercel reads
    for dup in DUPLICATES:
        shutil.rmtree(out / dup, ignore_errors=True)

    renamed = rename_query_files(out)
    changed = 0
    for p in out.rglob("*"):
        if p.is_file() and p.suffix in TEXT_EXT:
            before = p.read_text(encoding="utf-8", errors="surrogateescape")
            after = clean_text(before, p.suffix == ".html")
            if after != before:
                p.write_text(after, encoding="utf-8", errors="surrogateescape")
                changed += 1
    print(f"Renamed {renamed} asset files, rewrote {changed} files -> {out}")


if __name__ == "__main__":
    main()

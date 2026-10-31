# Financial Fixation — static demo

A static copy of https://financialfixationllc.com/ (a WordPress + Elementor site) for editing and demoing. It's hosted on Vercel.

## Layout
```
site/                     the website Vercel serves
  index.html              home page
  <page>/index.html       other pages (about-us, services, faq, contact, ...)
  wp-content/, wp-includes/  styles, scripts, images and fonts copied from WordPress
  assets/demo.js          demo-only: stops forms from submitting
scripts/
  clean_mirror.py         turns a raw site download into site/ (fixes file names and links)
  fetch_missing.sh        downloads the 12 files the downloader can't see (see below)
  mirror.sh               full re-download + clean + fetch (overwrites site/)
CHANGELOG.md              every change made vs. the live site — add to it when you edit
vercel.json               Vercel settings: serve site/, clean URLs, keep out of search engines
```

## Preview locally
```bash
npx serve site
```
Then open http://localhost:3000. Opening the HTML files directly by double-clicking them won't work, because links start at the site root.

## Missing files (run once)
Elementor loads some scripts and the home page's background video only after the page opens, so the copy is missing them. Until they're added:
- the mobile menu button doesn't open,
- FAQ questions don't expand,
- the home page banner is gray instead of showing the video,
- number counters and the testimonial slider don't animate.

From a computer that can open the live site:
```bash
./scripts/fetch_missing.sh
```
Then commit and push `site/`.

## Editing
Page text is in each `site/<page>/index.html`. Search for the sentence you want to change and edit it in place. Page-specific styling is in `site/wp-content/uploads/elementor/css/post-<id>.css`:

| id | page |
|---|---|
| 47 | home |
| 50 | about-us |
| 52 | services |
| 56 | tax-advisory |
| 58 | compliance |
| 60 | contact |
| 64 | client-testimonials |
| 567 | virtual-chief-financial-strategist |
| 1785 | consultation |
| 2231 | about-founder |
| 2972 | faq |

Shared header, footer and colors are in post-10, post-79 and post-89.

## What behaves differently from the live site
- **Contact forms** don't send anything. Submitting one shows a "Demo site" notice (`site/assets/demo.js`). For real submissions, point the forms at a service such as Formspree.
- **Links that still go to live services:** Calendly booking, the Dubsado and SecureFilePro client portal, Google Maps, social links, and the email and phone links.
- The browser tab title is the WordPress site name, "finfix2025", the same as on the live site.
- `/tax-advisory-planning/` was an exact duplicate of `/tax-advisory/`, so it now redirects there.

## Deploy to Vercel
Import this repo at https://vercel.com/new and keep the default settings. `vercel.json` already tells Vercel to serve `site/` with no build step. Or, from the command line:
```bash
npx vercel --prod
```
Every page is sent with `noindex` so the demo stays out of Google. Don't attach the real domain unless the owner approves.

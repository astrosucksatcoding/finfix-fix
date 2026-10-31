# Change log

Every change made to the static demo of financialfixationllc.com, compared with the live site. Newest entries at the top.

When you make an edit, add a line under a new dated heading: what changed, which file, and why. Git keeps the exact before and after (`git log -p <file>`), so this file only needs the plain-English version.

---

## 2026-10-31 — Static copy built from the site snapshot

Source: `financialfixation-static.zip` (a WordPress + Elementor download of the live site), imported into `site/`. Commits `c16685b` and `39abc40` on branch `claude/pensive-hawking-qahpmo`.

### Page content
No wording, images or layout were changed. Each page should match the live site.

### Pages and links
| Change | Where | Why |
|---|---|---|
| 596 links between pages rewritten from WordPress-style addresses (`index.html?p=1785`) to clean ones (`/consultation/`) | all 11 pages | The old addresses pointed to files that don't exist in the copy |
| Links like `../index.html` changed to `/` and `/about-us/` | all pages | Clean URLs on Vercel |
| `/tax-advisory-planning/` removed and now redirects to `/tax-advisory/` | `vercel.json` | It was a byte-for-byte duplicate, so editing one would leave the other out of date |
| The founder's LinkedIn link now goes straight to `linkedin.com/in/felicia-paul-65078036/` | every page | The saved link was LinkedIn's login wall with tracking parameters attached |

### Files and technical fixes
| Change | Where | Why |
|---|---|---|
| 94 style, script and font files renamed to drop version tags (`main.min.css?ver=4.14.0.css` → `main.min.css`); 3 of them were duplicate font files and were deleted instead | `site/wp-content/`, `site/wp-includes/` | Vercel can't serve file names that contain `?`, and scripts without a `.js` ending can be blocked by browsers |
| References to the live domain (`https://financialfixationllc.com/...`) changed to start at the demo's own root | page HTML and its embedded settings | So the demo never loads files from, or sends data to, the live site |
| WordPress emoji loader script removed | all pages | It only loads a fallback for old browsers and would have failed |
| Snapshot's own `vercel.json` removed from `site/` | — | Vercel reads the one at the repo root |

### Added for the demo (not on the live site)
| Change | Where | Why |
|---|---|---|
| Contact forms stop on submit and show "Demo site: form submissions are turned off on this preview." | `site/assets/demo.js`, loaded on every page | The forms post to WordPress, which doesn't exist here. Without this they would show an error |
| `<meta name="robots" content="noindex, nofollow">` on every page, plus the same rule as a header on every response | every page, `vercel.json` | Keeps the demo out of Google so it doesn't compete with the real site |
| `robots.txt` blocks all crawlers | `site/robots.txt` | Came with the snapshot; kept |

### Repo tooling
| File | Purpose |
|---|---|
| `vercel.json` | Serves `site/` with no build step, clean URLs and trailing slashes, the noindex header and the tax-advisory redirect |
| `scripts/clean_mirror.py` | Repeats every fix above on a fresh download of the site |
| `scripts/fetch_missing.sh` | Downloads the 12 files the snapshot is missing (see below) |
| `scripts/mirror.sh` | Full re-download, clean-up and fetch. It overwrites `site/`, so commit your edits first |
| `README.md` | How to preview, edit and deploy |
| `CHANGELOG.md` | This file |

### Not changed on purpose
- The browser tab title stays "finfix2025", the WordPress site name, the same as on the live site.
- These links still go to the business's real accounts: Calendly booking ("Book Now"), the Dubsado and SecureFilePro client portal, Google Maps, social media, `info@financialfixationllc.com` and (512) 309-8810.

### Known gaps (open)
- [ ] **12 files are missing from the snapshot.** Elementor loads them only after a page opens, so the downloader never saw them: 11 scripts and the home page banner video. Until they're added, the phone menu doesn't open, FAQ questions don't expand, the home banner is gray, and the counters and testimonial slider don't animate. Fix: run `./scripts/fetch_missing.sh` on a computer that can open the live site, then commit `site/`.
- [ ] Re-test every page after the missing files are added. They may load further files of their own.

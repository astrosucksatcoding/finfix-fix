# Financial Fixation — static demo

Static copy of https://financialfixationllc.com/ for editing and demoing, hosted on Vercel.

## 1. Pull the site
```bash
./scripts/mirror.sh
```
Writes the HTML, CSS, JS and images into `site/`. Run it from a machine that can reach the site.

## 2. Preview locally
```bash
npx serve site
```

## 3. Edit
Edit the files in `site/` directly. Each page is `site/<path>/index.html` or `site/<page>.html`.

Things that won't work in a static copy and need replacing before a real launch:
- Contact and booking forms that post to the original platform (Wix, Squarespace, GoDaddy and others). Swap in Formspree, Netlify Forms or a mailto link.
- Analytics and chat widgets that are tied to the original domain.
- Scripts that render content at runtime (common on site builders). If a page looks blank, the content is loaded by JavaScript and has to be rebuilt by hand.

## 4. Deploy to Vercel
Import this repo at https://vercel.com/new. `vercel.json` already sets the output folder to `site/`, so there is no build step. Or from the CLI:
```bash
npx vercel --prod
```

Keep the demo off search engines and don't attach the real domain until the owner approves it.

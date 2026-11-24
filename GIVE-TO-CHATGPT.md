# Instructions for the AI assistant (ChatGPT, Codex, or any agent)

You are helping a teammate edit the StarSI website. Read all of this first, then do what the teammate asks.

## The project
- The website is built from small files in the `sections/` folder (one `.html` and one `.css` per section). `index.html` is generated from them automatically. NEVER edit `index.html`.
- Repository: https://github.com/abluemaw/starsi-site (public, branch `main`)
- Read `AGENTS.md` first. It explains the files. Always read the latest section file before editing, for example: https://raw.githubusercontent.com/abluemaw/starsi-site/main/sections/30-growth.html
- Live site: https://abluemaw.github.io/starsi-site/
- Design system (read before any design change): https://raw.githubusercontent.com/abluemaw/starsi-site/main/DESIGN.md and the page https://abluemaw.github.io/starsi-site/design/
- If you cannot open those links, ask the teammate to paste the current section file. Never edit from memory of an older version.

## Rules
1. Make only the change the teammate asked for. Leave everything else exactly as it is.
2. Use the teammate's wording exactly. Do not rewrite, shorten or "improve" copy unless asked.
3. Keep the section comment at the top of each section file and the existing class names.
4. Colors, fonts, spacing and corners are values at the top of `DESIGN.md` (the design system). For a design change like "make the gold deeper" or "use rounder buttons", edit that value in `DESIGN.md` and nothing else; the site and the design page rebuild by themselves. If the teammate wants their OWN version of the look ("my design", "try a variant"), do NOT touch `DESIGN.md`: create `designs/<their-name>.md` with only the values that differ (see `designs/README.md` for the format), and tell them to pick it in the "Look" dropdown on the site. In section CSS use the variables only (for example `var(--gold-400)`), never raw colours. Never edit `design/index.html`.
5. It must look right on a phone. Keep the existing responsive rules.
6. No tracking scripts, no forms that collect data, no new outside services or libraries.
7. The page copy comes from the owner's approved prototype and carries its own cautions ("preview mode", "estimated value", "not a forecast or guarantee"). Never remove or soften those notices, never change prices, and never claim customer results, unless the teammate says the owner approved.

## How to deliver the change (use the first one you can do)

**A. You can write to GitHub (Codex or a GitHub connection):**
1. Start from the latest `main`.
2. Create a new branch in the repo `abluemaw/starsi-site` (not a fork) and make the edit in the right file in `sections/`.
3. Open a pull request into `main`. A rule in the repo merges it automatically within a minute, rebuilds `index.html`, and the live site updates by itself. Do not wait for a review.
4. Tell the teammate the pull request link and that the live site updates in about a minute.

**B. You cannot write to GitHub:**
1. Tell the teammate which file in `sections/` to change, and give ONLY the changed part, as a clear "find this, replace with this" pair:
   - FIND: the exact existing text or block, copied character for character
   - REPLACE WITH: the new text or block
   Keep each block small and say which section it is in.
2. Then give these steps in plain words:
   1. Open https://github.com/abluemaw/starsi-site/tree/main/sections, click the section file, and click the pencil icon.
   2. Press Cmd+F (Ctrl+F on Windows) and search for the FIND text.
   3. Replace it with the new text. Do not touch symbols like `<` and `>`.
   4. Click Commit changes, keep "Commit directly to the main branch", click Commit changes again.
   5. Refresh https://abluemaw.github.io/starsi-site/ after about a minute.
3. If the change is large, give the complete new section file and tell the teammate to replace the whole file in the GitHub editor (select all, paste, commit).

## Undo
If the teammate says "undo that", do the opposite change, or open a pull request that reverts the last commit.

## Before you finish
- Re-read your edit for broken tags or missing closing `</div>`.
- Confirm you did not edit `index.html` and did not paste an image in as text. Images go in `images/`.
- Check that nothing outside the requested change moved.
- State in one or two sentences what you changed and where.

## Languages (English, Spanish, Korean)
- The English page is `index.html`. The Spanish and Korean pages (`/es/`, `/ko/`) are built from it by `build.py`; never edit them by hand.
- Every translated line lives in `i18n/es.json` and `i18n/ko.json` as `"exact English text": "translation"`.
- When you change English wording in `sections/`, also update the same line in both i18n files, or the page shows the old English there. The build prints a warning for any translation line that no longer matches.
- Product names (AI Website, AI Concierge, U-Bill, HQ Function and so on) stay in English on purpose.
- The first drafts of the translations need review by a native speaker before they count as final.
- The language menu is in `sections/01-header.html`; the "What could success look like?" section has its own words in `sections/27-success.js`.

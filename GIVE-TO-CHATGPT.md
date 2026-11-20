# Instructions for the AI assistant (ChatGPT, Codex, or any agent)

You are helping a teammate edit the StarSI website. Read all of this first, then do what the teammate asks.

## The project
- The whole website is ONE file: `index.html` (plain HTML and CSS, no build step, no frameworks).
- Repository: https://github.com/abluemaw/starsi-site (public, branch `main`)
- Latest file, always read this before editing: https://raw.githubusercontent.com/abluemaw/starsi-site/main/index.html
- Live site: https://abluemaw.github.io/starsi-site/
- If you cannot open those links, ask the teammate to upload or paste the current `index.html`. Never edit from memory of an older version.

## Rules
1. Make only the change the teammate asked for. Leave everything else exactly as it is.
2. Use the teammate's wording exactly. Do not rewrite, shorten or "improve" copy unless asked.
3. Keep the section comments (`SECTION 3: BENEFITS` and so on) and the existing class names.
4. Colors, fonts and spacing are the variables in `:root { ... }` at the top of the `<style>` block. Change those for site-wide changes instead of editing many lines.
5. It must look right on a phone. Keep the existing responsive rules.
6. No tracking scripts, no forms that collect data, no new outside services or libraries.
7. The page has two placeholders waiting on the owner: `[Confirm each quote is OK to reuse under the StarSI name]` and `[BONUS GIFT: name it here]`. Do not remove or fill them in unless the teammate says the owner approved.

## How to deliver the change (use the first one you can do)

**A. You can write to GitHub (Codex or a GitHub connection):**
1. Start from the latest `main`.
2. Create a new branch in the repo `abluemaw/starsi-site` (not a fork) and make the edit in `index.html`.
3. Open a pull request into `main`. A rule in the repo merges it automatically within a minute and the live site updates by itself. Do not wait for a review.
4. Tell the teammate the pull request link and that the live site updates in about a minute.

**B. You cannot write to GitHub:**
1. Give the teammate ONLY the changed part, as a clear "find this, replace with this" pair:
   - FIND: the exact existing text or block, copied character for character
   - REPLACE WITH: the new text or block
   Keep each block small and say which section it is in.
2. Then give these steps in plain words:
   1. Open https://github.com/abluemaw/starsi-site/blob/main/index.html and click the pencil icon.
   2. Press Cmd+F (Ctrl+F on Windows) and search for the FIND text.
   3. Replace it with the new text. Do not touch symbols like `<` and `>`.
   4. Click Commit changes, keep "Commit directly to the main branch", click Commit changes again.
   5. Refresh https://abluemaw.github.io/starsi-site/ after about a minute.
3. If the change is large, give the complete new `index.html` and tell the teammate to replace the whole file in the GitHub editor (select all, paste, commit).

## Undo
If the teammate says "undo that", do the opposite change, or open a pull request that reverts the last commit.

## Before you finish
- Re-read your edit for broken tags or missing closing `</div>`.
- Check that nothing outside the requested change moved.
- State in one or two sentences what you changed and where.

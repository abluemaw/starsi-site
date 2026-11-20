# StarSI website: instructions for ChatGPT / Codex / any AI helper

This is a plain static website. The page is `index.html`. There is no build step.

## Rules
1. Edit `index.html` only (add new `.html` pages next to it if asked). Keep it plain HTML and CSS, no frameworks.
2. Use the copy the owner gives you exactly. Do not rewrite, "improve" or shorten wording unless asked.
3. Keep section comments (`SECTION 3: BENEFITS` etc.) so others can find things.
4. Colors and fonts live in `:root { ... }` at the top of the `<style>` block. Change those, not hundreds of lines.
5. The page must work on phones. Check narrow widths.
6. Do not add tracking scripts, forms that collect data, or external services without asking.
7. Make small, clear changes and describe them in the commit message ("Change hero headline").

## How changes go live
Every push to the `main` branch publishes the live site automatically (about 30 seconds). There is no approval step, so double-check before you push, and pull the latest first (`git pull`) so you do not overwrite a teammate's change.
Undo a mistake: `git revert HEAD` then `git push`.

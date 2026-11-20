# StarSI website (live)

Live: https://abluemaw.github.io/starsi-site/ (GitHub Pages, updates about a minute after every push to `main`)
Designs gallery: https://abluemaw.github.io/starsi-site/designs/ (each design also has its own page at `designs/<name>/`) · Design system page: https://abluemaw.github.io/starsi-site/design/ · Version history: https://abluemaw.github.io/starsi-site/versions/ · Design file: [DESIGN.md](DESIGN.md)
The page is built from small files in `sections/` (one per section) by `build.py`; `index.html` is generated, never edited by hand. Anyone on the team can change it with ChatGPT, and the live site updates by itself.

## For coworkers (using ChatGPT)
1. Get a free GitHub account and ask Amen to add you to the repo.
2. In ChatGPT, open Codex (or ChatGPT with the GitHub connection), choose this repo, and tell it what to change:
   "Change the hero headline to ... " or "Make the testimonials section have two columns."
   It reads `AGENTS.md` for the house rules by itself.
3. Let it commit straight to `main`. The live site updates in about 30 seconds. No approval step.
4. Something broke? Tell ChatGPT "undo the last change" (it runs `git revert`).

## Set up (done)
- Repo is public (required for free GitHub Pages). Pages publishes the `main` branch.
- Add coworkers: repo Settings > Collaborators > Add people, Write access.
- Buttons in the repo's Actions tab: "Save this version" (name the current site) and "Restore the site" (go back to a saved name or commit).
- `DESIGN.md` is the design system. It syncs with `sections/00-tokens.css` in both directions (if both change at once, DESIGN.md wins) and generates the page at `/design/`.
- Design variants live in `designs/` (one small file each). The "Look" dropdown in the site header and the design page previews them; Actions > "Make a design live" promotes one into `DESIGN.md`. Set `lookPicker: "off"` in `DESIGN.md` to hide the dropdown.
- After a change, GitHub rebuilds `index.html` itself (auto-merge and `build.yml`).

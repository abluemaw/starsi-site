# StarSI website (live)

Live: https://abluemaw.github.io/starsi-site/ (GitHub Pages, updates about a minute after every push to `main`)
The whole page is `index.html`. Anyone on the team can change it with ChatGPT, and the live site updates by itself.

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

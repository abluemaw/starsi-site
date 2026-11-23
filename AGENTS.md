# StarSI website: instructions for ChatGPT / Codex / any AI helper

This is a plain static website. The page is built from small files in the `sections/` folder. There is no framework.

## Where things are
- `sections/NN-name.html`: the words and layout of one section (`10-welcome`, `20-sales`, `30-growth`, `40-calculator`, `50-passion`, `60-faq`, `70-enroll`, `72-features`, `74-benefits`, `76-pricing`, `78-stories`, plus `01-header`, `90-footer` and `96-sticky-cta`). Some sections also have a `.js` file (calculator, enrollment preview, welcome banner).
- `sections/NN-name.css`: the styling for that same section.
- `sections/00-head.html`: page title and description. `sections/00-base.css`: colours, fonts and spacing variables (`:root { ... }`).
- `DESIGN.md`: the design system (colours, fonts, spacing, corners, light and dark). It is kept in step with `sections/00-tokens.css` automatically in both directions, and the page `design/index.html` is generated from it.
- `designs/`: personal design variants. One file per variant (for example `designs/erin.md`) listing ONLY the values that differ from `DESIGN.md`. People try a variant with the "Look" dropdown or `?design=name`. For a personal try-out, create or edit a file in `designs/` and leave `DESIGN.md` alone. Never edit `designs/looks/`, `designs/variants.json`, `designs/index.html` or the generated `designs/<name>/` folders. A design may also set `logo`, `logoLight`, `logoWidth`, `fontsUrl` and `headingStretch`; put logo files in `images/`. Pictures go in `images/` (WebP or JPG, under about 300 KB). See `designs/README.md`.
- `images/`: pictures (for example `images/hero.webp`). Reference them as `images/name.webp`.
- `index.html` is GENERATED from those files by `build.py`. NEVER edit `index.html`: any change to it is thrown away at the next build.
- To add a section: create `sections/NN-name.html` (and `.css`) with a number between 10 and 89 to set its position. Numbers 10 to 89 sit inside `<main>`.

## Rules
1. Edit only the section file(s) the change needs. Leave everything else exactly as it is.
2. Use the copy the owner gives you exactly. Do not rewrite, "improve" or shorten wording unless asked.
3. Keep the section comment at the top of each `.html` file (`SECTION 3: GROW YOUR PROFITS` etc.) and the existing class names.
4. Design changes (a colour, a font, spacing, corner roundness, light or dark values): change the value in the list at the top of `DESIGN.md`. The site follows after the merge. Section CSS must use the variables (`var(--gold-400)`, `var(--page-bg)`), never raw colours. Never edit `design/index.html` or `index.html`.
5. The page must work on phones. Check narrow widths.
6. Do not add tracking scripts, forms that collect data, or external services without asking.
7. Never put images inline as base64 text. Save the image file in `images/` and link to it.
8. Make small, clear changes and describe them in the commit message ("Change hero headline").

## How changes go live
Open a pull request against `main` from a branch in this repository. Pull requests are merged automatically within about a minute, with no review. GitHub then rebuilds `index.html` and publishes the site by itself. Always start from the latest `main` so you do not overwrite a teammate's change.
Undo a mistake: open a pull request that reverts the bad commit, or use the "Restore the site" button in the Actions tab.

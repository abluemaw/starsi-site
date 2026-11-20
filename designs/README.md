# Design variants

Each file here is one person's (or one idea's) version of the look. It lists ONLY the values that differ from the shared `DESIGN.md`; everything else comes from the shared design, so changes the team makes to `DESIGN.md` reach every variant.

- File name = the variant name used in the picker and the web address (`red-belt.md` -> `?design=red-belt`).
- Format: same front matter as `DESIGN.md`, but only the lines you change (colors, effects, typography, spacing, rounded, themes), plus `name:` and `description:`.
- Try one: use the "Look" dropdown in the site header or on the design page, or open `https://abluemaw.github.io/starsi-site/?design=red-belt`.
- Make one live for everyone: Actions tab > "Make a design live" > Run workflow > type the name.
- `looks/` and `variants.json` in this folder are generated. Do not edit them.
- Every design also gets its own page, `designs/<name>/`, and the gallery of all designs is `designs/` (pictures are taken automatically). Both are generated; do not edit them.
- Optional lines in a variant's front matter: `fontsUrl:` (a Google Fonts stylesheet link, loaded only when that design is on) and `headingStretch:` (for example `"125%"` for wide headings).

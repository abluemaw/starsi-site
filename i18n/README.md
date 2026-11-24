# Translations

One file per language: `es.json` (Español) and `ko.json` (한국어).
Each line is `"exact English text from the page": "the translation"`.
The build makes `/es/` and `/ko/` pages from the English page by swapping those lines.
- Lines with no translation stay in English (nothing breaks).
- If someone changes the English wording, the old line stops matching and the build prints a warning, so it can be re-translated.
- These first drafts need a native speaker to review them before they are treated as final.

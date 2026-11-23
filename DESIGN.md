---
name: "StarSI Gold"
description: "Bold StarSI.AI look: deep navy night ground, gold metal buttons and headlines, chrome and electric blue accents, blue glass cards with metal rims. Titillium Web headlines, Roboto body. Works in light and dark."
# Show the "Look" dropdown in the site header? on / off
lookPicker: "on"
# Logo files (paths inside the repo). logoLight is optional: used on light pages. logoWidth is the header size in px on desktop.
logo: "images/starsi-ai-logo.webp"
logoLight: ""
logoWidth: "220"
# Optional: a Google Fonts stylesheet link and a heading width (for example "125%")
fontsUrl: ""
headingStretch: ""
# HOW THIS FILE WORKS: every value below becomes a CSS variable on the site (sections/00-tokens.css).
# Change a value here and the site follows. Change a value in sections/00-tokens.css and it is copied back here.
colors:
  # Ground and panels
  night: "#070B1C"
  navy900: "#060D3A"
  panel: "#0E1E60"
  panelLight: "#2040AA"
  # Light surfaces
  surface: "#FFFFFF"
  surfaceSoft: "#F3F5FA"
  surfaceMuted: "#E3E8F3"
  # Text
  ink: "#0A1130"
  inkMuted: "#465178"
  inkOnDark: "#F4F6FF"
  inkOnDarkMuted: "#A9B3D6"
  headingOnDark: "var(--gold-400)"
  # Gold: primary action, buttons, headline metal
  gold300: "#FFE680"
  gold400: "#FFC61A"
  gold500: "#F2A100"
  gold600: "#B96A00"
  gold900: "#4D2A05"
  onGold: "#1A0F00"
  # Chrome: frames, rims, secondary buttons
  chrome100: "#F4F6FA"
  chrome300: "#C5CCD8"
  chrome500: "#8892A3"
  chrome700: "#4A5365"
  # Electric blue: AI, links, focus
  electric300: "#7FB2FF"
  electric500: "#1F5CFF"
  electric700: "#0B2FB0"
  link: "#1646D6"
  # Lines and status
  border: "#C3CBE0"
  borderStrong: "#66719B"
  success: "#0B7A55"
  successBright: "#4FD6A0"
  warning: "#8A5200"
  danger: "#C0152F"
  dangerBright: "#FF8591"
effects:
  goldMetal: "linear-gradient(180deg,#fff3b0 0%,#ffd23f 28%,#f0a000 49%,#ffc61a 52%,#ffe27a 100%)"
  chromeMetal: "linear-gradient(180deg,#ffffff 0%,#dfe4ec 45%,#9aa4b4 50%,#cfd6e0 52%,#f4f6fa 100%)"
  electricMetal: "linear-gradient(180deg,#1f5cff 0%,#0b2fb0 100%)"
  bevelGold: "inset 0 2px 0 #fff0a8, inset 0 -3px 0 #b96a00, 0 3px 0 #4d2a05"
  rimChrome: "conic-gradient(from 20deg,#f4f6fa,#aab4c6,#ffffff,#dfe4ec,#9aa4b4,#f4f6fa)"
  rimGold: "conic-gradient(from 20deg,#fff3b0,#b96a00,#ffe27a,#f2a100,#4d2a05,#fff3b0)"
  cardShadow: "0 10px 28px rgba(6,13,58,.28)"
  buttonGloss: "rgba(255,255,255,.16)"
  buttonSweep: "rgba(255,255,255,.55)"
typography:
  display:
    fontFamily: "'Titillium Web', 'Arial Black', system-ui, sans-serif"
    fontWeight: "700"
    note: "Headlines. Tight leading (about 1.15). Font files live in the fonts folder."
  body:
    fontFamily: "Roboto, system-ui, sans-serif"
    fontWeight: "400"
    note: "Paragraphs and labels. 700 for emphasis and buttons."
  mono:
    fontFamily: "'IBM Plex Mono', ui-monospace, monospace"
    note: "Small data and code only."
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  xxl: "48px"
  xxxl: "64px"
rounded:
  sm: "4px"
  md: "8px"
  lg: "14px"
  pill: "999px"
components:
  buttons: "Primary: gold metal. Vertical horizon-band gradient (#FFF3B0 > #FFD23F > #F0A000 > #FFC61A > #FFE27A), dark label #1A0F00, Roboto 700, 8px radius, slanted -8deg with the label slanted back so text stays upright. Bevel shadow: inset 0 2px 0 #FFF0A8, inset 0 -3px 0 #B96A00, 0 3px 0 #4D2A05. A glossy top half and a slow light sweep. Sizes: small 13px, medium 15px, large 17px, extra large 22px for the hero. Secondary: chrome (white to grey metal, brushed). Accent: electric blue gradient with white label. Ghost: transparent with a 2px strong border. One gold button per view is the action."
  eyebrows: "The small label above a headline is plain text, not a button: uppercase, bold, wide tracking, electric blue (the link colour for the current mode). No background, no border, no pill and no line, so it never looks clickable."
  cards: "Blue glass panel: vertical gradient from #2040AA to #0E1E60 (96% opaque), 14px radius, with a metal rim (chrome conic gradient) that gets a slow light sweep. On hover or for featured cards the rim turns gold."
  badges: "Pills (999px), never wrap, 12px on phones."
  forms: "Fields: soft surface fill, 2px strong border, 8px radius. Focus shows a 3px electric blue ring (gold on dark)."
  motion: "Slow and heavy: light sweeps across metal, hyperspace star field and rising gold embers behind the hero, tilt on cards. Always off for people who ask for reduced motion."
themes:
  dark:
    page: "#070B1C"
    pageAlt: "#0B1230"
    text: "#F4F6FF"
    textMuted: "#A9B3D6"
    cardFill: "#0B1230"
    line: "rgba(255,255,255,.14)"
    link: "#7FB2FF"
    label: "#FFC61A"
    heading: "var(--gold-400)"
    ok: "#4FD6A0"
    okBg: "rgba(79,214,160,.15)"
    navBg: "rgba(7,11,28,.9)"
    heroGlow: "#14275A"
    headlineFrom: "#FFF3B0"
    headlineMid: "#FFC61A"
    headlineTo: "#F2A100"
  light:
    page: "#F3F5FA"
    pageAlt: "#FFFFFF"
    text: "#0A1130"
    textMuted: "#465178"
    cardFill: "#FFFFFF"
    line: "#D5DBEA"
    link: "#1646D6"
    label: "#8A5200"
    heading: "var(--gold-400)"
    ok: "#0B7A55"
    okBg: "rgba(11,122,85,.14)"
    navBg: "rgba(243,245,250,.92)"
    heroGlow: "#FFF1BF"
    headlineFrom: "#0A1130"
    headlineMid: "#0A1130"
    headlineTo: "#0A1130"
dials:
  variance: 0.9
  density: 0.6
  motion: 0.9
---

# StarSI Gold · design system for the website

*Nov 20, 2026. Based on the bold StarSI site with gold buttons (the "loud" version) and its design system tokens. This is a separate system from the lime and ice-blue StarSi v14 brand and from the Clean White system. Do not mix them.*

## What this look is

Big, bold and a little over the top, on purpose. The page sits on a deep navy night sky. Everything that matters is **metal**: gold for the action, chrome for frames, electric blue for the AI. Headlines are big, bold and glossy. Buttons are slanted and bevelled like a trophy.

## Light mode and dark mode

Both are first-class. The page follows the visitor's device setting and offers a switch.

- **Dark (default look):** deep navy ground, white text, bright gold headline metal.
- **Light:** soft grey-white ground, deep navy text and headlines, white cards. Headlines are solid navy in light mode (gold text is for dark ground only); the gold stays on buttons and icons.
- **What never changes:** the gold, chrome and electric buttons, the blue glass cards with their metal rims, the spacing and corner radii. Cards keep white text in both modes.
- **Rule:** nothing is hard-coded to one mode. Use the theme roles (page, text, textMuted, cardFill, line, link, label), not raw colours.

## How to use it

1. **Gold means action.** The gold button is the one thing to click on a screen ("Book My Free Demo"). Use one per view. Do not use gold for body text.
2. **Electric blue means AI and focus.** Links, glows, focus rings and anything the AI does.
3. **Chrome is for structure.** Frames, rims, secondary buttons, dividers.
4. **Text:** white on dark, deep navy (#0A1130) on light. Gold text only for large display headlines on dark.
5. **Contrast:** body text must pass 4.5 to 1. Never put copy over a face in a photo.

## Colour roles

| Role | Token (value is in the list at the top of this file) |
|---|---|
| Page ground | night (dark) / themes.light.page |
| Panels and cards | panel, panelLight |
| Primary action | gold400, with the metal scale gold300 to gold600 |
| Text on gold | onGold |
| AI and accent | electric500 |
| Frames | chrome300 |
| Text on dark | inkOnDark, inkOnDarkMuted |

The values themselves are never repeated in this text, so there is only one place to change them.

## Type

- **Display:** Titillium Web Bold, leading 1.15, sizes fluid with the screen.
- **Body:** Roboto 400, 17 to 18px for lead paragraphs, 15 to 16px elsewhere, line height 1.5 to 1.6.
- Fonts are files in the `fonts` folder (loaded in `sections/00-base.css`). Keep a safe fallback.

## Icons

- **Style:** bold rounded outlines (2.4px line on a 24px grid) with small dash-and-dot detail lines, one colour (it follows the text colour, so it works in light and dark). Five icons (belt, gi, kick, meditate, palm strike) come from the supplied exercise set; the rest are drawn to match it.
- **Where they live:** one SVG per icon in the `icons` folder. `icons/sprite.svg` and the Icons section of the design page are generated from that folder, so adding a file adds an icon everywhere.
- **Use:** gold (`gold400`) for the one icon you want noticed, ink or text colour for the rest. On gold buttons and chips use `onGold`. On blue glass use `gold300` or `inkOnDark`.
- **First set:** belt, gi, fist, dojo gate, trophy, medal, star, glove, mat, gong, certificate, shield.
- **Second set (class and school life):** attendance, family, calendar, pro shop, billing, check-in, trial lesson, student, instructor, message, report, location, class time, backpack, snack, lesson video, homework.
- **Martial arts pack (Flaticon, pack 921600, by Freepik):** 31 icons (stances, kicks, punches, boxing, kendo, sumo, kimono, bow, tatami ring and more); the exercise set's kick, belt, gi, meditate and palm strike also come from it. Credit: icons designed by Flaticon / Freepik (flaticon.com). Weapons are left out on purpose.
- **From your own ATLAS icon files (backgrounds removed, recoloured):** 2020 program icons (after school, business, campaigns, social media, software, settings) and the 2023 app icons (account, address, call, email, home, last attended, map, membership, messages, password, sign out, students, website). The app icons are small and thin, so use them a size up.
- **Lending (2021):** two students with a dollar coin and exchange arrows, for payments, tuition and billing transfers.
- **From the 2021 icon tests (background removed):** scanner, kiosk, tablet agreement, megaphone, tap, checkbox, kick check. They are thinner than the bold set, so use them a size up.
- **Rules:** keep to martial arts and school life (belts, ranks, classes, families). No weapons, no violence.

## Logo

- The logo files are set at the top of this file (`logo`, `logoLight`, `logoWidth`) and shown in the Logo section of the design page.
- The site header uses `logo`. If `logoLight` is set, light pages use that one instead.
- Use the files, never retype the name. Keep clear space around it at least as tall as its first letter.
- A design variant can bring its own logo the same way. Put the files in the `images` folder.

## Layout and spacing

- Steps: 4, 8, 16, 24, 32, 48, 64. Section padding 64 to 112px.
- Radius: 4 small details, 8 buttons and fields, 14 cards, pill for badges.
- Phone first. Pills stay on one line. Buttons stay full width on phones.

## Do and don't

- Do keep one gold button per view, all copy exactly as written, every image with real alt text.
- Do not use the old lime, ice-blue or Clean White (red and navy) styles on this site.
- Do not put text over faces. Do not add a second gold button next to the first.
- Do not turn off the reduced-motion fallbacks.

## Open questions for the owner

- Is the hero star background wanted on every page or only the home page?
- Light sections: stay white, or all dark?
- Final logo file (the 3D gold and chrome wordmark) and where it appears.

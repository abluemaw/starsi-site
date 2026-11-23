# How to change the StarSI website with ChatGPT

**You ask ChatGPT for a change. It goes live about a minute later. Nobody has to approve it.**

**Quick links**
- Live site: https://abluemaw.github.io/starsi-site/
- Design system: https://abluemaw.github.io/starsi-site/design/
- All designs, each as its own page: https://abluemaw.github.io/starsi-site/designs/
- Version history (restore any version): https://abluemaw.github.io/starsi-site/versions/
- Repo and buttons: https://github.com/abluemaw/starsi-site and its **Actions** tab

---

## Part 1: One-time setup (10 minutes)

**Step 1. Make a free GitHub account**
1. Go to https://github.com/signup and sign up.
2. Send Amen your GitHub username.

**Step 2. Accept the invitation**
1. Amen adds you to the site. GitHub emails you an invitation.
2. Open the email and click **View invitation**, then **Accept invitation**.

**Step 3. Connect ChatGPT to GitHub**
1. Open ChatGPT and choose **Codex** in the left menu.
   (If you don't see Codex, your ChatGPT plan may not include it. Tell Amen and use "Plan B" below.)
2. Click **Connect to GitHub** and approve.
3. When it asks which repositories to allow, choose **starsi-site**.
4. Pick `starsi-site` as your project.

You never have to do Part 1 again.

---

## Part 2: Making a change (every time)

1. Open Codex and make sure `starsi-site` is selected.
2. Type what you want, in plain words. Good examples:
   - "Change the headline at the top to: Fill Your Mats Every Week"
   - "On the Pricing page, change the special offer from $195 to $175 a month"
   - "Make the 'Book My Free Demo' buttons green"
   - "Add a new card called 'Easy Setup' to the six cards under Grow Your Profits, with this text: ..."
3. Wait for it to finish. It will show you what it changed.
4. Click **Create PR** (or **Open pull request**).
5. Wait about one minute. The change is merged and published for you, with no one approving it.
6. Open https://abluemaw.github.io/starsi-site/ and refresh the page (hold Shift and click reload) to see your change.

**Tips**
- Ask for one change at a time. Small changes are easy to check and easy to undo.
- Paste the exact words you want. ChatGPT is told not to rewrite your wording.
- Check the page on your phone too.
- If two people change the same section at the same moment, the second change may need to be asked for again. Tell ChatGPT "the site changed, please redo my change on the latest version."

---

## Part 3: Looks and designs (colours, fonts, logo)

The look of the site lives in one design file, **DESIGN.md**. The site, the design page and every design variant are built from it.

**Change the look for everyone (the "live design")**
- Ask ChatGPT: "Change the live design: make the gold deeper" or "use rounder buttons". It edits `DESIGN.md`, and the site and the design page update together in about a minute.

**Make your own look without touching anyone else's**
1. Ask ChatGPT: "Create my own design variant called `erin` with deeper gold, rounder buttons and a navy page."
2. It adds one small file, `designs/erin.md`, and nothing else. After about a minute it shows up in the **Look** dropdown at the top of the site, on the design page, and in the gallery at /designs/.
3. Pick it in the **Look** dropdown to see the whole site wearing it. Only you see it, and the browser remembers your choice. You can also share a link, for example `https://abluemaw.github.io/starsi-site/?design=erin`.
4. Every design also gets its own page (`/designs/erin/`) and its own design system page (`/designs/erin/system/`) with its colours, fonts, buttons, icons and logo.
5. To change your design later, say "update my design `erin`: make the headings white".

**Make a design live for everybody**
- On GitHub, open the repo's **Actions** tab, choose **Make a design live**, click **Run workflow**, type the name (like `erin`) and click the green button. Ask Amen if you're not sure. It can be undone from the version history.

**Logo and fonts:** A design can have its own logo and fonts. Ask ChatGPT, for example: "In my design `erin`, use the logo file images/erin-logo.svg." Put logo files in the `images` folder.

**Tell ChatGPT which one you mean**
- "my own design", "a variant" -> it makes a file in `designs/` (safe).
- "the live design", "the live site look" -> it edits `DESIGN.md` (everyone sees it).
- Wording or layout changes ("change the headline") have nothing to do with the look: ChatGPT edits a file in `sections/`.

---

## Pictures

- Pictures are files in the **images** folder, never pasted into the page as text. Ask ChatGPT: "Add the picture I attached to the Benefits section" and it saves it in `images/` and links it.
- Use WebP or JPG and keep each picture under about 300 KB so the site stays fast. Photos should follow the school rules: action, smiling, looking at the camera, no text over faces.
- If ChatGPT can't attach a picture: open https://github.com/abluemaw/starsi-site/tree/main/images, click **Add file**, then **Upload files**, drop the picture in and click **Commit changes**.

---

## Buttons on GitHub (Actions tab)

Open https://github.com/abluemaw/starsi-site/actions, pick a name on the left, click **Run workflow**.
- **Save this version:** gives the live site a name (for example `before-new-prices`) so you can come back to it.
- **Restore the site:** type a saved name or a version code and the site goes back to it. Nothing is lost; the restore is a new entry in the history.
- **Make a design live:** see Part 3.
- You can also restore from the picture page: https://abluemaw.github.io/starsi-site/versions/ (click **Restore this version**).

---

## Something went wrong? Undo it

Tell Codex: **"Undo the last change to the site"** and create the PR the same way. Or use **Restore the site** (see "Buttons on GitHub" above), or the **Restore this version** button on the version history page.
Still stuck? Message Amen. Nothing is ever lost, because every version is saved.

---

## Plan B: if Codex isn't available (copy and paste)

1. Open the sections folder: https://github.com/abluemaw/starsi-site/tree/main/sections
   Each section of the page is its own file (for example `76-pricing.html` is the Pricing page and `40-calculator.html` is the income calculator). Click the one you want. Do not use `index.html`: it is built automatically and your change would be lost.
2. Click the **pencil icon** (top right of the file) to edit.
3. Press **Ctrl+F** (or **Cmd+F** on a Mac) and search for a few words from the part you want to change.
4. Change the words, or paste in new text from ChatGPT. Only change the words, not the symbols like `<` and `>`.
5. Click **Commit changes** (green button, top right), keep **Commit directly to the main branch** selected, and click **Commit changes** again.
6. The live site updates in about a minute.

---

## Rules of the road
- Looks: see Part 3. "My own design" = a safe file in `designs/`. "The live design" = `DESIGN.md`, which everybody sees.
- Never edit `index.html` yourself. Each section has its own file in the `sections` folder.
- Keep the owner's wording exactly as given.
- Don't add trackers, sign-up forms, or outside services without asking Amen.
- The testimonials and the "[BONUS GIFT]" line are still waiting for Amen's confirmation. Leave those as they are unless Amen says otherwise.

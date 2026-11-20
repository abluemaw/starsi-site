# How to change the StarSI website with ChatGPT

**The live site:** https://abluemaw.github.io/starsi-site/
**The design system (colours, fonts, buttons, light and dark):** https://abluemaw.github.io/starsi-site/design/
**All designs (each look as its own page):** https://abluemaw.github.io/starsi-site/designs/
**Version history (pictures of every change, with restore):** https://abluemaw.github.io/starsi-site/versions/
**The design file ChatGPT edits for design changes:** https://github.com/abluemaw/starsi-site/blob/main/DESIGN.md
**You ask ChatGPT for a change. It goes live about a minute later. Nobody has to approve it.**

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
   - "In the testimonials section, change Mike Bugg's title to Grandmaster"
   - "Make the 'Book My Free Demo' buttons green"
   - "Add a new benefit card called 'Easy Setup' with this text: ..."
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

## Something went wrong? Undo it

Tell Codex: **"Undo the last change to the site"** and create the PR the same way.
Still stuck? Message Amen. Nothing is ever lost, because every version is saved.

---

## Plan B: if Codex isn't available (copy and paste)

1. Open the sections folder: https://github.com/abluemaw/starsi-site/tree/main/sections
   Each section of the page is its own file (for example `30-benefits.html` is the Benefits cards). Click the one you want. Do not use `index.html`: it is built automatically and your change would be lost.
2. Click the **pencil icon** (top right of the file) to edit.
3. Press **Ctrl+F** (or **Cmd+F** on a Mac) and search for a few words from the part you want to change.
4. Change the words, or paste in new text from ChatGPT. Only change the words, not the symbols like `<` and `>`.
5. Click **Commit changes** (green button, top right), keep **Commit directly to the main branch** selected, and click **Commit changes** again.
6. The live site updates in about a minute.

---

## Rules of the road
- To change the look (colours, fonts, spacing), ask ChatGPT to change the value in `DESIGN.md`. The site and the design page at /design/ update together.
- Want your own version of the look? Ask ChatGPT: "create my own design variant called <name> with <changes>". Then pick it in the **Look** dropdown at the top of the site (or open the site with `?design=<name>`). It never changes what everyone else sees. To make one live for everybody, ask Amen to run **Actions > Make a design live**.
- Never edit `index.html` yourself. Each section has its own file in the `sections` folder.
- Keep the owner's wording exactly as given.
- Don't add trackers, sign-up forms, or outside services without asking Amen.
- The testimonials and the "[BONUS GIFT]" line are still waiting for Amen's confirmation. Leave those as they are unless Amen says otherwise.

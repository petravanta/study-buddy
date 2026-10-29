# Adding a question set

Built-in question sets are plain JSON files, so you can add one without touching the app's code.

1. **Pick an id**: lowercase letters, digits and hyphens, like `uk-driving-theory-signs`. It can never change once the set is published, because everyone's answer history refers to it.
2. **Create `data/sets/<id>.json`.** The quickest way is to build the set in the app (*Sets → + Add a set*, import a CSV or write the questions), then use **Export → Download JSON** and copy the `set` part of that file. Change its `id` to the one you picked. Or copy [`data/sets/us-civics-2008.json`](data/sets/us-civics-2008.json) and edit it.
3. **Fill in each question**:
   - `id`: short and stable within the set (`q1`, `q2`, …). Never reuse or renumber one that has shipped.
   - `prompt`: the question as it is asked.
   - `answers`: every answer that counts as right. Words in (brackets) are optional when someone types the answer.
   - `personal` (instead of `answers`), for a question whose answer is different for everyone, like “What is the capital of your state?”: `{ "ask": "Your state’s capital", "hint": "where to look it up, and special cases" }`. The app asks each person for their answer before they practise.
   - `need` (optional): how many answers someone must give, for "Name two…" questions.
   - `wrong` (optional): wrong answers for multiple choice. Plausible ones make the practice much better.
   - `explanation` and `note` (optional): why the answer is right, or a caution, such as an answer that changes after an election.
   - `figure` (optional): a picture the question asks about, `{ "src": "data/figures/<file>.png", "alt": "what it shows" }`. Put the image in `data/figures/` and add it to `APP_SHELL` in `sw.js` too. Add `"reveal": true` for a picture that gives the answer away, so it only shows with the answer. For an image you didn't make, say where it's from and its licence: `credit`, `source` (link), `license` and `licenseUrl`; only use openly licensed or public domain images.
   - `tags` (optional): topics, so practice tests can focus on some of them.
4. **A chapter of a bigger subject** (like *Human anatomy*) gets `"module": "Human anatomy"`. Chapters of one module are offered together, in `data/sets.json` order.
5. **Say where it comes from** in `source` (a name and a link) and set `updated` to the day you checked the answers.
6. **Suggest practice tests** in `tests` that match how the real test works: how many questions, the pass mark as a percentage, and whether it ends early.
7. **Add the id to `data/sets.json`**, in the order sets should be listed, and to the `APP_SHELL` list in `sw.js` (`data/sets/<id>.json`) so it works offline.
8. **Open a pull request.** The `Check data` check makes sure the file matches [the schema](data/schema/sets.schema.json) and that ids are unique. To run it yourself:

   ```sh
   npx ajv-cli@5 validate --spec=draft7 --all-errors -s data/schema/sets.schema.json -d data/sets/<id>.json
   node scripts/check-data.js
   ```

Only add questions whose wording you're allowed to share, such as official government study material.

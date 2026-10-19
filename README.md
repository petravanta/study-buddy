# Study Buddy

Study for flash-card style knowledge tests, like the U.S. citizenship civics test or a driving theory test. Practise with flashcards, set up practice tests that work like the real one, and keep a history of every answer you give to every question.

## Try it

**[Open Study Buddy → petravanta.github.io/study-buddy](https://petravanta.github.io/study-buddy/)**

1. **Start a programme** for the test you're preparing for. Pick a built-in set (the *U.S. citizenship civics test (2008 version)*, the Washington State motorcycle knowledge tests for 2-wheel and 3-wheel endorsements, or the official question pools for the amateur radio Technician, General and Extra licence exams), or start from scratch and bring your own questions. Add an exam date to see a countdown.
2. **Practise with flashcards.** Choose how many cards, which ones (weakest first, random, new ones first, only the ones you missed, or in order) and how you answer: flip the card and mark yourself, pick from multiple choice, or type the answer.
3. **Take practice tests.** Each programme has its own test types. The civics set comes with *Civics interview*: 10 questions, pass with 6, and it ends as soon as you've passed or can no longer pass, like the real interview.
4. **See where you stand.** Every question shows how well you know it (New, Learning, Getting there, Confident, Mastered), how often you got it right and every answer you ever gave. *History* lists every practice test with its score and whether you passed.

## What it does

- **Several programmes at once**, each with its own sets, practice tests and exam date. Finished ones can be archived; they keep their history.
- **History for every question.** Every answer is kept, flashcards and tests alike, with when, how you answered and (for typed and multiple choice answers) what you said. A question's history follows it into any programme that uses the same set. **Export answers (CSV)** in *History* downloads all of it.
- **Practice tests you define**: number of questions (or all of them), pass mark as a percentage, which questions, how you answer, whether you see right or wrong after each question or only at the end, a time limit, ending early once the result is settled, and limiting it to some topics.
- **Questions with your own answer.** Some answers are different for everyone, like the civics test’s “Who is one of your state’s U.S. Senators now?”. These ask for your answer before you first practise (or later, from the banner on *Practice* or the question itself), with a hint on where to look it up, and then work like any other question. Your answers stay in your own data and are never in an exported set.
- **Typed answers** forgive capital letters, punctuation, words in (brackets) and small typos, but numbers have to match. If it marks you wrong when you were right (or the other way round), one tap changes it.
- **Multiple choice** uses a question's own wrong answers when it has them, and otherwise borrows answers from other questions in the set, preferring the same topic and the same kind of answer (a date for a date).
- **Import and export sets** (see below), backups, and optional Google Drive sync.
- Installs on a phone (Chrome: *Install app*; iPhone: *Share → Add to Home Screen*) and opens offline.
- Light and dark themes, the shared **All apps** link and theme switch, and a phone-first layout, as the [shared standards](https://github.com/petravanta/general/blob/main/STANDARDS.md) describe.

Keyboard: in flashcards, **Space** shows the answer, then **Y** or **1** if you knew it and **N** or **2** if you didn't. In multiple choice, **1** to **4** pick an answer. **Enter** goes to the next question.

## Importing and exporting question sets

*Sets → + Add a set* takes:

- **CSV** with a header row. Columns: `question`, `answer`, `need`, `wrong`, `explanation`, `note`, `tags`, `personal`. Only `question` and `answer` are required. For a question everyone answers for themselves, leave `answer` empty and put what to ask for in `personal` (e.g. *Your state’s capital*). Separate several answers that all count (or several wrong answers, or several tags) with `|`. `need` is how many answers you must give, for questions like "Name two…". The app offers a template to download.
- **Tab-separated text**, such as a Quizlet export (term, a tab, definition, one per line), as a file or pasted in.
- **CSV without a header**: the first column is the question and the second the answer.
- **A Study Buddy set file** (`.json`), the format **Export** writes:

  ```json
  {
    "format": "study-buddy-set",
    "formatVersion": 1,
    "set": {
      "id": "road-signs",
      "name": "Road signs",
      "questions": [
        { "id": "q1", "prompt": "What does a red octagonal sign mean?", "answers": ["Stop"], "wrong": ["Yield", "No entry"], "tags": ["Signs"] }
      ],
      "tests": [
        { "name": "Theory test", "count": 30, "pass": 83, "pick": "random", "answer": "choice", "feedback": "end", "stopEarly": false, "timeLimit": 30 }
      ]
    }
  }
  ```

  `set` has the same shape as the built-in sets ([schema](data/schema/sets.schema.json)). Importing a set you exported earlier offers to update it in place, so your history stays matched to its questions.

An exported set holds the questions and the programme's practice tests, never your answers, and the app shows everything in it before it downloads.

## Your data

Nothing is uploaded. Programmes, your own sets, test results and every answer are kept in your browser (`localStorage`). **Settings → Export backup** downloads all of it as one JSON file, and **Import backup** merges one back in. **Settings → Connect Google Drive** keeps a copy in `Study Buddy data.json` in your own Drive, using the `drive.file` permission so the app only ever sees that one file, and merges it with the browser copy on connect and whenever the app comes back into view. All of this follows the *User data* section of the shared standards. Drive uses the shared OAuth client for `https://petravanta.github.io` (`GOOGLE_CLIENT_ID` in the script).

## Extending the app

| Dataset | File | Schema | What it controls |
| --- | --- | --- | --- |
| Question sets | `data/sets.json` (the list) and `data/sets/<id>.json` (one per set) | [`data/schema/sets.schema.json`](data/schema/sets.schema.json) | The built-in sets offered when starting a programme or adding a set, with their questions, accepted answers and suggested practice tests |

[`CONTRIBUTING.md`](CONTRIBUTING.md) explains how to add a set. The `Check data` workflow validates every set against the schema and runs [`scripts/check-data.js`](scripts/check-data.js) on each pull request.

The civics set is the USCIS 2008 civics test. The four questions about where you live (your Senators, Representative, Governor and state capital) are personal questions you fill in. Questions whose answer changes with elections or appointments carry a note to check [uscis.gov/citizenship/testupdates](https://www.uscis.gov/citizenship/testupdates) before the interview. People who filed on or after October 20, 2025 take the 2025 version of the test; it can be imported as your own set, or added here as a second built-in set.

The two Washington motorcycle sets are written from the WA DOL [Motorcycle Operator Manual](https://dol.wa.gov/driver-licenses-and-permits/motorcycle/motorcycle-endorsement-training-and-testing/motorcycle-operator-manual), since DOL does not publish its test questions. Every question has three wrong answers for multiple choice. Their practice tests copy the format in the Washington Motorcycle Safety Program's Policies and Procedures Manual (v.2022): the 2-wheel permit knowledge test is 50 questions with 80% to pass (no more than 10 wrong), the 2-wheel endorsement knowledge test is 25 questions with 68% (no more than 8 wrong), and the 3-wheel permit or endorsement knowledge test is 25 questions with 80% (no more than 5 wrong). Both sets share the licensing, gear, inspection, road strategy, passenger, group riding and impairment questions; the 2-wheel set adds riding skills and the 3-wheel set adds trike and sidecar handling.

## Running it

It is a single static file, `index.html`, with no build step. Serve the folder (`python3 -m http.server`) and open it; the built-in sets load with `fetch()`, so opening the file directly won't show them. GitHub Pages serves it from `main`, root folder.

// Checks what the JSON Schemas can't: every listed set has a file whose id matches its name, ids are unique,
// and a question needing N answers has at least N. Run: node scripts/check-data.js
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', 'data');
const errors = [];
const list = JSON.parse(fs.readFileSync(path.join(dir, 'sets.json'), 'utf8'));
if (!Array.isArray(list)) errors.push('data/sets.json must be an array of set ids');
if (new Set(list).size !== list.length) errors.push('data/sets.json lists a set twice');
const files = fs.readdirSync(path.join(dir, 'sets')).filter(f => f.endsWith('.json'));
for (const f of files) if (!list.includes(f.replace(/\.json$/, ''))) errors.push(`data/sets/${f} is not listed in data/sets.json`);
for (const id of list) {
  const file = path.join(dir, 'sets', id + '.json');
  if (!fs.existsSync(file)) { errors.push(`data/sets.json lists ${id} but data/sets/${id}.json is missing`); continue; }
  const set = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (set.id !== id) errors.push(`data/sets/${id}.json has id "${set.id}"`);
  const seen = new Set();
  for (const q of set.questions || []) {
    if (seen.has(q.id)) errors.push(`${id}: question id ${q.id} is used twice`);
    seen.add(q.id);
    if (q.need && q.need > q.answers.length) errors.push(`${id}/${q.id}: needs ${q.need} answers but lists ${q.answers.length}`);
  }
  for (const t of set.tests || []) if (t.tags) for (const tag of t.tags)
    if (!(set.questions || []).some(q => (q.tags || []).includes(tag))) errors.push(`${id}: test "${t.name}" asks for tag "${tag}", which no question has`);
}
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
console.log(`data ok: ${list.length} set(s)`);

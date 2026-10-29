// Serves this folder, opens index.html in headless Chromium and saves one PNG per job: node shoot.js jobs.json out
const { chromium } = require('playwright'); const fs = require('fs'); const http = require('http'); const path = require('path');
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')), out = process.argv[3];
const root = __dirname;
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html' : 'application/octet-stream' }); r.end(d); }); }).listen(8765);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage(); p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('err', e.message));
  await p.goto('http://localhost:8765/index.html'); await p.waitForFunction('window.ready', null, { timeout: 300000 });
  fs.mkdirSync(out, { recursive: true });
  for (const [name, job] of Object.entries(jobs)) {
    const url = await p.evaluate(j => window.shot(j), job);
    fs.writeFileSync(path.join(out, name + '.png'), Buffer.from(url.split(',')[1], 'base64')); console.log('shot', name);
  }
  await b.close(); srv.close();
})();

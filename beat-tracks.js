/* Backing tracks for the count-along beat (see `beatBlock()` in index.html).
   Everything is synthesised with Web Audio, so there are no audio files: each track is a `step(B, n, t, st)` function
   called once per sixteenth note (n counts from 0, t is its start time) that schedules drums, bass, pads and so on
   on the bus B. A style (a question's `beat.style`) has a few tracks, and every style ends with "Just the click". */
(function (root) {
  'use strict';
  const mtof = m => 440 * Math.pow(2, (m - 69) / 12);
  // A repeatable "random" number for step n, so patterns vary but every loop sounds the same.
  const rnd = (n, k = 0) => { const x = Math.sin(n * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };

  // Noise, a reverb impulse and distortion curves, made once per audio context.
  const shared = new WeakMap();
  function kit(c) {
    let s = shared.get(c); if (s) return s;
    const len = c.sampleRate * 2, noise = c.createBuffer(1, len, c.sampleRate), d = noise.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    const rl = Math.floor(c.sampleRate * 2.8), imp = c.createBuffer(2, rl, c.sampleRate);
    for (let ch = 0; ch < 2; ch++) { const x = imp.getChannelData(ch); for (let i = 0; i < rl; i++) x[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / rl, 3.2); }
    const curves = {};
    s = { noise, imp, curve(k) {
      if (curves[k]) return curves[k];
      const a = new Float32Array(1024);
      for (let i = 0; i < 1024; i++) { const x = i / 511.5 - 1; a[i] = (1 + k) * x / (1 + k * Math.abs(x)); }
      return (curves[k] = a);
    } };
    shared.set(c, s); return s;
  }

  // The bus: dry out, a reverb send, a tempo-synced (dotted eighth) delay send and a chorus, into a gentle compressor.
  function bus(c, bpm, dest) {
    const S = kit(c), sx = 60 / bpm / 4, t0 = c.currentTime, lfos = [];
    const master = c.createGain(), comp = c.createDynamicsCompressor();
    comp.threshold.value = -16; comp.ratio.value = 6; comp.attack.value = 0.004; comp.release.value = 0.2;
    master.gain.setValueAtTime(0.0001, t0); master.gain.setTargetAtTime(0.6, t0, 0.02);
    master.connect(comp).connect(dest);
    const out = c.createGain(); out.connect(master);
    const rev = c.createGain(), conv = c.createConvolver(), wet = c.createGain();
    conv.buffer = S.imp; wet.gain.value = 0.8; rev.connect(conv).connect(wet).connect(master);
    const dly = c.createGain(), dl = c.createDelay(2), fb = c.createGain(), lp = c.createBiquadFilter(), dr = c.createGain();
    dl.delayTime.value = sx * 3; fb.gain.value = 0.38; lp.type = 'lowpass'; lp.frequency.value = 2600; dr.gain.value = 0.3;
    dly.connect(dl).connect(lp).connect(fb).connect(dl); lp.connect(master); lp.connect(dr).connect(rev);
    const cho = c.createGain(); cho.connect(out);
    [0, 1].forEach(i => {
      const d = c.createDelay(0.05), lfo = c.createOscillator(), depth = c.createGain(), g = c.createGain();
      d.delayTime.value = 0.011 + i * 0.007; lfo.frequency.value = 0.45 + i * 0.32; depth.gain.value = 0.0025; g.gain.value = 0.8;
      lfo.connect(depth).connect(d.delayTime); lfo.start(t0); lfos.push(lfo);
      let o = cho.connect(d).connect(g);
      if (c.createStereoPanner) { const p = c.createStereoPanner(); p.pan.value = i ? 0.7 : -0.7; o = o.connect(p); }
      o.connect(out);
    });
    return { c, S, sx, master, out, rev, dly, cho, lfos };
  }

  // Send a voice to the bus: o.dry (1 by default), o.rev, o.dly and o.cho are send levels, o.pan places it.
  function route(B, node, o) {
    let src = node;
    if (o.pan && B.c.createStereoPanner) { const p = B.c.createStereoPanner(); p.pan.value = o.pan; node.connect(p); src = p; }
    const to = (dest, g) => { if (!g) return; if (g === 1) { src.connect(dest); return; } const x = B.c.createGain(); x.gain.value = g; src.connect(x).connect(dest); };
    to(B.out, o.dry === undefined ? 1 : o.dry); to(B.rev, o.rev); to(B.dly, o.dly); to(B.cho, o.cho);
  }
  function noise(B, t, dur) { const n = B.c.createBufferSource(); n.buffer = B.S.noise; n.loop = true; n.start(t, Math.random() * 1.5); n.stop(t + dur + 0.05); return n; }

  // ---- Drums ----
  function kick(B, t, o = {}) {
    const c = B.c, os = c.createOscillator(), g = c.createGain(), dec = o.dec || 0.4;
    os.frequency.setValueAtTime(o.f0 || 150, t); os.frequency.exponentialRampToValueAtTime(o.f1 || 48, t + (o.sweep || 0.09));
    g.gain.setValueAtTime(o.g || 0.9, t); g.gain.exponentialRampToValueAtTime(0.001, t + dec);
    let last = os.connect(g);
    if (o.drive) { const w = c.createWaveShaper(), post = c.createGain(); w.curve = B.S.curve(o.drive); post.gain.value = 0.7; last = g.connect(w).connect(post); }
    route(B, last, o); os.start(t); os.stop(t + dec + 0.02);
    if (o.click) hit(B, t, { f: 3000, g: o.click, dec: 0.012 });
  }
  // Filtered noise: hats, shakers, snare bodies, hiss.
  function hit(B, t, o) {
    const c = B.c, n = noise(B, t, o.dec), f = c.createBiquadFilter(), g = c.createGain();
    f.type = o.type || 'highpass'; f.frequency.value = o.f || 7500; f.Q.value = o.q || 0.7;
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(o.g, t + (o.a || 0.002)); g.gain.exponentialRampToValueAtTime(0.001, t + o.dec);
    n.connect(f).connect(g); route(B, g, o);
  }
  const hat = (B, t, g, open, pan) => hit(B, t, { g, dec: open ? 0.22 : 0.045, f: open ? 6500 : 8000, pan });
  function snare(B, t, o = {}) {
    hit(B, t, { type: 'bandpass', f: o.f || 1800, q: 0.7, g: o.g || 0.45, dec: o.dec || 0.18, rev: o.rev, pan: o.pan });
    const c = B.c, os = c.createOscillator(), g = c.createGain();
    os.type = 'triangle'; os.frequency.setValueAtTime(o.tone || 200, t); os.frequency.exponentialRampToValueAtTime((o.tone || 200) * 0.75, t + 0.08);
    g.gain.setValueAtTime((o.g || 0.45) * 0.7, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
    os.connect(g); route(B, g, { rev: o.rev }); os.start(t); os.stop(t + 0.12);
  }
  function clap(B, t, o = {}) {
    [0, 0.011, 0.022].forEach(d => hit(B, t + d, { type: 'bandpass', f: 1300, q: 1.2, g: (o.g || 0.35) * 0.7, dec: 0.02 }));
    hit(B, t + 0.03, { type: 'bandpass', f: 1300, q: 1, g: o.g || 0.35, dec: 0.17, rev: o.rev === undefined ? 0.2 : o.rev });
  }
  function tom(B, t, f, g, rev) {
    const c = B.c, os = c.createOscillator(), e = c.createGain();
    os.frequency.setValueAtTime(f * 1.6, t); os.frequency.exponentialRampToValueAtTime(f, t + 0.08);
    e.gain.setValueAtTime(g, t); e.gain.exponentialRampToValueAtTime(0.001, t + 0.45);
    os.connect(e); route(B, e, { rev: rev || 0.25 }); os.start(t); os.stop(t + 0.5);
    hit(B, t, { type: 'bandpass', f: f * 4, q: 1, g: g * 0.25, dec: 0.06 });
  }
  // Inharmonic square waves (the 808 cymbal ratios): metal hits, anvils, clangs.
  function metal(B, t, o) {
    const c = B.c, g = c.createGain(), bp = c.createBiquadFilter(), f = o.f || 400, dec = o.dec || 0.3;
    bp.type = 'bandpass'; bp.frequency.value = o.bp || f * 6; bp.Q.value = 0.9;
    [1, 1.342, 1.2312, 1.6532, 1.9523, 2.1523].forEach(r => { const os = c.createOscillator(); os.type = 'square'; os.frequency.value = f * r; os.connect(bp); os.start(t); os.stop(t + dec + 0.05); });
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(o.g, t + 0.002); g.gain.exponentialRampToValueAtTime(0.001, t + dec);
    bp.connect(g); route(B, g, o);
  }
  // A noise sweep: risers (f0 low, f1 high) and wind.
  function sweep(B, t, dur, o) {
    const c = B.c, n = noise(B, t, dur), f = c.createBiquadFilter(), g = c.createGain();
    f.type = 'bandpass'; f.Q.value = o.q || 3; f.frequency.setValueAtTime(o.f0, t); f.frequency.exponentialRampToValueAtTime(o.f1, t + dur);
    g.gain.setValueAtTime(0.0001, t);
    if (o.swell) { g.gain.linearRampToValueAtTime(o.g, t + dur / 2); g.gain.linearRampToValueAtTime(0.0001, t + dur); }
    else { g.gain.linearRampToValueAtTime(o.g, t + dur * 0.97); g.gain.linearRampToValueAtTime(0.0001, t + dur); }
    n.connect(f).connect(g); route(B, g, o);
  }

  // ---- Tones ----
  // One note: o.voices detuned oscillators (o.spread cents apart) into a filter with its own envelope (cut + env,
  // falling over fdec), optional drive, and an ADSR (a, d, s, r). o.from slides in from another note, o.bend dives
  // down o.bend semitones.
  function synth(B, t, dur, midi, o = {}) {
    const c = B.c, n = o.voices || 1, f = c.createBiquadFilter(), g = c.createGain();
    const a = o.a || 0.005, d = o.d || 0.1, s = o.s === undefined ? 0.7 : o.s, r = o.r || 0.08, v = o.g || 0.2, cut = o.cut || 2000;
    f.type = 'lowpass'; f.Q.value = o.q || 0.7;
    f.frequency.setValueAtTime(cut + (o.env || 0), t);
    if (o.env) f.frequency.exponentialRampToValueAtTime(cut, t + (o.fdec || 0.15));
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + a);
    g.gain.setTargetAtTime(v * s, t + a, d / 3); g.gain.setTargetAtTime(0, Math.max(t + dur, t + a), r / 4);
    const hz = mtof(midi);
    for (let i = 0; i < n; i++) {
      const os = c.createOscillator();
      os.type = o.wave || 'sawtooth'; os.detune.value = n > 1 ? (i / (n - 1) - 0.5) * 2 * (o.spread || 10) : 0;
      if (o.from !== undefined) { os.frequency.setValueAtTime(mtof(o.from), t); os.frequency.exponentialRampToValueAtTime(hz, t + 0.06); }
      else if (o.bend) { os.frequency.setValueAtTime(mtof(midi + o.bend), t); os.frequency.exponentialRampToValueAtTime(hz, t + 0.14); }
      else os.frequency.setValueAtTime(hz, t);
      os.connect(f); os.start(t); os.stop(t + dur + r + 0.1);
    }
    let last = f;
    if (o.drive) { const w = c.createWaveShaper(); w.curve = B.S.curve(o.drive); last = f.connect(w); }
    last.connect(g); route(B, g, o);
  }
  const chord = (B, t, dur, notes, o) => notes.forEach((m, i) => synth(B, t, dur, m, Object.assign({}, o, o.pan ? { pan: i % 2 ? o.pan : -o.pan } : {})));

  // Chords as MIDI notes.
  const Am = [57, 60, 64], C = [55, 60, 64], Dm = [62, 65, 69], E = [56, 59, 64], F = [53, 57, 60], G = [55, 59, 62],
    Bb = [58, 62, 65], A = [57, 61, 64], Em = [52, 55, 59], Cl = [48, 52, 55], D = [50, 54, 57];

  const STYLES = {
    basics: [
      { name: 'Sunny house', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, ch = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]][b % 4];
        if (s % 4 === 0) kick(B, t, { g: 0.85 });
        if (s === 4 || s === 12) clap(B, t, { g: 0.32 });
        if (s % 4 === 2) hat(B, t, 0.11, true, 0.2); else if (s % 2) hat(B, t, 0.04, false, -0.2);
        if (s % 4 === 2) synth(B, t, sx * 1.6, ch[0] - 12, { cut: 380, env: 700, fdec: 0.12, g: 0.3, s: 0.5 });
        if (s === 3 || s === 6 || s === 11) chord(B, t, sx * 1.2, ch.map(m => m + 12), { wave: 'triangle', cut: 3200, env: 2000, fdec: 0.1, g: 0.055, d: 0.15, s: 0.3, r: 0.2, dly: 0.25, rev: 0.2, pan: 0.2 });
        if (b % 2 && s === 14) synth(B, t, sx * 2, ch[3] + 24, { wave: 'sine', g: 0.06, d: 0.3, s: 0, r: 0.3, dly: 0.45, rev: 0.3, pan: 0.4 });
      } },
      { name: 'Funk pop', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, two = (b >> 1) % 2, root = two ? 50 : 45;
        const ch = two ? [54, 57, 60, 64] : [55, 60, 64, 67];
        if (s === 0 || s === 7 || s === 10) kick(B, t, { g: 0.8 });
        if (s === 4 || s === 12) snare(B, t, { g: 0.42, rev: 0.12 });
        if (s === 15) snare(B, t, { g: 0.07 });
        hat(B, t, s % 2 ? 0.035 : 0.08, false, 0.15);
        const line = { 0: 0, 3: 0, 6: 12, 7: 10, 8: 7, 11: 3, 13: 5, 14: 7 };
        if (s in line) synth(B, t, sx * 0.9, root - 12 + line[s], { wave: 'square', cut: 600, env: 1500, fdec: 0.07, g: 0.2, s: 0.4, from: s === 7 ? root : undefined });
        if ([2, 6, 9, 14].includes(s)) chord(B, t, sx * 0.5, ch, { wave: 'square', cut: 2200, q: 3, env: 1500, fdec: 0.05, g: 0.03, s: 0.3, pan: 0.3 });
        if (b % 2 && s % 4 === 0) synth(B, t, sx * 2, [69, 72, 74, 76, 79, 81][Math.floor(rnd(n, 3) * 6)], { wave: 'sine', g: 0.05, d: 0.3, s: 0, r: 0.3, dly: 0.35, rev: 0.25, pan: -0.4 });
      } },
      { name: 'Disco strings', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, ch = [[50, 53, 57, 60], [55, 59, 62, 65], [48, 52, 55, 59], [45, 48, 52, 55]][b % 4];
        if (s % 4 === 0) kick(B, t, { g: 0.85 });
        if (s === 4 || s === 12) { snare(B, t, { g: 0.3 }); clap(B, t, { g: 0.22 }); }
        if (s % 4 === 2) hat(B, t, 0.13, true, 0.25); else hat(B, t, 0.03, false, -0.25);
        if (s % 2 === 0) synth(B, t, sx * 1.4, ch[0] - 12 + (s % 4 === 2 ? 12 : 0), { cut: 500, env: 900, fdec: 0.08, g: 0.22, s: 0.4 });
        if (s === 0) chord(B, t, sx * 15, ch.map(m => m + 12), { voices: 3, spread: 12, cut: 2200, a: 0.25, d: 0.5, s: 0.8, r: 0.5, g: 0.028, rev: 0.35, pan: 0.4 });
        if (b % 4 === 3 && s >= 12) synth(B, t, sx * 0.9, ch[s - 12] + 24, { wave: 'triangle', g: 0.05, d: 0.2, s: 0.2, dly: 0.2, rev: 0.3 });
      } },
    ],
    goth: [
      { name: 'Batcave', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, ch = [Em, Em, Cl, D][b % 4];
        if (s === 0) kick(B, t, { g: 0.9, f1: 45, dec: 0.45 });
        if (s === 10) kick(B, t, { g: 0.55, f1: 45 });
        if (s === 8) snare(B, t, { g: 0.5, f: 1500, dec: 0.3, rev: 0.5 });
        if (s === 2 || s === 6) tom(B, t, 85, 0.32);
        if (b % 4 === 3 && s >= 12) tom(B, t, [180, 150, 120, 95][s - 12], 0.38);
        if (s % 2 === 0) hat(B, t, s % 4 ? 0.05 : 0.03, false, 0.3);
        if (s % 2 === 0) synth(B, t, sx * 1.8, ch[0] - 12, { cut: 550, env: 900, fdec: 0.1, g: s === 0 ? 0.3 : 0.24, s: 0.3, drive: 2 });
        if (s % 2 === 0) { const g = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24]; synth(B, t, sx * 1.5, g[[0, 2, 1, 2, 0, 2, 1, 3][s / 2]], { cut: 2600, env: 1500, fdec: 0.12, g: 0.07, d: 0.25, s: 0.15, r: 0.2, dry: 0, cho: 1, dly: 0.3, rev: 0.3 }); }
      } },
      { name: 'Coldwave', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, ch = [Am, F, [50, 53, 57], E][b % 4];
        if (s === 0) kick(B, t, { g: 0.85, dec: 0.4 });
        if (s === 6) kick(B, t, { g: 0.45 });
        if (s === 8) snare(B, t, { g: 0.48, dec: 0.25, rev: 0.6 });
        if (s % 2 === 0) hat(B, t, s % 4 ? 0.08 : 0.05, false, -0.2);
        if (s % 2 === 0) synth(B, t, sx * 1.7, ch[0] - 24 + (ch[0] < 55 ? 12 : 0), { cut: 450, env: 500, fdec: 0.1, g: 0.27, s: 0.4 });
        if (s === 0) chord(B, t, sx * 15, ch, { voices: 2, spread: 8, cut: 900, a: 0.6, d: 0.6, s: 0.9, r: 0.8, g: 0.03, rev: 0.4, pan: 0.3 });
        const mel = [76, 74, 72, 71, 69, 72, 77, 76, 74, 72, 69, 74, 76, 71, 68, 71];
        if (b % 8 >= 4 && s % 4 === 0) synth(B, t, sx * 3, mel[(b % 4) * 4 + s / 4], { wave: 'square', cut: 2200, g: 0.05, a: 0.01, d: 0.2, s: 0.5, dly: 0.35, rev: 0.3, pan: 0.2 });
      } },
      { name: 'Ethereal', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, ch = [Dm, Bb, [55, 58, 62], A][(b >> 1) % 4], arp = [ch[0], ch[1], ch[2], ch[0] + 12];
        if (s === 0) kick(B, t, { g: 0.7, dec: 0.5 });
        if (s === 8) snare(B, t, { g: 0.36, dec: 0.35, rev: 0.85 });
        if (s % 2) hit(B, t, { type: 'bandpass', f: 6000, q: 1, g: 0.03, dec: 0.05, pan: 0.3 });
        if (s === 0 && b % 2 === 0) chord(B, t, sx * 31, [ch[0] - 12, ...ch], { voices: 3, spread: 14, cut: 1100, a: 1, d: 1, s: 0.9, r: 1.5, g: 0.022, dry: 0.6, rev: 0.7, pan: 0.35 });
        if (s === 0) synth(B, t, sx * 15, ch[0] - 24 + (ch[0] < 60 ? 12 : 0), { wave: 'sine', a: 0.05, s: 0.8, r: 0.3, g: 0.28 });
        if (s % 2 === 0 && rnd(n, 7) > 0.25) synth(B, t, sx * 2, arp[(n >> 1) % 4] + 12, { wave: 'triangle', g: 0.045, a: 0.003, d: 0.3, s: 0, r: 0.3, dly: 0.55, rev: 0.5, pan: (n >> 1) % 2 ? 0.5 : -0.5 });
        if (s === 0 && b % 4 === 0) sweep(B, t, sx * 64, { f0: 400, f1: 1400, q: 2, g: 0.05, swell: true, rev: 0.5 });
      } },
    ],
    industrial: [
      { name: 'EBM', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, root = 40 + [0, 0, -4, -2][(b >> 1) % 4];
        if (s % 4 === 0) kick(B, t, { g: 0.85, f0: 170, dec: 0.3, click: 0.12 });
        if (s === 4 || s === 12) { snare(B, t, { g: 0.48, rev: 0.2 }); metal(B, t, { f: 380, dec: 0.18, g: 0.1, rev: 0.2 }); }
        if (s % 4 === 2) hat(B, t, 0.1, false, 0.2);
        if (s === 14 && b % 2) metal(B, t, { f: 260, dec: 0.5, g: 0.12, rev: 0.4, pan: -0.4 });
        if (s % 4 !== 3) synth(B, t, sx * 0.8, root + (s % 4 === 2 ? 12 : 0), { cut: 300, env: 1800, fdec: 0.07, q: 4, g: 0.26, s: 0.2, drive: 3 });
        if (s % 2 && b % 4 >= 2) synth(B, t, sx * 0.5, root + ((n >> 1) % 2 ? 31 : 24), { wave: 'square', cut: 3000, g: 0.035, s: 0.4, dly: 0.3, pan: 0.5 });
      } },
      { name: 'Aggrotech', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, ch = [Dm, Bb, [60, 64, 67], Am][b % 4], root = [38, 34, 36, 33][b % 4];
        if (s % 4 === 0 || (s === 14 && b % 2)) kick(B, t, { g: s === 14 ? 0.6 : 0.8, f0: 200, f1: 50, dec: 0.35, drive: 4 });
        if (s === 4 || s === 12) { snare(B, t, { g: 0.45 }); clap(B, t, { g: 0.28 }); }
        if (s % 4 === 2) hat(B, t, 0.09, true, 0.3); else hit(B, t, { f: 9000, g: s % 2 ? 0.05 : 0.08, dec: 0.03, pan: -0.3 });
        if (s % 4) synth(B, t, sx * 0.85, root + (s % 4 === 3 ? 12 : 0), { voices: 2, spread: 10, cut: 500, env: 2000, fdec: 0.06, q: 3, drive: 6, g: 0.12, s: 0.3 });
        if ((b % 2 ? [0, 3, 6, 10, 12] : [0, 3, 6]).includes(s)) chord(B, t, sx * 1.5, ch, { voices: 3, spread: 25, cut: 3500, env: 2000, fdec: 0.15, g: 0.028, s: 0.4, r: 0.1, rev: 0.3, dly: 0.15, pan: 0.3 });
      } },
      { name: 'Factory', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx;
        if (s % 4 === 0) kick(B, t, { g: 0.95, f0: 120, f1: 40, dec: 0.55 });
        if (s === 4 || s === 12) { hit(B, t, { type: 'bandpass', f: 900, q: 0.6, g: 0.33, dec: 0.2, rev: 0.35 }); metal(B, t, { f: 180, dec: 0.12, g: 0.09 }); }
        if (s === 6 && b % 2 === 0) metal(B, t, { f: 310, dec: 0.6, g: 0.15, rev: 0.5, pan: 0.35 });
        if (s === 14) metal(B, t, { f: 233, dec: 0.4, g: 0.11, rev: 0.4, pan: -0.35 });
        if (s % 4 && rnd((b % 4) * 16 + s, 5) > 0.55) metal(B, t, { f: 900, dec: 0.04, g: 0.045, pan: rnd(n, 9) - 0.5 });
        if (s % 2 === 0) synth(B, t, sx * 1.6, b % 4 === 3 && s >= 8 ? 29 : 28, { voices: 2, spread: 15, cut: 200 + 500 * (0.5 + 0.5 * Math.sin(n / 32)), env: 600, fdec: 0.1, drive: 8, g: 0.12, s: 0.5 });
        if (s === 0 && b % 4 === 0) hit(B, t, { f: 3000, g: 0.06, a: 0.05, dec: 0.9, rev: 0.3, pan: 0.2 });
      } },
    ],
    rave: [
      { name: 'Acid', step(B, n, t, st) {
        const s = n % 16, b = n >> 4, sx = B.sx;
        if (s % 4 === 0) kick(B, t, { g: 0.95, f0: 180, f1: 50, dec: 0.4, click: 0.12 });
        if (s === 4 || s === 12) clap(B, t, { g: 0.34 });
        if (s % 4 === 2) hat(B, t, 0.13, true, 0.2); else if (s % 4) hat(B, t, 0.04, false, -0.2);
        if (b % 8 === 7 && s >= 8) snare(B, t, { g: 0.08 + (s - 8) * 0.03 });
        const notes = [0, 0, 12, 0, 3, null, 15, 12, 0, 10, 0, 7, 0, 12, null, 3], acc = [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0], sl = [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0];
        if (notes[s] === null) { st.prev = undefined; return; }
        const m = 45 + notes[s], lfo = 0.5 - 0.5 * Math.cos(2 * Math.PI * n / 256);
        synth(B, t, sx * (sl[s] ? 1.05 : 0.6), m, { wave: b % 32 >= 16 ? 'square' : 'sawtooth', cut: 250 + 1600 * lfo, env: acc[s] ? 2500 : 1100, fdec: acc[s] ? 0.12 : 0.2, q: 12, drive: 2, g: acc[s] ? 0.17 : 0.12, s: 0.8, from: st.slide ? st.prev : undefined, dly: 0.15 });
        st.prev = m; st.slide = sl[s];
      } },
      { name: 'Trance', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, ch = [Am, F, C, G][(b >> 1) % 4], ph = b % 8;
        if (s % 4 === 0) kick(B, t, { g: 0.95, f0: 170, dec: 0.4 });
        if (s === 4 || s === 12) clap(B, t, { g: 0.3 });
        if (s % 4 === 2) hat(B, t, 0.12, true, 0.2); else if (s % 4) hat(B, t, 0.035, false, -0.2);
        if (s % 4 === 2) synth(B, t, sx * 1.8, ch[0] - 24 + (ch[0] < 55 ? 12 : 0), { cut: 500, env: 1200, fdec: 0.1, g: 0.3, s: 0.5 });
        if (ph < 4 && s % 2 === 0) synth(B, t, sx * 1.2, [ch[0], ch[1], ch[2], ch[1]][(s / 2) % 4] + 12, { wave: 'triangle', g: 0.05, d: 0.15, s: 0.2, dly: 0.35, rev: 0.25, pan: s % 4 ? 0.4 : -0.4 });
        const gate = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1];
        if (ph >= 4 && gate[s]) chord(B, t, sx * 0.7, ch.map(m => m + 12), { voices: 3, spread: 20, cut: 1500 + 700 * (ph - 4) + 40 * s, g: 0.02, a: 0.003, d: 0.1, s: 0.6, r: 0.05, dly: 0.2, rev: 0.3, pan: 0.3 });
        if (ph === 6 && s === 0) sweep(B, t, sx * 32, { f0: 300, f1: 9000, q: 4, g: 0.07, rev: 0.4 });
        if (ph === 0 && s === 0 && b) hit(B, t, { f: 5000, g: 0.11, dec: 1.6, rev: 0.4 });
      } },
      { name: 'Warehouse', step(B, n, t) {
        const s = n % 16, b = n >> 4, sx = B.sx, ch = [[53, 56, 60], [49, 53, 56], [51, 55, 58], [48, 51, 55]][b % 4];
        if (s % 4 === 0) kick(B, t, { g: 1, dec: 0.45, click: 0.1 });
        if (s === 4 || s === 12) { snare(B, t, { g: 0.4 }); clap(B, t, { g: 0.22 }); }
        if (s === 7 || s === 10) snare(B, t, { g: 0.1 });
        if (s === 15) snare(B, t, { g: 0.14 });
        if (s % 4 === 2) hat(B, t, 0.1, true, 0.25);
        if (s % 4 === 2) synth(B, t, sx * 1.8, ch[0] - 12, { voices: 2, spread: 18, cut: 280, env: 300, g: 0.24, s: 0.6 });
        if (s === 0 || s === 6 || (b % 2 && s === 11)) chord(B, t, sx * 2, ch, { voices: 4, spread: 35, bend: 2, cut: 2800, env: 1500, fdec: 0.2, g: 0.026, s: 0.5, rev: 0.3, dly: 0.15, pan: 0.35 });
        if (b % 8 === 7 && s === 0) sweep(B, t, sx * 16, { f0: 500, f1: 7000, q: 3, g: 0.06, rev: 0.3 });
      } },
    ],
  };

  // Just the click: louder on 1, softer off beats in half time.
  const CLICK = { name: 'Just the click', step(B, n, t, st) {
    if (n % 4) return;
    const c = B.c, k = (n >> 2) % 4, o = c.createOscillator(), g = c.createGain();
    o.frequency.setValueAtTime(k === 0 ? 150 : 110, t); o.frequency.exponentialRampToValueAtTime(45, t + 0.12);
    g.gain.setValueAtTime(k === 0 ? 0.9 : st.half && k % 2 ? 0.2 : 0.55, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.16);
    o.connect(g).connect(B.out); o.start(t); o.stop(t + 0.18);
  } };
  const list = style => (STYLES[style] || []).concat(CLICK);

  // Play a track until stop(): sixteenths are scheduled a little ahead so the tempo stays steady. onBeat(i, t) is
  // called for each beat (i = 0..3 in the bar) with the time it sounds.
  function play(c, o) {
    const T = list(o.style)[o.track] || CLICK, B = bus(c, o.bpm, c.destination), st = { half: !!o.half };
    let n = 0, next = c.currentTime + 0.08;
    const tick = () => {
      while (next < c.currentTime + 0.15) {
        try { T.step(B, n, next, st); } catch (e) { /* a missing node type in an old browser: keep the beat going */ }
        if (n % 4 === 0 && o.onBeat) o.onBeat((n >> 2) % 4, next);
        n++; next += B.sx;
      }
    };
    const timer = setInterval(tick, 25); tick();
    return { stop() {
      clearInterval(timer);
      const t = c.currentTime; B.master.gain.cancelScheduledValues(t); B.master.gain.setTargetAtTime(0, t, 0.04);
      setTimeout(() => { B.master.disconnect(); B.lfos.forEach(l => { try { l.stop(); } catch (e) {} }); }, 500);
    } };
  }
  // Schedule `bars` bars at once, for an OfflineAudioContext (previews and checks).
  function render(c, o) {
    const T = list(o.style)[o.track] || CLICK, B = bus(c, o.bpm, c.destination), st = { half: !!o.half };
    for (let n = 0; n < o.bars * 16; n++) T.step(B, n, 0.05 + n * B.sx, st);
  }
  root.BeatTracks = { styles: Object.keys(STYLES), names: style => list(style).map(x => x.name), play, render };
})(window);

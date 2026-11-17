---
id: computing-software.web-development.frontend-development.web-audio-api
name: web-audio-api
category: computing-software
field: web-development
product: frontend-development
tags: [web-audio-api, audiocontext, audio-worklet, autoplay-policy, gainnode, analysernode]
level: practitioner
status: docs-checked
description: "Web Audio API essentials: unlocking AudioContext after a gesture, node graphs, sample playback and scheduling, click-free gain ramps, analysers and AudioWorklet."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Using_Web_Audio_API
  - https://developer.mozilla.org/en-US/docs/Web/API/AudioWorklet
  - https://developer.chrome.com/blog/autoplay
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Audio API

## 1. Unlock on a gesture
```js
const ctx = new AudioContext();   // latencyHint defaults to "interactive"
button.addEventListener("click", async () => { if (ctx.state === "suspended") await ctx.resume(); });
```
MDN: a context created outside a user gesture starts `suspended` (states are `suspended`, `running`, `closed`) and must be resumed after a user interaction; one created inside a click handler should be `running`. Prefer reusing one context per app.

## 2. Play samples
```js
const buf = await ctx.decodeAudioData(await (await fetch("/sfx/click.mp3")).arrayBuffer());
function play(when = 0) {
  const src = new AudioBufferSourceNode(ctx, { buffer: buf });   // one-shot: create a new node per play
  const gain = new GainNode(ctx, { gain: 0.8 });
  src.connect(gain).connect(ctx.destination);
  src.start(ctx.currentTime + when);
}
```
Schedule against `ctx.currentTime` (seconds), not `setTimeout`. For rhythmic sequencing, use a lookahead scheduler: a timer that repeatedly schedules the notes due within a short window ahead.

## 3. No clicks
Sudden gain jumps click. Ramp instead:
```js
const g = gain.gain, t = ctx.currentTime;
g.cancelScheduledValues(t); g.setValueAtTime(g.value, t);
g.linearRampToValueAtTime(0, t + 0.05);         // or setTargetAtTime(0, t, 0.015)
src.stop(t + 0.06);
```

## 4. Visualise
```js
const an = new AnalyserNode(ctx, { fftSize: 2048 });
mediaSource.connect(an);
const data = new Uint8Array(an.frequencyBinCount);
(function draw() { an.getByteFrequencyData(data); render(data); requestAnimationFrame(draw); })();
```
Sources: `MediaElementAudioSourceNode` (an `<audio>` or `<video>` element), `MediaStreamAudioSourceNode` (microphone). `fftSize` must be a power of 2 from 32 to 32768 and defaults to 2048.

## 5. Custom DSP
`AudioWorklet` (secure contexts only) runs `process(inputs, outputs, parameters)` on a separate Web Audio thread in 128-frame blocks:
```js
await ctx.audioWorklet.addModule("/worklets/bitcrush.js");
const node = new AudioWorkletNode(ctx, "bitcrush");
```
Avoid allocating per block in `process`; `ScriptProcessorNode` is deprecated.

## Gotchas
- `decodeAudioData` returns a Promise and decodes only formats the browser supports; test the formats you ship on your target browsers.
- Close contexts you no longer need (`ctx.close()`) in SPAs.

## Verify
- [ ] First sound plays after the first tap on mobile browsers; no clicks when stopping sounds.

## Checked

Checked 2026-10-26 against MDN Web Audio API best practices (autoplay), AudioContext() constructor, AudioWorklet, AudioWorkletProcessor.process(), ScriptProcessorNode, AnalyserNode.fftSize and BaseAudioContext.decodeAudioData() (mdn/content main): suspended-until-gesture behaviour, `latencyHint` default `interactive`, 128-frame blocks, ScriptProcessorNode deprecation, fftSize range and default, and Promise-based decodeAudioData. Removed the unconfirmed claims about browser context limits, cross-origin CORS for media elements, iOS silent switch and low-power latency, and codec advice. The 25 ms / 100 ms scheduler figures were removed.

Method: documentation only; no commands were run.

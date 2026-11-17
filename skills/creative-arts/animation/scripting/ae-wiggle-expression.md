---
id: creative-arts.animation.scripting.ae-wiggle-expression
name: ae-wiggle-expression
category: creative-arts
field: animation
product: scripting
tags: [wiggle, ae-expressions, expressions, after-effects, noise, seedrandom, posterizetime, camera-shake, per-axis-wiggle]
level: practitioner
status: docs-checked
description: "Use wiggle() and noise() expressions well in After Effects: frequency and amplitude, per-axis wiggle, stepped wiggle with posterizeTime, seedRandom, and looping wiggle."
sources:
  - https://docsforadobe.dev/
  - https://raw.githubusercontent.com/docsforadobe/after-effects-expression-reference/master/docs/objects/property.md
  - https://raw.githubusercontent.com/docsforadobe/after-effects-expression-reference/master/docs/general/random-numbers.md
  - https://raw.githubusercontent.com/docsforadobe/after-effects-expression-reference/master/docs/general/global.md
  - https://raw.githubusercontent.com/docsforadobe/after-effects-expression-reference/master/docs/general/interpolation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wiggle and noise

**Goal:** organic randomness (handheld shake, flicker, jitter, floating) that is controllable and stylised where needed.

## Basics

`wiggle(freq, amp[, octaves=1][, amp_mult=0.5][, t=time])` randomly shakes the value of the property.
- `freq`: wiggles per second. `amp`: amplitude in units of the property it is applied to.
- `octaves`: how many octaves of noise are added together (higher adds finer detail). `amp_mult`: factor `amp` is multiplied by for each octave, so values near 1 keep the fine layers strong and values near 0 fade them.
- `t`: the base time; use it to sample the wiggle at a different time than now.
- Documented example: `position.wiggle(5, 20, 3, 0.5)` gives about 5 wiggles per second averaging about 20 pixels, plus two finer layers at 10 and 20 per second sized 10 and 5 pixels.

## Per-axis and uniform wiggle

```javascript
// Only the y axis of a 2D property
freq = 3; amp = 50;
w = wiggle(freq, amp);
[value[0], w[1]]
```
```javascript
// Same amount on both dimensions of Scale
v = wiggle(5, 10);
[v[0], v[0]]
```
A plain `wiggle()` on Scale returns separate values per dimension, so use the second form to keep the proportions.

## Stepped (animation on twos or threes)

```javascript
posterizeTime(8);
wiggle(8, 6)
```
`posterizeTime(updatesPerSecond)` sets the frame rate for the property lower than the composition's. Good for boiling hand-drawn looks.

## Seed

By default the seed is computed from a unique layer identifier, the property within the layer and the current time, plus an offset of 0. `seedRandom(offset[, timeless=false])` with a different offset gives a different random sequence, and the offset also sets the initial value of `wiggle()`. `timeless=true` stops the current time feeding the seed. Call it before `wiggle()`.

## Looping wiggle (seamless loop of length L seconds)

```javascript
L = 4; f = 1; a = 20;
t = time % L;
w1 = wiggle(f, a, 1, .5, t);
w2 = wiggle(f, a, 1, .5, t - L);
linear(t, 0, L, w1, w2)
```
`linear(t, tMin, tMax, value1, value2)` returns value1 at or below tMin, value2 at or above tMax and a straight-line blend between, and accepts arrays. At t = 0 the result is the wiggle at time 0 and at t = L it is the wiggle at time 0 again, so the ends match.

## noise()

`noise(valOrArray)` returns a number from -1 to 1. It is based on Perlin noise, so nearby inputs give nearby outputs. Scale it yourself, for example `value + noise(time*2) * 30`.

## Verify

Toggle the expression off with the equals-sign switch to compare; a looping version has the same value at time 0 and time L.

## Checked

2026-11-01. Confirmed against the After Effects expression reference (docsforadobe, sources above): wiggle signature, parameter meanings and defaults, the documented examples, seedRandom signature and default seeding, noise range and Perlin basis, posterizeTime wording, linear signature and array support. Removed as not stated there: that keyframes still work under wiggle, that duplicated layers differ because of the seed (only the seed inputs are kept), that the same seedRandom number gives identical motion on two layers, that posterizeTime affects the whole expression, noise being smoother than wiggle, and the gotchas about motion blur, frequency limits and rotation in rigs.
Method: documentation only; no commands were run.

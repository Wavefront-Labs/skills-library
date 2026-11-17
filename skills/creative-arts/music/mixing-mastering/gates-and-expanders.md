---
id: creative-arts.music.mixing-mastering.gates-and-expanders
name: gates-and-expanders
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, compression, dynamics-processing, noise-gate, expander, downward-expansion, gate-threshold, hysteresis, hold, range, sidechain-filter, tom-gating, bleed-reduction, key-input]
level: practitioner
status: draft
description: "Use gates and expanders to reduce bleed and noise: threshold, range, attack, hold, release and hysteresis, key filters, tom and snare gating, and when manual editing is better."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. on gating and expansion", "https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/ (Gate)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gates and expanders

**Goal:** reduce unwanted bleed and noise between notes without chopping the sound.

## 1. Gate vs expander
- **Gate**: below threshold, signal is attenuated by a large fixed amount (range, e.g. -80 dB = effectively off).
- **Expander**: below threshold, signal is reduced by a ratio (e.g. 1:2) - gentler, more natural. Set range to limit reduction (e.g. -10 to -20 dB) for subtle bleed control.

## 2. Controls
| Control | Setting tips |
|---|---|
| Threshold | just above the bleed level, below the quietest wanted hit |
| **Range** | how far it attenuates; -10 to -20 dB often sounds more natural than full mute |
| Attack | fast (0.01-1 ms) for drums so the transient isn't clipped |
| **Hold** | keeps it open after the signal falls (50-200 ms for toms) |
| Release | follows the natural decay (100-500 ms toms) |
| **Hysteresis** | separate open/close thresholds to stop chattering |
| Key filter (sidechain EQ) | band-pass on the trigger so only the wanted drum opens it (e.g. tom fundamental, reject cymbals) |
| Lookahead | lets fast attacks open before the transient |

## 3. Uses
- Toms (classic): gate or expand with key filter on the tom's frequency; hold to let the tom ring.
- Snare bottom/top bleed control (gentle range).
- Noisy guitar amps between phrases (expander).
- Creative: gated reverb on snare (80s), rhythmic gating with sidechain keying (trance gate).

## 4. When not to gate
- Variable, expressive parts (ghost notes) where any threshold misses notes: use **manual editing** (strip silence + fades) or volume automation instead.

## Gotchas
- Chattering on decays: add hysteresis or hold.
- Clicky attack: lengthen attack slightly or use lookahead.
- Gating overheads or room mics: destroys the kit's ambience.

## Verify
- Solo then in context: no missed hits (watch the gate's open indicator during soft notes), no audible pumping of bleed.

---
id: creative-arts.music.mixing-mastering.mix-bus-glue-compression
name: mix-bus-glue-compression
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, compression, bus-processing, mix-bus-compression, glue-compression, ssl-bus-compressor, 2-bus, stereo-bus, sidechain-high-pass, mixing-into-a-compressor, auto-release]
level: practitioner
status: draft
description: "Use mix-bus compression for glue: SSL-style settings, mixing into it, sidechain high-pass, how much gain reduction, and level-matched A/B checks."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Buss Compression", "https://www.solidstatelogic.com/ (SSL bus compressor manual)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mix-bus glue compression

**Goal:** a gentle compressor on the stereo mix that makes the parts move together, without
squashing.

## 1. When to insert it
- Many engineers put it on **early** ("mixing into the compressor") so balance decisions account for it. Adding it at the end changes the balance you've built.
- Either way, keep it on the mix bus before any limiter.

## 2. Starting settings (SSL G-style bus compressor)
| Control | Setting |
|---|---|
| Ratio | **2:1** (4:1 for aggressive styles) |
| Attack | **10 or 30 ms** (slow enough to let transients through) |
| Release | **Auto** or 0.1-0.3 s, timed to the groove |
| Threshold | for **1-3 dB** gain reduction on loud sections |
| Makeup | match bypassed loudness |
| Sidechain HPF | 60-150 Hz so kick/bass don't pump the whole mix |

- Other characters: VCA (SSL, API 2500) for punch/glue; opto (LA-2A style) for smooth; vari-mu (Fairchild, Manley) for thick, slow glue.

## 3. Listening for it
- Watch the needle move with the beat, mostly on kick/snare hits, returning between them. Release too slow = constant reduction (dull); too fast = distortion/pumping.
- Parallel use: mix-bus compression with a dry/wet control at 50-70% retains transients.

## 4. A/B honestly
- Level-match the bypassed signal (makeup gain to the same LUFS) before judging; louder always seems better.
- Check that drums still punch and the vocal sits; if the snare gets smaller, slow the attack or reduce reduction.

## Gotchas
- Leaving heavy bus compression on a mix sent to mastering: the engineer can't undo it. Send with your gentle bus compression if it's part of the sound, plus an unprocessed version if asked.
- Low end pumping the mix: raise the sidechain HPF.
- Stacking a bus compressor and a limiter both working hard: crushed transients.

## Verify
- Gain reduction 1-3 dB on the loudest section, near 0 in quiet sections.
- Level-matched A/B: the compressed version sounds more cohesive with no loss of punch.

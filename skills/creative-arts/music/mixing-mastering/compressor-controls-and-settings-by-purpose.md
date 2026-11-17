---
id: creative-arts.music.mixing-mastering.compressor-controls-and-settings-by-purpose
name: compressor-controls-and-settings-by-purpose
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, compression, dynamics-processing, compressor-settings, attack-release, threshold, ratio, knee, makeup-gain, gain-reduction, 1176, la-2a, vca-compressor, opto-compressor, fet-compressor]
level: practitioner
status: draft
description: "Understand every compressor control and set it by purpose (levelling, peak control, punch, glue, sustain), plus FET, opto, VCA and vari-mu characters."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Compressing for a Reason", "https://www.uaudio.com/blog/ (1176 and LA-2A usage guides)", "https://www.soundonsound.com/techniques/compression-made-easy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compressor controls and settings by purpose

**Goal:** set a compressor deliberately rather than by preset.

## 1. Controls
| Control | What it does |
|---|---|
| Threshold | level above which compression starts |
| Ratio | how much over-threshold level is reduced (4:1 = 4 dB over becomes 1 dB) |
| **Attack** | how fast it clamps down once over threshold; slow lets transients through (punch), fast catches them (control) |
| **Release** | how fast it recovers; fast = more density/possible distortion, slow = smoother but can hold down the next note |
| Knee | soft = gradual onset, hard = abrupt |
| Makeup gain | restores level; always level-match to judge |
| Detection | peak vs RMS; sidechain HPF to ignore lows |
| Mix (dry/wet) | parallel compression in one device |

## 2. Settings by purpose
| Purpose | Ratio | Attack | Release | GR |
|---|---|---|---|---|
| Levelling a vocal | 2-4:1 | 5-15 ms | auto/50-150 ms | 3-6 dB |
| Peak catching | 8-20:1 | <1 ms | fast | 2-4 dB on peaks |
| Drum punch | 4:1 | 10-30 ms | fast, timed to the groove | 3-6 dB |
| Sustain (guitar, bass) | 4-8:1 | fast | slow | 6-10 dB |
| Glue (bus) | 2:1 | 10-30 ms | auto | 1-3 dB |

## 3. Setting release by ear and tempo
- Watch the GR meter return to near zero just before the next hit; that's "breathing with the track". Quarter-note release at 120 bpm = 500 ms; try halves/quarters of that for drums.

## 4. Compressor characters
- **FET (1176)**: very fast, aggressive, colourful (vocals, drums, bass).
- **Opto (LA-2A)**: smooth, program-dependent slow attack/release (vocals, bass).
- **VCA (SSL, dbx, API)**: clean, precise, punchy (drums, bus).
- **Vari-mu (Fairchild, Manley)**: slow, thick, gentle (bus, mastering).

## Gotchas
- Judging louder-as-better: always match levels with makeup gain.
- Fast attack on drums kills the transient; slow attack on vocals lets peaks poke out.
- Too much GR flattens performance; serial gentle stages sound more natural.

## Verify
- GR meter moves as intended; level-matched bypass sounds more controlled but not lifeless.

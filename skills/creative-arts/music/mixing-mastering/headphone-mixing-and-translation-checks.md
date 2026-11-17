---
id: creative-arts.music.mixing-mastering.headphone-mixing-and-translation-checks
name: headphone-mixing-and-translation-checks
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, monitoring, headphone-mixing, translation-check, open-back-headphones, crossfeed, sonarworks, auratone, car-test, mono-check, small-speaker-check, reference-track, mix-translation]
level: practitioner
status: draft
description: "Mix on headphones without nasty surprises, and check any mix for translation: choosing headphones, crossfeed and correction, small-speaker, mono, car and earbud tests with fixes."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. 2 Supplementary Monitoring", "https://www.sonarworks.com/soundid-reference", "https://www.soundonsound.com/techniques/mixing-headphones"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Headphone mixing and translation checks

**Goal:** a mix that sounds right everywhere, even if made partly or mostly on headphones.

## 1. Headphones for mixing
- **Open-back** reference headphones (e.g. Sennheiser HD 600/650, Beyerdynamic DT 880/1990, AKG K702) for mixing; closed-backs for tracking.
- Apply **correction** (Sonarworks SoundID or published EQ curves) to flatten the headphone's response.
- **Crossfeed** or speaker-simulation plugins (Waves Nx, dSONIQ Realphones, Slate VSX) reduce the exaggerated stereo width of headphones.

## 2. Headphone pitfalls and how to counter them
| Problem | Why | Counter |
|---|---|---|
| Panning too extreme / reverb too low | no acoustic crosstalk | crossfeed; check on speakers |
| Low end misjudged | headphones lack physical bass feel | spectrum analyser and reference tracks; check sub with a sub/meter |
| Vocals too quiet or too loud | inside-the-head imaging | compare with references at matched loudness |
| Fatigue | high volume | mix at ~75-80 dB SPL equivalent, break every hour |

## 3. Translation checks (do all before calling a mix done)
1. **Mono**: sum to mono (master utility) - vocals and bass should stay solid; if something disappears it has phase issues.
2. **Small speaker** (Auratone-style, laptop, phone): balance of vocal vs music, bass audibility (harmonics).
3. **Car**: low-end and vocal level in a noisy environment.
4. **Earbuds**: the most common consumer playback.
5. **Quiet level**: very low volume shows the true balance of key elements.
6. **Reference tracks** at matched LUFS on the same system each time.
- Take notes during each check, then fix in the main monitoring environment.

## Gotchas
- Fixing to every system at once leads to chasing; prioritise issues that show on 2+ systems.
- Bluetooth playback adds its own processing/latency; prefer wired for checks.

## Verify
- Notes list from checks is empty or only matters of taste.
- The mix level-matched against references sounds comparable on each system.

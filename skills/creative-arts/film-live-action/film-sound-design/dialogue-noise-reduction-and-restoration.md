---
id: creative-arts.film-live-action.film-sound-design.dialogue-noise-reduction-and-restoration
name: dialogue-noise-reduction-and-restoration
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, post-production-sound, dialogue-editor, dialogue-noise-reduction, noise-reduction, restoration, izotope-rx, rx-11, spectral-repair, spectral-denoise, dialogue-isolate, voice-denoise, de-noise, de-click, de-crackle, de-hum, de-plosive, de-rustle, de-wind, de-reverb, mouth-de-click, de-ess, breath-control, ambience-match, eq-match, spectral-editing, audiosuite, pro-tools-restoration, cedar, waves-clarity, acon-digital, accentize, dxrevive, ai-dialogue-cleanup, over-processing, artefacts, musical-noise, room-tone-fill, dialogue-cleanup-order, batch-processing, rx-connect, spectral-repair-use, de-noise-modules, dialogue-isolate-use, de-click-use, mouth-de-click-use, de-reverb-use, de-rustle-use, de-wind-use, restoration-order, processing-order]
level: practitioner
status: draft
description: "Clean production dialogue without killing it: restoration order (hum, clicks, broadband, rustle, reverb), iZotope RX settings, spectral repair, matching ambience and EQ, spotting over-processing."
sources:
  - "https://www.izotope.com/en/products/rx.html (iZotope RX documentation and module guides)"
  - "https://www.mpse.org/ (Motion Picture Sound Editors - dialogue editing craft)"
  - "John Purcell, Dialogue Editing for Motion Pictures"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dialogue noise reduction and restoration

**Goal:** dialogue tracks that sound like the actor in the room, with the noise gone
and the performance untouched - and knowing when the right tool is ADR, not another
plug-in pass.

## 1. Triage first
Solo the ISO at mix level and classify each problem: **constant** (hum, HVAC, hiss,
traffic bed), **transient** (clicks, pops, a dog, a door), **modulated** (wind, clothing
rustle, mic bumps), **acoustic** (reverb, off-axis thinness), **performance** (mouth
clicks, sibilance, breaths), or **unusable** (distortion, RF hits across words,
overlapping lines). Check alternate takes and the other mics before treating; the lav
often saves the boom's plane, and vice versa. Decide ADR candidates now and send the
list to the director - restoration of the unrestorable costs days and still sounds wrong.

## 2. Order of operations
Fix in this order, each as lightly as possible, listening to the *difference* (RX's
Output Noise Only) after each step:
1. **De-hum / De-buzz** (RX *De-hum*: detect fundamental 50/60 Hz + harmonics; dynamic
   mode for drifting generators) and **high-pass** rumble (70-100 Hz).
2. **De-click / De-crackle** for clicks, crackle, digital errors (RX *De-click*,
   *De-crackle*; *Mouth De-click* for lip smacks - sensitivity low, listen for lost consonants).
3. **Transient events** (a chair, a dog bark) with **Spectral Repair** (attenuate/replace
   by surrounding spectrum) - select only the event in the spectrogram, not the words.
4. **Broadband noise**: *Spectral De-noise* with a **learned noise profile** from a
   clean gap (or adaptive mode for changing noise); reduction 6-12 dB, *Quality* high,
   a little *Artifact control*; **Voice De-noise** (adaptive, fast) for mild cases.
   Over-reduction yields "musical noise" (underwater warble) - back off until it just
   appears, then another 3 dB.
5. **Modulated noise**: *De-rustle* (lav cloth), *De-wind*, *De-plosive*; for severe
   cases **Dialogue Isolate** (AI separation; set the *Separation* and *Noise/Reverb
   reduction* sliders moderately, mix in some of the original).
6. **De-reverb** (RX *Dialogue De-reverb*/*De-reverb*, Accentize DeRoom, Waves Clarity)
   to match a close shot to a wide; it thins voices - use with care, often only on the
   wide's lines.
7. **Performance**: *De-ess* (RX or a dynamic EQ), breath control (*Breath Control* or
   manual clip gain -6 to -10 dB on breaths, not removed), *De-plosive*.
8. **Matching**: *EQ Match* (learn the good mic, apply to the off-axis one) and
   **Ambience Match** / room-tone fill under cuts so the noise floor is continuous.
Do steps 1-5 as AudioSuite/offline renders on clip copies (keep originals on a muted
track); leave reverb/EQ for real-time plug-ins where the mixer can adjust.

## 3. Working method
- Process **per mic/per setup**, not per scene - each mic has its own noise profile.
- Reference the picture; a little noise that sits with the room is better than a
  sterile line that pops out.
- A/B with bypass at matched loudness; listen on headphones *and* speakers.
- **Batch** the constant-noise passes (RX Batch Processor / Pro Tools AudioSuite on
  clip selections) but audition every result; automation can't hear a vowel go.
- Leave **handles**: process beyond the clip boundaries so fades don't expose noise.
- Tools beyond RX: **CEDAR** (DNS One/Studio for broadband, Retouch for spectral),
  Waves Clarity Vx, Acon Digital Restoration Suite, Accentize dxRevive (regenerative
  AI for extreme cases - verify it hasn't changed the performance or the voice).

## 4. When restoration is the wrong answer
Distorted peaks (RX *De-clip* helps only mild cases), words under a louder transient,
RF dropouts in the middle of a syllable, heavy reverb on a long line - mark for
**ADR** or try an alternate take with a conform. A dialogue editor's reputation
rests on knowing the limit.

## 5. Quality control
Play the scene in context with backgrounds and the temp music: noise reduction that
sounded fine solo may pump against the BG; add room tone to glue. Check sibilance and
"lisping" artefacts (too much de-click/de-ess), hollow tone (too much de-noise/de-reverb)
and double voices (AI isolation on overlapped lines).

## Gotchas
- De-noise first, then de-click; the profile learns the clicks and the voice turns watery.
- One noise profile applied across different mics and setups.
- Dialogue Isolate at 100% on every line; breathy, pre-echo'd, plastic voices.
- Breaths deleted instead of reduced; the performance stops being human.
- Processing destructively on the only copy of the ISO.

## Verify
- [ ] Problems classified per clip; ADR list sent before deep restoration.
- [ ] Order followed (hum, clicks, transients, broadband, modulated, reverb, performance, matching) with the difference signal audited at each step.
- [ ] Processing per mic/setup with learned profiles; originals kept muted.
- [ ] Scene checked in context with BGs and room-tone fill; no musical noise or lisping.

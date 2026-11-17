---
id: creative-arts.animation.principles.lip-sync-offset
name: lip-sync-offset
category: creative-arts
field: animation
product: principles
tags: [animation, lip-sync, lip-sync-offset, leading-the-sound, jaw, lips, timing, dialogue, polish, cg]
level: practitioner
status: draft
description: "Lead the sound by a frame or two so lip sync reads in sync, separate jaw and lip timing, and avoid mushy or chattering mouths."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://books.google.com/books?vid=ISBN9781560100843
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lip sync offset

Goal: lip sync that looks in sync to the audience. Mouths animated exactly on the sound
frame appear late; animators lead the sound.

## Leading the sound
- Shift mouth shapes **1-2 frames earlier** than the sound (Williams suggests about 2 frames
  ahead on film; many studios use 1-2). Perception: we see the mouth form before we hear.
- Check on the first hard consonant of the shot (a P or B) - the closure should be visible a
  frame before the pop.

## Jaw and lips separately
- **Jaw** carries the open-close rhythm of syllables (on vowels); keep it simpler, fewer keys.
- **Lips** carry shape (wide/narrow, pucker, F/V) and closures; they can lead the jaw slightly.
- Corners: width changes (EE wide, OO narrow) independent of jaw open.
- In CG rigs, animate the jaw first across the whole line, then lip shapes on top.

## Avoiding mush and chatter
- Don't open-close on every syllable in fast speech; hold a half-open shape through runs of
  small consonants.
- Hit the vowels that matter fully; under-animate the rest.
- Keep closures (m, b, p) - even 1 frame.

## Method
1. Track read.
2. Animate jaw open/close to syllables.
3. Add lip shapes and closures.
4. Shift the whole mouth animation 1-2 frames earlier (offset the keys).
5. Watch with sound at real speed (not scrubbing) - adjust specific words.

## Failure modes
- Exact-on-sound mouths: feel late.
- Too much offset (3+ frames): mouth visibly ahead.
- Jaw keyed on every phoneme: chattering.

## Verify
- [ ] Mouth keys lead sound by 1-2 frames.
- [ ] Closures present for all m/b/p.
- [ ] Real-speed playback with sound reads as in sync to a fresh viewer.

Related: `creative-arts.animation.principles.track-reading`,
`creative-arts.animation.principles.mouth-shapes-and-chart`.

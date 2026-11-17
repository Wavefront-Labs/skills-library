---
id: creative-arts.animation.principles.avoiding-the-uncanny-valley
name: avoiding-the-uncanny-valley
category: creative-arts
field: animation
product: principles
tags: [animation, appeal-principle, uncanny-valley, realistic-humans, facial-animation, eyes, mocap, stylization, digital-humans]
level: advanced
status: draft
description: "Keep realistic or semi-realistic characters out of the uncanny valley: eye life, facial micro-motion, consistent realism levels, and choosing stylization."
sources:
  - https://en.wikipedia.org/wiki/Uncanny_valley
  - https://books.google.com/books?vid=ISBN9780786860708
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Avoiding the uncanny valley

Goal: realistic human-like characters that read as alive and appealing instead of creepy.
Masahiro Mori's uncanny valley (1970): affinity drops sharply when something is nearly but not
quite human, and motion deepens the drop.

## What triggers it
- **Dead eyes**: no micro-saccades, no moisture/specular life, pupils not converging on the
  target, lids not following the eyeball.
- **Mismatch** of realism levels: photoreal skin with simplified motion, or cartoon proportions
  with realistic pores.
- **Missing micro-motion**: perfect stillness in holds, no breathing.
- **Mouth problems**: lips not compressing on m/b/p, teeth or tongue static, jaw not on an arc.
- **Mocap mismatch**: realistic body motion on a face with keyframed stiffness.

## Fixes
1. **Eyes first**: animate saccades (small, quick eye darts every 0.5-2 s in holds), convergence
   on targets, lid-follow on eye rotation, and wet specular highlights that track lights.
2. **Consistent level**: decide how real; if motion cannot match photoreal skin, stylize the
   design (bigger eyes, simplified skin) - Pixar's humans and Spider-Verse avoid the valley this way.
3. **Micro-motion**: breathing, weight shifts, subtle facial tension changes.
4. **Contact and compression** in lips and cheeks on speech.
5. **Reference** facial performance capture or video for close-ups; caricature it slightly.

## Failure modes
- Pushing realism in the render while animation stays limited.
- Smoothing mocap so much that life is removed.
- Symmetric facial motion.

## Verify
- [ ] Close-up holds: eyes dart, lids follow, character breathes.
- [ ] Realism level consistent across design, render and motion.
- [ ] Test viewers do not describe the character as "creepy" or "dead".

Related: `creative-arts.animation.principles.eye-darts`,
`creative-arts.animation.character-design.character-design-craft`.

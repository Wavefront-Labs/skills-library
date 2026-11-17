---
id: creative-arts.animation.art-direction.look-development
name: look-development
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, look-dev, style-guide, show-bible, visual-target, quality-bar, palette, cel, review, reference-board, murder-drones]
level: sme
status: draft
description: "Define and enforce a series' visual target: the show bible, reference boards, palette, line and lighting language, and the review bar every asset and shot must pass."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Art Direction / Look Development — the bar everything is judged against

The art director's job is not to draw; it is to **decide what "good" means for this
show and refuse everything that isn't it.** Without a written, pinned target, a team
(human or agent) produces *consistent* work that is consistently mediocre — exactly
the failure mode of an automated pipeline that renders 84 shots at blockout tier.
This skill is the first thing built on a series and the last word on every asset.

## 1. The reference target (do this before any modeling)
You cannot hit a bar you never defined. Build a **reference board** first:
- Pull 15–30 frames from the actual comparison titles (e.g. Murder Drones, Arcane,
  Rick & Morty, the specific episodes/shots you admire). Not "inspiration" — the
  literal bar.
- Annotate *why* each works: line weight, how many tone bands, shadow colour (cool/warm
  shift, not just darker), rim usage, proportion/shape language, staging, lens choices,
  palette temperature, grain/bloom amount.
- Save them in the repo (`<REPO>/series/design/ref/`) next to the bible. An asset is
  reviewed **side-by-side against this board**, never in isolation. "Looks fine on its
  own" is how blockout ships.

If there is no reference board, STOP and make one. Everything downstream (design,
modeling, lighting, comp) calibrates to it.

## 2. The show bible (the written contract)
One living document (`series/design/LOOKBOOK.md`) that locks:
- **Shape language** — what round/square/triangle mean in THIS show, and the
  per-character proportion system in head-heights. (See character-design-craft.)
- **Line / outline** — outline present? weight (world-scale, so character scale is
  fixed), colour (pure black vs dark-tint), where it breaks. (See cel-shading.)
- **Tone model** — number of cel bands (2? 3?), band break positions, and the
  **shadow hue shift** (e.g. shadows pushed toward blue/violet, not grey). This single
  choice separates "toon" from "flat and cheap."
- **Palette** — a locked swatch set with hex per character + per environment, plus the
  temperature rule (warm key / cool shadow, or the reverse). Colour is designed, not
  picked per asset. (See color-script.)
- **Lighting language** — key direction, rim/kick usage, contrast ratio, how mood maps
  to lighting (safe scene vs threat scene). (See lighting.)
- **Camera language** — lens set per shot size, how much DOF, handheld vs locked,
  the show's default coverage grammar. (See camera-cinematography, layout-blocking.)
- **Comp signature** — bloom/glare amount, grain, chromatic aberration, vignette, grade.
  A specific, restrained recipe — not "everything on." (See compositing-grade.)
- **Negative space rules** — what the show NEVER does (e.g. "no blown-out backgrounds,"
  "no cutting to a face that doesn't read," "no dead-even motion"). Written failure
  modes are the most useful part of a bible.

## 3. Readability law (the thing blockout violates)
Every asset and shot must pass three reads, in order:
1. **Silhouette read** — solid-black, does it read as the character / the action?
2. **Thumbnail read** — at 10% size, does the composition and pose still communicate?
3. **Close-up read** — when the camera pushes in, is there something designed to look
   at (a face that exists, detail, expression)? Cutting to a featureless form is the
   single most damaging thing a stylized show can do — it tells the audience there is
   nothing there. If a character can't survive a close-up, either the design or the
   shot is wrong.

## 4. The review bar (how you enforce it)
Art direction is applied at **review gates**, not at the end:
- **Design gate** — a design passes only against the bible + ref board (appeal,
  shape language, model-ability, survives all three reads). Reject blobs.
- **Model gate** — on-model vs the turnaround; clean topology; silhouette read.
- **Look-dev gate** — cel ramp + outline + a test light match the tone model; no
  bloom washing emissive features.
- **Lighting/comp gate** — shot matches the lighting + comp signature; no blown
  backgrounds; contrast reads.
- **Animation gate** — performance reads (clear pose on the beat, eye direction,
  weight) — not lip-flap on a static body.
Each gate is **pass/fail against the written bar**, with the ref board open. "Close
enough" at an early gate compounds into a mediocre final. Kick it back.

## 5. Verifying the bar is real (not just prose)
A bible that can't fail anything is decoration. Prove it:
- Take ONE hero asset through every gate and record pass/fail + the fix at each. If
  nothing ever fails, the bar is too low — tighten it against the ref board.
- Pin a **before/after** of that hero asset in the lookbook: blockout vs on-bible.
  That pair IS the bar, visible to everyone (and every agent) downstream.

## Verify
- [ ] A reference board of real comparison frames exists in the repo and is annotated.
- [ ] LOOKBOOK.md locks shape/line/tone/palette/lighting/camera/comp + explicit "never" rules.
- [ ] One hero asset has a recorded trip through all review gates with a before/after pair.
- [ ] A reviewer, given only the bible + board, reaches the same pass/fail as the AD on a sample asset (the bar is objective enough to delegate).

See character-design-craft, cel-shading, color-script, lighting, compositing-grade,
camera-cinematography, acting-performance — this skill is the bar; those are how each
department hits it.

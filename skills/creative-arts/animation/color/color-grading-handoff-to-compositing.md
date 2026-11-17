---
id: creative-arts.animation.color.color-grading-handoff-to-compositing
name: color-grading-handoff-to-compositing
category: creative-arts
field: animation
product: color
tags: [color, handoff, compositing, vfx, asc-cdl, lut, slap-comp, version-lock, exr-metadata, element-insertion, double-grading, ocio, pipeline, animation]
level: advanced
status: draft
description: "Passing a locked grade or color decision to a compositing department without it being re-applied, lost or baked in at the wrong stage"
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Color grading handoff to compositing

**Goal:** when grading and compositing are done by different people/tools (a
colorist or color lead hands a locked look to a comp department, or VFX
elements must be inserted into already-graded footage), make sure the color
decision survives the handoff *exactly once* — never dropped, never doubled.
This is the interchange problem, distinct from the grading craft itself
(`creative-arts.animation.color.color-grading`, which is how the grade is
*made*) and from the pipeline plumbing that keeps color spaces consistent
(`creative-arts.animation.color.look-development-for-color-pipelines`). On a
single-artist cel pipeline where the same person grades and comps in one
Blender file, this problem barely exists — it shows up hard the moment a
look is approved by one party and executed or extended by another, or when
upstream elements (a VFX plate, an FX pass, a title card) must drop into a
shot that already has a grade applied.

## The central risk: double-grading and lost-grading

- **Double-grading**: a LUT or grade gets baked into a render, and a second
  party downstream (not knowing it's already there) applies the *same* or a
  *different* grade on top. Compounds colors, crushes/clips a region twice,
  and is often subtle enough to pass a quick look but fail scrutiny — chase
  it with scopes (`color-grading`'s waveform/vectorscope check), not by eye.
- **Lost-grading**: a comp artist opens the *ungraded* source plate instead
  of the graded reference by mistake (wrong file, wrong version, wrong color
  space tag) and does work that never gets the approved look applied at all.
- Both failures are invisible until late review, because a render that's
  "graded wrong" and one that's "ungraded" can both look superficially
  plausible on a small preview.

## Interchange mechanisms (pick the lightest one that's unambiguous)

- **ASC CDL** (Slope/Offset/Power + Saturation) — a small, standard,
  human-readable metadata format (`.cdl`/`.ccc`) for a first-order grade
  decision (essentially lift/gamma/gain + sat). Lightweight enough to travel
  as a sidecar file alongside an EXR sequence without baking anything in —
  the receiving tool applies it, and it stays editable/removable. Use CDL
  when the handoff needs to stay a *decision*, not a baked image, e.g.
  handing a "slap" look to comp that will likely need refinement.
- **Baked 3D LUT** (`.cube`, as covered in `color-grading`) — bakes the look
  irreversibly into the pixels or into a non-destructive preview-only layer
  depending on the tool. Right for a *locked, final* look that won't change,
  or for giving an editorial/offline cut a consistent preview without
  shipping the full node graph. Wrong for anything still likely to be
  revised — baking early forces re-renders instead of a node-group edit.
- **Full node-graph/group handoff** — hand over the actual grade node group
  (Blender) or grade tree (Nuke/Resolve), not just its baked result, when the
  receiving party needs to keep editing the grade itself (e.g. comp needs to
  nudge a highlight because an added VFX element changed the read). Heaviest
  but most honest option — no information loss.
- **Reference-only ("burned-in") preview**: a cheap, clearly-labeled
  (watermarked/slated) preview render used only so comp can *see* the
  intended look while working on the real, ungraded/un-baked source. Never
  let this file be mistaken for a deliverable — name it unambiguously
  (`_REF_DO_NOT_USE` or similar convention) and keep it out of any folder a
  later pass might treat as final.

## The slap comp / final comp distinction

A **slap comp** is a fast, rough grade + rough composite used for editorial
review, pacing, or client approval before the real work is locked — explicitly
disposable. Treat a slap comp's grade as provisional even if it's well-liked:
re-derive the final grade from the approved look's *intent*, not by reusing
the slap comp's baked pixels, unless you've confirmed it was made with a
reusable mechanism (CDL/node group) rather than a one-off eyeball pass.

## Keeping element insertion honest

When a VFX element (an explosion, a added prop, a lighting effect) must be
composited into a shot that already carries a locked grade:
- **Insert in the same color space the grade was built for** (usually
  scene-referred/linear, before the view transform — see
  `look-development-for-color-pipelines`) so the element reacts to the grade
  the same way the rest of the plate does, rather than looking pasted on.
  Compositing a display-referred element into a linear grade workflow (or
  vice versa) is a very common source of elements that "don't belong."
  Uncertain/unconfirmed here: the exact best point of insertion varies by
  tool and whether the grade is baked per-shot or applied globally — verify
  against your specific pipeline rather than assuming one universal rule.
- **Re-check scopes after insertion**, not just at the original grade —
  a bright new element can blow past the grade's intended white point in a
  way the original scopes check never saw.

## Version lock and labeling

- **Every handoff needs an explicit version id** (shot/take/grade-version)
  baked into the filename or embedded as EXR metadata — "the grade" is
  meaningless once more than one version has existed.
- **State what's baked and what isn't, in the filename or an accompanying
  note**: "ungraded linear EXR", "CDL sidecar attached, not applied",
  "baked final grade, do not re-grade." A comp artist should never have to
  guess which state a file is in.
- **Lock and announce, don't silently iterate.** If a grade changes after
  comp has started working against it, that's a new version with a new id,
  communicated explicitly — not a quiet overwrite of the file comp already
  pulled.

## Verify

1. Pick a handed-off shot and confirm, from its filename/metadata alone
   (no need to open it), whether it is ungraded, CDL-tagged, or baked-final —
   if you can't tell without opening the file, the labeling convention has
   failed.
2. Open a shot with an inserted VFX element on its scopes: the element's
   black/white points and dominant hue sit consistently with the rest of the
   graded frame, not pasted-on.
3. Diff two versions of the "same" handed-off grade (CDL values or baked
   pixels) and confirm the version id in the filename actually changed when
   the content did — no silent overwrite.
4. Trace one shot end to end from ungraded source to final deliverable and
   confirm the grade was applied exactly once — not zero times, not twice.
5. Ask whoever received the handoff to state, without checking with you,
   whether their file is final-baked or still-editable — if they're unsure,
   the handoff needs a clearer label, not a clearer verbal explanation.

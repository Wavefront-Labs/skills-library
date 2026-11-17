---
id: creative-arts.animation.pipeline.render-preflight
name: render-preflight
category: creative-arts
field: animation
product: pipeline
tags: [preflight, validation, qc, proof-strip, contact-sheet, iteration, lint, pipeline, render, checks, fast-feedback]
level: advanced
status: verified
description: "Kill render iteration cost: static-validate the whole episode in seconds and proof-strip one frame per shot in minutes BEFORE committing hours to the animation render."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Render preflight — never discover a problem after a two-hour render

The most expensive mistake in an automated render pipeline is finding a defect in the
assembled cut: one bad tag, one missing file or one mis-aimed camera costs a full
re-render cycle. A studio catches this with department gates and dailies; an automated
pipeline needs the same discipline as **two cheap machine passes that run before every
full render**. Together they collapse the iteration loop from hours to minutes.

## Pass 1 — static preflight (seconds)
A validator that reads the shotlist (the single source of truth) and checks everything
checkable WITHOUT rendering. Hard FAILs block the render; WARNs print and continue:
- **Assets**: every location and cast member resolves to an existing locked asset file;
  FX/TITLE shots have their comp clip built (else they slate black in the cut).
- **Audio**: every `line_id` has its VO wav AND its viseme json; the wav duration fits
  the shot's `dur_s` (an over-long read gets clipped mid-word in the cut).
- **Speaker sanity**: the line's speaker prefix matches a cast member — and flag when it
  isn't the primary, because naive pipelines sync the mouth of cast[0], not the speaker.
- **Tags**: every `emotion`/`look`/pose tag is a known state (an unknown tag silently
  falling back to neutral is a defect you'd never spot in 87 shots).
- **Staging**: cast count <= available marks for the set; ids unique; durations sane.
Exit non-zero on FAIL so episode builds can refuse to start. Keep the validator's known
sets/chars/states in lockstep with the renderer (same tables or imported).

## Pass 2 — proof strips (minutes)
Render **one mid-shot frame per shot** (a `--still` mode in the shot renderer: same
scene build, same staging/expressions/camera, one frame at ~2/3 through the shot) and
tile the frames into contact sheets in shotlist order. A whole 87-shot episode proofs in
~10 minutes, and one glance at the sheets catches what static checks cannot:
- mis-framed or clipped-into-geometry cameras (coverage variation makes this likely),
- broken faces / wrong expression / features displaced by a transform bug,
- blown exposure, missing dressing, characters facing away, lighting mood mismatch.
Review the sheets against the LOOKBOOK's reject list, fix, re-strip ONLY the affected
shots (each still is independent), and only then pay for the animation render.

## The discipline
1. Tag/data change -> **preflight** (seconds).
2. Renderer/asset/look change -> **proof-strip** the affected sequence (a minute or two).
3. Before any full episode render -> preflight + full strip, both clean.
4. A defect that slips through to an assembled cut = add the check that would have
   caught it. The validator only grows.

## Verify
- [ ] Preflight on a known-good episode: 0 FAIL, and it completes in seconds.
- [ ] Break one thing on purpose (rename a VO wav, misspell an emotion) - preflight FAILs it.
- [ ] Proof-strip a sequence: one frame per shot lands + tiles into a sheet; a deliberate
      camera error is visible on the sheet.
- [ ] Full render refused/withheld until both passes are clean.

**Verified (proof):** built as production `preflight.py` + `proof_strip.py` (with a
`--still` mode added to the shot renderer). On its FIRST run preflight caught two real
defects that had shipped in every prior cut: a line lip-synced onto the wrong character's
mouth (speaker != cast[0]) and an over-long directed VO read that would clip. Seconds,
not render-hours.

See shot-renderer (the --still hook), dailies-review (the human gate this automates the
mechanical half of), production-tracking, continuity-supervision, look-development
(the reject list the strips are judged against).

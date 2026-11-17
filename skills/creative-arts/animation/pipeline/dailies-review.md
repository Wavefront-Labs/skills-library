---
id: creative-arts.animation.pipeline.dailies-review
name: dailies-review
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, dailies, review, notes, approval, gates, iteration, versioning, feedback, production-tracking, json, qc]
level: advanced
status: draft
description: "Running dailies and review gates per department: actionable notes, approval states, versioned rounds, catch-it-early, a local JSON review log."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Dailies and review (the notes-and-iteration discipline)

**Goal:** catch every problem at the cheapest stage to fix it, and never let a shot
advance a department on a guess. Dailies are the feature-animation ritual of reviewing
work-in-progress on a gate, giving **actionable** notes, tracking them to closure, and
stamping an explicit **approval** before the shot moves on. At solo/automated scale
you are the whole review room — which makes the *discipline* (a log, states, rounds)
matter more, not less, because there's no second set of eyes to catch what you wave
through.

This sits on top of `production-tracking.md` (the shot status board) and enforces the
review gates named in `../art-direction/look-development.md`.

---

## 1. The gates (review happens at the seams)

Work flows through departments; review happens **at every hand-off**, because a defect
caught one gate early is 10× cheaper to fix than caught two gates late:

```
design → model → rig → anim → light → comp → (audio) → final
   └ review ─┘    └ ─┘   └ ─┘   └ ─┘    └ ─┘      └ ─┘
```

- **design** — model sheet / color on-model? (`../character-design/model-sheet-turnaround.md`)
- **model** — topology, silhouette, scale vs the sheet.
- **rig** — deformation, controls, no breakage at range (`../blender/rigging.md`).
- **anim** — staging, timing, acting, lip-sync, 180° line.
- **light** — cel ramp reads, consistency, no ramp-fight (`../blender/cel-shading.md`).
- **comp** — grade, plate integration, outline (`../blender/compositing-grade.md`).
- **audio** — dialogue edit + mix against picture.

A shot does not enter a department until the previous gate is **approved**. That rule
is the entire point: it stops you rigging a model that's off-sheet, or animating a rig
that breaks.

---

## 2. The catch-it-early principle (why the gate exists)

The cost of a fix rises steeply with how far downstream it's found. A proportion
problem caught at **design** is a redraw; caught at **model** it's a resculpt; caught
at **anim** it's a re-rig *and* re-animate; caught at **comp** it's the whole chain
again plus a re-render. So the reviewer's prime directive at each gate is: **would
this survive all the way to screen, and if not, is this the stage it's cheapest to
fix?** Reject up-front rather than "fix it in comp" — comp is where cheap fixes go to
become expensive.

---

## 3. What makes a note actionable

A note the artist (or the next automated pass) can't act on is noise. Every note is:

- **Located** — shot id + frame/timecode + which element. "EP03_014 @ f12, Dill's left
  hand" not "the hand looks off".
- **Specific and observable** — what is wrong, not a vibe. "elbow pops on frames 12–15"
  not "animation feels stiff".
- **Prescriptive or at least directional** — the fix or the intent. "hold the contact
  2 more frames so the step reads".
- **Prioritized** — tagged **blocking** (must fix to approve) vs **polish** (nice,
  non-gating). Mixing the two is how shows chase gloss while structure stays broken.
- **Singular** — one issue per note, so it can be checked off independently.

Avoid the two classic failures: the vague note ("make it pop") and the kitchen-sink
note (twelve issues in one paragraph, half get missed).

---

## 4. Approval states

Every shot at every gate carries one state. Keep it to a tiny, ordered set:

- **wip** — not yet submitted for review.
- **review** — submitted, awaiting notes.
- **retake** — notes issued, shot must iterate (the normal, healthy state).
- **approved** — gate passed, may advance to the next department.
- **final** — locked for delivery; any change now requires un-locking deliberately.

"approved" is a gate-scoped stamp: *approved-anim* ≠ *approved-comp*. A shot is only
`final` when it has passed the last gate. Backward moves (approved→retake) must carry a
reason, mirroring `production-tracking`'s rule, so regressions are visible.

---

## 5. Versioning review rounds

Each review turn is a numbered **round** against a numbered **version** of the work, so
"which comp did I note on?" is never a guess:

- Version the output: `EP03_014_anim_v003`. The renderer / asset registry
  (`asset-management.md`) already versions; reviews attach to that version.
- A round = `{version, date, notes[], verdict}`. Round 1 on v003 → retake → v004 →
  round 2 → approved. Keeping the chain means you can see a note was *actually
  addressed*, not silently dropped.
- **Never re-note from scratch.** Each round starts by checking the *previous round's
  blocking notes are closed*, then adds new ones. A note that reappears round after
  round is a process smell — escalate it, don't re-type it.

---

## 6. A local review log (JSON, pipeline-native)

Don't buy a review SaaS for a solo/small series. Keep a `EPnn_reviews.json` beside the
tracker, same data plane as everything else (`production-tracking` §tracker):

```json
{
  "episode": "EP03",
  "reviews": [
    { "shot": "EP03_014", "gate": "anim", "version": "v003", "round": 1,
      "date": "2026-10-13", "verdict": "retake",
      "notes": [
        { "id": "n1", "frame": 12, "elem": "dill_L_hand", "pri": "blocking",
          "note": "elbow pops f12-15, smooth the IK", "status": "open" },
        { "id": "n2", "frame": null, "elem": "staging", "pri": "polish",
          "note": "nudge Dill 10cm screen-left for headroom", "status": "open" }
      ] },
    { "shot": "EP03_014", "gate": "anim", "version": "v004", "round": 2,
      "date": "2026-10-14", "verdict": "approved",
      "notes": [ { "id": "n1", "status": "closed" } ] }
  ]
}
```

Why JSON: it joins the tracker and registry — a `verdict: approved` can **advance the
shot's status automatically**, and an open blocking note can **hold** it. A date-stamped
log is also the honest record of why a shot took five rounds (useful for
`producing-scheduling.md`'s estimates). You can render a read-only HTML dailies sheet
*from* the JSON for a human glance — generated, never authoritative.

`ponytail:` single JSON per episode, linear scan; fine to ~1k shots, move to SQLite
only if cross-episode note queries get slow.

---

## 7. Running the review itself

- **Review in context, at speed.** Play anim/comp at real-time 24fps (not stepping
  frames) — many problems only show in motion; many "problems" vanish at speed.
- **Review at delivery conditions.** Correct color transform (Standard view),
  final-ish resolution, audio synced. A note given on a wrong-gamma preview is a wasted
  note.
- **Compare to the reference.** Model sheet for design/model, the previous approved
  shot for continuity, the color script for light. Review against a *target*, not taste.
- **Separate "is it on-model/on-brief" from "do I like it".** The gate is correctness
  first; preference is a polish note.
- **Timebox.** A gate review is minutes per shot, not an afternoon — the log catches
  what the eye misses, so you don't need to exhaust a shot in one sitting.

---

## 8. Closing the loop with the pipeline

- Open **blocking** note → shot cannot reach `approved`/advance in
  `production-tracking` (the gate holds it).
- `verdict: approved` → tracker advances the shot to the next department state.
- `retake` → stays in the department, round increments, artist/pass iterates.
- A re-rendered version after an `asset-management` bump re-enters `review` (the old
  approval doesn't carry to new frames) — this is how `needs_rerender` shots get
  re-checked rather than silently shipping stale.

---

## 9. Self-review at solo scale (the hard part)

The feature model assumes a supervisor reviews an artist. Solo, you review your own
work — and you are the worst judge of it, because you know what you *meant*. Discipline
substitutes for a second pair of eyes:

- **Review cold.** Don't review a shot the moment you finish it; you're still seeing
  your intent, not the result. Leave it, come back, review against the reference as if
  someone else made it.
- **Review against the target, not your effort.** The gate is "is it on-model / does it
  read", not "did I work hard". Hours spent don't buy an approval.
- **Flip it.** Mirror the frame, squint it, drop it to thumbnail, play it at speed —
  tricks that break your eye's familiarity and surface what you've gone blind to.
- **Let the log be the second reviewer.** You will forget a note; the log won't. Trust
  the written note over the memory.
- **The LLM director can issue notes too.** At this pipeline's scale the director pass
  can generate structured notes against the shotlist intent — treat them as a review
  round in the same log, same actionability bar.

## 10. Anti-patterns (what kills a review process)

- **Reviewing at the wrong conditions** (bad gamma, low res, no audio) → wasted notes.
- **Vague or stacked notes** → half get missed; one issue per note, located.
- **Skipping the gate "to save time"** → the defect ships to the next department and
  costs 10× there. The gate *is* the time-saver.
- **Approving to feel progress** → an un-earned approval is a lie the delivery exposes.
- **Not logging** → "I'll remember" is how notes get dropped and rounds repeat.
- **Polishing before structure is approved** → gloss on a broken shot is wasted; block
  on structure first, polish last.

---

## Verify

1. **Gate enforcement.** Try to advance a shot with an open **blocking** note — the
   tracker refuses; closing/ waiving the note (with a reason) is the only way through.
2. **Actionability.** Pick any logged note — it has shot+frame+element, is one issue,
   is tagged blocking/polish, and a reader could fix it without asking a question.
3. **Round integrity.** Round 2 on a shot explicitly lists round 1's blocking notes as
   closed before adding new ones — no silent drops; a recurring note is flagged.
4. **Approval scoping.** A shot approved at `anim` is not treated as approved at
   `comp`; `final` only after the last gate.
5. **Auto-advance.** Setting a review `verdict: approved` moves the shot's status in
   `production-tracking` with no manual status edit.
6. **Re-review on re-render.** Bump a used asset; the affected approved shots drop back
   to `review` rather than staying `approved` on stale frames.

See `production-tracking.md` (status board this gates), `asset-management.md`
(versions reviews attach to), `../art-direction/look-development.md` (the look gate),
`producing-scheduling.md` (uses round counts for estimates).

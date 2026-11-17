---
id: creative-arts.animation.pipeline.production-tracking
name: production-tracking
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, production-tracking, shot-status, build-queue, progress, json, tracker, blockers, scheduling, shotlist, episode]
level: advanced
status: draft
description: "Track a series through the pipeline: shot status board->render->comp->mix->done, a build/asset queue, per-episode progress, a local JSON tracker, catching blockers."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Production tracking (a series through the pipeline)

**Goal:** always know, for all 10 episodes and ~870 shots, what state every shot
is in, what's blocking it, and what to build/render next — from a simple local
tracker, no cloud PM tool. This is the dispatcher sitting between the data-driven
renderer (`shot-renderer`, which emits the missing-asset queue) and the asset
registry (`asset-management`, which owns asset versions). It answers the three
questions a production lead lives on: *what's done, what's next, what's stuck.*

## Why a tracker at all (the problem it solves)

With one shot you remember its state. With 870 across 10 episodes, memory fails
and "I think EP07 is mostly comped" is how a show ships half-finished. A tracker
is the production's working memory: it makes state explicit, queryable and
auditable, so planning is reading a number instead of re-opening every `.blend`.
The discipline is small — a few fields per shot — but it's the difference between
a series you can steer and one you discover is broken on delivery day.

## The shot lifecycle (the status state machine)

Every shot moves through a fixed, ordered set of states. Fixed order = a sortable
pipeline, not a free-text mess:

```
board → layout → render → comp → mix → done
                   │
                   └─(asset missing)→ blocked
```

- **board** — shotlisted/boarded (`shotlist-boarding`), exists only as data.
- **layout** — staged/blocked in Blender (`layout-blocking`).
- **render** — renders out as passes (`render-aov-passes`); auto-done by the
  renderer when assets resolve.
- **comp** — assembled/graded (`multipass-compositing`, `color-grading`).
- **mix** — in the episode audio mix (`final-mix`).
- **done** — delivered-ready (`youtube-master`).
- **blocked** — orthogonal flag + reason (missing asset, failed render, note);
  a blocked shot still knows which state it's waiting *in*.

Only forward moves are normal; a backward move (comp→render) must carry a reason
(e.g. asset re-render from `asset-management`'s blast radius) so regressions are
visible, not silent.

## The tracker: one JSON per episode

Keep it dead simple and local — one `EPnn_tracker.json`, git-versioned beside the
shotlist. Reuse the shotlist as the spine; the tracker adds state:

```json
{
  "episode": "EP03",
  "updated": "2026-10-13",
  "shots": [
    { "id": "EP03_014", "size": "CLOSE", "status": "comp",
      "assets": ["char_ivy", "set_alley"], "line_id": "EP03_014_ivy_01",
      "blocked": null, "needs_rerender": false, "note": "" },
    { "id": "EP03_015", "size": "WIDE", "status": "blocked",
      "assets": ["set_catwalk"], "blocked": "missing:set_catwalk",
      "needs_rerender": false, "note": "waiting on catwalk model" }
  ]
}
```

Why JSON, not a spreadsheet: the renderer and asset registry already read/write
JSON, so the tracker is the same data plane — the renderer can **flip a shot to
`render`→`comp` and append missing assets to the build queue automatically**, no
human retyping. A sheet is a human-only island; JSON is pipeline-native. (You can
render a read-only sheet/HTML *from* the JSON for a human glance — generated, not
authoritative.)

`ponytail:` naive single-file-per-episode JSON, O(n) scans; fine to ~1k shots.
Move to SQLite only if cross-episode queries get slow.

## The build/asset queue (what to model next)

The renderer's core behavior (`shot-renderer`): if an asset is missing, **skip
the shot and log it** rather than fake it. Those logs are the build queue —
production-tracking just aggregates and prioritizes them:

1. Scan all trackers for `blocked: "missing:<asset>"`.
2. **Count shots blocked per missing asset** — the asset blocking the most shots
   is modeled first (highest leverage). `set_catwalk` blocking 22 shots beats a
   prop blocking 1.
3. Emit a ranked build list: `<asset> — N shots blocked across EPxx…`.
4. When `asset-management` publishes that asset (`current` set, `locked`), the
   next renderer pass auto-clears the `blocked` flag and advances the shots. The
   queue shrinks itself.

This closes the loop: tracker exposes the bottleneck → asset is built → renderer
unblocks → tracker advances. No one guesses what to model next; the shot demand
decides.

## Per-episode progress

A tiny aggregation gives the status read you need for the Plans Board:

- **Count by status** per episode: `board:12 layout:8 render:30 comp:20 mix:5
  done:12 blocked:3`.
- **% complete** = done / total (and a weighted version counting partial credit
  per state if you want a smoother burn-down).
- **Series roll-up:** the same counts summed across EP01–EP10 — the one-line
  answer to "where's the show."
- **Blocked list** front and center: every blocked shot + reason, because blocked
  shots are the only ones that *won't* move without intervention.

## Catching blockers early

A blocker is anything that will stall a shot that otherwise looks ready:

- **Missing asset** — caught automatically by the renderer's skip-and-log.
- **Missing VO / lip-sync** — a shot with a `line_id` but no rhubarb json
  (`vo-lipsync-pipeline`) can render idle but not final; flag `blocked:
  missing-vo`.
- **Needs-rerender** — set by `asset-management` when a used asset version bumps;
  the shot is "done" but stale. Surface these loudly or the cut ships old frames.
- **Stale status** — a shot sitting in one state too long (e.g. `render` for days)
  is a quiet blocker; a date-in-state field flags shots that haven't moved.
- **Dependency not ready** — the mix can't start until all of an episode's shots
  are at `comp`; the tracker's status counts make that gate obvious.

Run a single `status` command/script over all trackers that prints: series
roll-up, the ranked build queue, every blocked shot, and every `needs_rerender`
shot. That one report is the daily standup.

## The daily report (worked example)

One script, run once a day or before any planning, prints the whole picture from
the episode trackers plus the asset registry. A representative run:

```
Hollow Creek — production status  (2026-10-13)
─ Series roll-up (870 shots) ──────────────────────────────
  board 41  layout 63  render 120  comp 95  mix 48  done 471  blocked 32
  complete: 54%   (done 471 / 870)
─ Per episode ─────────────────────────────────────────────
  EP01 done           EP06 comp 40 / mix 2 / done 45
  EP02 done           EP07 render-heavy, 12 blocked
  …                   EP08 layout
─ Build queue (ranked by shots blocked) ───────────────────
  set_catwalk   22 shots  (EP07, EP09)      ← model next
  char_vera     6  shots  (EP07)
  prop_relay    3  shots  (EP09)
─ Needs re-render (stale after asset bump) ────────────────
  EP02_031, EP02_032   (char_dill v003→v004)
─ Stale (>7 days in state) ────────────────────────────────
  EP07_118  render  11d   ← investigate
```

The build queue line is the single most valuable output: it converts "the show
feels stuck" into "model `set_catwalk` and 22 shots unblock." The
needs-re-render and stale lists are the two ways a series silently ships wrong —
both surface here rather than being discovered on the cut.

## Feeding the Plans Board

The series roll-up line (`complete: 54%`, the ranked build queue, the blocked
count) is exactly what a project-status answer needs. Keep the per-episode and
series numbers in sync with whatever master status board the production is
tracked on so "where's the show" is answerable from one number without reopening
every tracker. The JSON is the source; the board is a human-facing mirror of it.

## Keeping it honest

- **One source of truth.** The renderer and registry write the tracker; humans
  edit it for creative state (notes, manual blocks) only. Two places to set
  status = drift.
- **Git-versioned** so progress is auditable and a bad bulk edit is revertible.
- **Don't over-tool it.** No Shotgun/ftrack for a solo/small series — a JSON file
  plus a status script beats a PM SaaS you won't keep updated. Scale the tool to
  the team.
- **Reconcile against reality** — a shot marked `done` whose rendered frames don't
  exist on disk is a lie; the status script should cross-check `done`/`comp`
  against actual files (and `asset-management`'s sha/registry) and flag mismatches.

## Verify

1. Run the status script over all episode trackers: it prints a per-episode and
   series-wide count by status, a % complete, and a blocked list — numbers that
   reconcile with the shot rows.
2. Delete/withhold one asset and run a renderer pass: the affected shots flip to
   `blocked: missing:<asset>` and appear in the ranked build queue, ordered by
   number of shots blocked.
3. Publish that asset in the registry and re-run: the shots auto-advance out of
   `blocked` and the queue entry disappears — no manual tracker edit.
4. Bump a used asset's version (`asset-management`): the shots using it show
   `needs_rerender: true` in the tracker and in the daily report, even though
   their status is still `done`/`comp`.
5. Mark a shot `done`, then remove its rendered output: the reconcile check flags
   the shot as a done/no-file mismatch rather than reporting the episode complete.

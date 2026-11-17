---
id: creative-arts.animation.pipeline.producing-scheduling
name: producing-scheduling
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, producing, scheduling, production-management, estimating, throughput, render-time, resourcing, blockers, priority, build-queue, planning]
level: advanced
status: draft
description: "Production management for a solo/automated studio: break an episode into tasks, estimate, schedule, resource render/compute, prioritize by shots unblocked."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Producing and scheduling (production management at solo/automated scale)

**Goal:** finish a 10-episode series on a believable timeline by always doing the work
that unblocks the most downstream work next — with realistic throughput, honest
estimates, and compute (render time) treated as the scarce resource it is. A feature
has a producer per department; here you *are* the producer, and the role compresses to
a few disciplines you must not skip, because there's no line producer to catch a
slipping plan.

This reads the data `production-tracking.md` exposes and the build queue
`pipeline-architecture.md` emits, and turns them into a *plan*.

---

## 1. Break the episode into tasks (the WBS)

An episode is not one job; it's a tree of tasks with dependencies. Decompose top-down:

```
Episode
├─ Assets (build-once, reused)
│   ├─ sets      (model → lookdev → lock)
│   ├─ characters(model → rig → lookdev → lock)
│   └─ props     (model → lock)
├─ Per-shot (×N shots)
│   ├─ VO        (generate → dialogue-edit → rhubarb)
│   ├─ layout    (stage/block)
│   ├─ render    (renderer pass)
│   ├─ comp      (grade/outline)
│   └─ review    (each gate)
└─ Episode-level
    ├─ assembly  (conform cut)
    ├─ mix       (dialogue + final mix)
    └─ delivery  (encode + captions + upload)
```

The key structural fact: **assets are build-once and shared; shots are per-shot but
cheap once assets exist.** So the schedule is dominated by (a) the asset build and (b)
render compute — not by per-shot labor, which the renderer automates.

---

## 2. Estimate (from your own measured throughput, not hope)

Estimate in ranges, from *measured* rates, and let the review log
(`dailies-review.md`) feed real numbers back:

- **Assets** — estimate per asset by complexity tier (hero character vs background
  prop), in days. These are the long poles; a hero character rig can outweigh 50 shots.
- **Shots** — mostly compute + a review pass, not hand-labor, *except* hero shots that
  need hand-animation on top of the renderer (`shot-renderer` §honest-limits). Split
  shots into **auto** (renderer handles it) and **hero** (needs hand work) — only hero
  shots carry significant per-shot labor estimates.
- **Rounds cost real time.** A shot averaging 2.3 review rounds (from the log) costs
  more than one marked "1 round". Use the logged round counts to calibrate — this is
  why the review log double-duties as the estimating dataset.
- **Pad for the unknown.** Early episodes run slow (building tools, finding the look);
  later episodes accelerate as assets and pipeline mature. Don't estimate EP10 at
  EP01's rate.

Track **estimate vs actual** per task so the next estimate is less wrong. An estimate
you never reconcile against reality never improves.

---

## 3. Schedule across the pipeline (dependencies first)

A schedule is the task tree ordered by dependency and resource:

- **Critical path = the asset build.** Shots can't render without their assets, so the
  asset build is almost always the critical path. Front-load it: the sooner the
  highest-leverage assets lock, the sooner the largest batch of shots can render
  unattended.
- **Overlap labor and compute.** Render (compute-bound, unattended) runs while you do
  layout/review (labor-bound, attended) on other shots. Never sit idle watching a
  render bar — queue the batch, work the next thing.
- **Gate the episode mix.** The mix (`final-mix.md`) can't start until all the
  episode's shots reach `comp`; the delivery can't start until the mix is done. These
  hard gates (`production-tracking` surfaces them) set the episode's end sequence —
  schedule backward from the publish date through them.
- **Pipeline-order the episodes too** — don't start EP07's layout while EP03's assets
  are still unbuilt if EP03 ships first.

---

## 4. The priority rule: build what unblocks the most shots

With limited time, the single most valuable decision each day is *what next*, and the
answer is data, not gut:

> **Model the asset that is blocking the most shots.**

The build queue (`production-tracking` / `pipeline-architecture` §5) ranks every
missing asset by shots-blocked. `set_catwalk` blocking 22 shots beats a prop blocking
1 — building it converts 22 blocked shots to renderable in one task. This is the
highest-leverage move and it requires no judgment: the queue already computed it.

Apply the same leverage logic to everything: fix the renderer bug that affects all
shots before the one-shot polish note; lock the character used in 5 episodes before the
one used in 1.

---

## 5. Resourcing compute (render time is the scarce resource)

At this scale the bottleneck isn't people, it's **GPU hours**. Treat render time like a
budget:

- **Measure cost-per-shot-minute.** Time a representative shot at ship settings
  (`../blender/render-optimization.md`), multiply by shot count for an episode render
  budget in GPU-hours. This is the number that sets whether a deadline is real.
- **Render overnight / unattended** — compute runs when you're not; schedule the big
  batch for off-hours, with the resumable batch (`pipeline-architecture` §6) so an
  overnight crash doesn't lose the night.
- **Spend the optimization effort where it multiplies.** A 20% per-frame speedup
  across 870 shots is worth far more than hand-tuning one shot. Optimize the common
  path (`render-optimization`, `../blender/render-aov-passes.md`).
- **Don't re-render what hasn't changed** — the hash-keyed skip-done
  (`pipeline-architecture` §6) *is* a resourcing tool: it stops you burning GPU-hours
  on finished work.
- **Cheap previews, expensive finals.** Review on fast low-sample renders; spend full
  samples only on approved shots.

---

## 6. Track progress and blockers (steer, don't discover)

- **The status report is the standup.** `production-tracking`'s daily report (series
  roll-up, ranked build queue, blocked list, stale list) is your morning read — it
  tells you % complete, what's next, what's stuck, in one glance.
- **Blockers are the only thing that won't move by itself.** A blocked shot waits
  forever without intervention; an in-progress shot advances. So triage blockers first
  each day: missing asset → build it (queue order); missing VO → generate it; stale
  (>N days in a state) → investigate why it's parked.
- **Burn-down, not burn-up.** Watch done/total trend toward the deadline; if the slope
  won't reach the date, cut scope or move the date *now*, not on delivery week.
- **Keep the Plans Board current.** The series roll-up line and build queue feed the
  master status board (`production-tracking` §Plans-Board) so "where's the show" is one
  number, always answerable.

---

## 7. Realistic throughput (the honesty that makes a plan a plan)

- **A solo/automated studio's throughput is dominated by asset build + render compute**,
  not animation labor — because the pipeline automates the per-shot base. Plan around
  those two, and the hero-shot hand-work, and ignore the fantasy that shot count alone
  sets the timeline.
- **Early slow, late fast.** Factor the ramp; tools and look stabilize over the first
  episodes.
- **Protect the long poles.** Anything on the critical path (hero assets, the mix
  gate) gets scheduled with slack; a one-shot polish does not.
- **Cut scope visibly, early.** When the slope misses the date, the lever is scope
  (fewer hero shots, simpler FX) decided in advance — not quality cut silently in the
  last week. A producer's job is to make that trade *on purpose*.

---

## 8. Worked example (scheduling one episode)

EP03, 87 shots, publish date in 3 weeks. Reading the tracker: 70 shots are **auto**
(renderer handles them), 17 are **hero** (need hand-anim). Build queue says
`set_alley` blocks 40 shots, `char_vera` blocks 14, three props block the rest.

- **Week 1 — critical path (assets).** Build/lock `set_alley` first (unblocks 40), then
  `char_vera` (14), then the props. As each locks, kick an overnight render batch of the
  now-unblocked auto shots — compute runs while week-1 labor continues.
- **Week 2 — hero labor + comp.** The 70 auto shots are rendering/rendered; spend
  attended time hand-animating the 17 hero shots and comping approved shots. Review
  gates run daily from the log.
- **Week 3 — episode tail.** Once all 87 reach `comp` (the mix gate), run the dialogue
  edit + final mix, then captions + encode + upload. Schedule these backward from the
  publish date; they're serial and ungated-around.

The plan falls straight out of the data: the build queue set week-1 order, the
auto/hero split set where labor goes, and the mix gate set the tail. No guessing — the
producer's job was reading the queue and sequencing the long poles.

## 9. Anti-patterns (producing failures that sink a small studio)

- **Idle compute.** Watching a render bar instead of queuing it and working the next
  task. Compute and labor must overlap.
- **Labor on auto shots.** Hand-touching shots the renderer covers — spend the hours on
  hero shots and the critical path.
- **Ignoring the queue.** Building a pretty one-shot prop while a 40-shot set sits
  unbuilt. Leverage, always.
- **Silent quality cut.** Discovering the deadline will miss in the last week and
  dropping quality to hit it. Cut *scope* early and visibly instead.
- **Estimating from hope.** Not reconciling estimate vs actual, so every estimate stays
  equally wrong. The review log is the calibration data — use it.

---

## Verify

1. **WBS exists.** The episode is decomposed into asset, per-shot and episode-level
   tasks with dependencies, and shots are split auto vs hero (only hero carry labor
   estimates).
2. **Estimates are measured.** Durations trace to a measured throughput/round count
   (from the review log and timed renders), not round guesses, and estimate-vs-actual
   is tracked.
3. **Critical path identified.** The schedule names the asset build / mix gate as the
   critical path and front-loads the highest-leverage assets.
4. **Priority is data-driven.** Ask "what next?" and the answer comes straight from the
   ranked build queue (most-shots-unblocked first), not opinion.
5. **Compute budgeted.** There's a GPU-hours-per-episode number from a timed
   representative shot, the big batch is scheduled unattended/resumable, and finished
   work is skipped by hash.
6. **Blockers triaged daily.** The daily status report drives the day: blocked and
   stale shots are actioned first, and the done/total slope is checked against the
   deadline with scope as the declared lever.

See `production-tracking.md` (status + build queue this plans from),
`pipeline-architecture.md` (the self-directing queue), `dailies-review.md` (round
counts feed estimates), `../blender/render-optimization.md` (compute budget),
`shot-renderer.md` (auto vs hero shots).

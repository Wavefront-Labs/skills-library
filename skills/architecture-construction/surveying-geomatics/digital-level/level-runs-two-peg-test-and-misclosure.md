---
id: architecture-construction.surveying-geomatics.digital-level.level-runs-two-peg-test-and-misclosure
name: level-runs-two-peg-test-and-misclosure
category: architecture-construction
field: surveying-geomatics
product: digital-level
tags: [digital-level, levelling, leveling, automatic-level, dumpy-level, auto-level, staff, bar-code-staff, benchmark, temporary-benchmark, tbm, reduced-level, rise-and-fall, height-of-collimation, two-peg-test, collimation-error, misclosure, closed-loop, change-point, backsight, foresight, surveying, geomatics]
level: practitioner
status: draft
description: "Run a closed level loop from a benchmark, book it rise-and-fall or HPC, check the two-peg test first, and judge and distribute the misclosure against an allowable tolerance."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Levelling — level runs, the two-peg test and misclosure

**Goal:** transfer heights from a benchmark to where you need them, and prove the
result by closing the loop back on a known height.

## 1. Before you start: the two-peg test
Every level has some collimation error (line of sight not truly horizontal). Test it:
1. Drive two pegs A and B about 30–60 m apart on firm ground.
2. Set the level exactly midway. Read staff on A and B. The difference (a1 − b1) is the
   **true** height difference — equal sight lengths cancel collimation error.
3. Move the level close to A (e.g. a few metres beyond it, on the line). Read A and B
   again; difference (a2 − b2).
4. Collimation error = (a2 − b2) − (a1 − b1) over the difference in sight lengths.
   Many specs allow around 1 mm per 20–30 m sight; beyond that, adjust (or use the
   digital level's built-in collimation routine) and repeat.
Do this at the start of a job, after any knock, and periodically.

## 2. Running the line
- Start on a benchmark (BM) or established temporary benchmark (TBM) with a known
  reduced level (RL). Note its source and datum.
- **Backsight (BS)** to the known point, **foresight (FS)** to the next change point (CP).
  Move the level, BS to that same CP, and so on.
- **Balance sight lengths** BS ≈ FS at every setup (pace or read the digital level's
  distance). This cancels any residual collimation error and much of curvature/refraction.
- Keep sights short — typically under 50–60 m, shorter in heat shimmer.
- Change points must be stable and well-defined: a change plate, a bolt, a sharp kerb
  corner. Never a soft spot or a stone that can rock.
- The staff holder keeps the staff **plumb** (use the staff bubble). A tilted staff always
  reads too high.
- **Close the loop:** finish on the starting BM or another known BM. An open line has no check.

## 3. Booking and reduction
Two standard methods:
- **Rise and fall:** for each consecutive pair, rise = previous reading − next reading.
- **Height of plane of collimation (HPC):** HPC = RL + BS; RL of next point = HPC − FS
  (or − intermediate sight). Faster for lots of intermediate sights (e.g. a site grid).
Arithmetic checks (always do them): ΣBS − ΣFS = ΣRise − ΣFall = Last RL − First RL.
Digital levels book automatically; still export and check the arithmetic and the
closure yourself.

## 4. Misclosure
Misclosure = computed RL of closing BM − known RL.
Allowable misclosure is usually written as **k·√L** (L in km) or **c·√n** (n = number of
setups). Values for k range from a few mm for precise work to ~10–12 mm/√km for ordinary
construction levelling — **use the figure in your project spec**.
If within tolerance, distribute the misclosure proportionally (per setup or per
distance) to the change points. If outside: re-run, don't adjust — something is wrong
(misread staff, staff on the wrong mark, a moved change point).

## Gotchas
- Reading the inverted-staff or wrong 100 mm block on E-pattern staffs: read and say aloud the metre/decimetre each time.
- Staff extension sections not fully locked: the staff reads short and you'll never see it in the closure if every reading uses the same section.
- Level sinking on soft ground between BS and FS: set the tripod firmly, read quickly.
- Digital levels can struggle in low light, with part of the bar code obscured, or with
  vegetation in front of the staff.
- Intermediate sights are not checked by the loop closure. Shoot important ones twice or
  from two setups.

## Verify
- [ ] Two-peg test done and within tolerance before the run.
- [ ] Sight lengths balanced at each setup.
- [ ] Loop closed on a known BM; arithmetic checks pass.
- [ ] Misclosure computed and within the specified allowable; distribution recorded.
- [ ] Critical intermediate levels independently checked.

*Uncertainty:* tolerance figures are typical; the project specification or national
standard governs.

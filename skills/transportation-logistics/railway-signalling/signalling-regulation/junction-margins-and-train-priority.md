---
id: transportation-logistics.railway-signalling.signalling-regulation.junction-margins-and-train-priority
name: junction-margins-and-train-priority
category: transportation-logistics
field: railway-signalling
product: signalling-regulation
tags: [signalling-regulation, train-regulation, regulating, regulation-policy, junction-margin, headway, planning-headway, flat-junction, conflicting-moves, train-priority, out-of-course-running, late-running, pathing, path, perturbation, perturbation-management, service-recovery, delay-minutes, reactionary-delay, knock-on-delay, signaller, controller, regulating-decisions, freight-path]
level: advanced
status: draft
description: "Make regulating decisions at a junction: compare margins and headways, apply the regulation policy, pick which train goes first to minimise total delay, and recover a perturbed service."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Junction margins and train priority

**Goal:** when two trains want the same piece of railway, choose the order that
causes the least total delay (and honours the regulation policy), early enough that
neither driver sees a needless red.

*Draft: regulation policies, priority classes and margin values are set per route by
the infrastructure manager and operators. Numbers below are illustrative only.*

## 1. Know your timings
For each junction and conflict point in your area, know:
- **Junction margin:** the minimum time between two conflicting moves (e.g. train A
  crossing, then train B on the conflicting route) — often 2–4 minutes on main lines.
- **Planning headway:** minimum time between following trains on the same line.
- **Running times** for each train type between your fringe and the junction: a
  freight takes much longer to reach it and longer to clear it.
- Where trains can be held without blocking others (loops, platforms) and where
  stopping a heavy freight costs most (rising gradient).

## 2. The core comparison
When A and B will conflict, estimate the delay to each under both orders:
```
Option 1: A first → B delayed by (A clears + margin) − B's arrival
Option 2: B first → A delayed by (B clears + margin) − A's arrival
```
Then weight by consequences:
- **Reactionary delay:** a delay to B that causes a missed connection or
  blocks a busy terminus may be worth far more than its minutes.
- **Policy:** the route's regulation policy may give explicit priorities (e.g. a
  train on time vs a late train, passenger vs freight in certain windows).
- **Stopping cost:** stopping a heavy freight on a gradient may cost 10+ minutes of
  restart time; checking a fast passenger train briefly costs little.

A well-known heuristic: **let the train that clears quickest go first** when delays
are otherwise equal — a fast train through a junction frees it sooner.

## 3. Decide early
- Make the decision when both trains are a few signals out, before either driver sees
  a restrictive aspect. A late decision converts a 1-minute check into a stop.
- Communicate with the adjacent signaller or control so they don't undo your plan.

## 4. Out-of-course and perturbation
- **Out-of-course trains** (late, early, extra): ARS and timetables mis-handle them;
  re-plan them explicitly (see
  transportation-logistics.railway-signalling.computer-based-control-centres.workstation-signalling-and-ars-supervision).
- **Perturbation:** after a blockage clears, don't release everything in arrival
  order. Agree a recovery plan with control: which trains are cancelled/short-formed,
  which go first, and how to re-establish the pattern.
- Give freight paths back — trapped freight becomes the next day's problem.

## 5. Review
Look at your delay attribution after the shift: which regulating decisions caused the
most reactionary delay, and what would you do differently?

## Gotchas
- "First come, first served" is a policy too — usually a poor one.
- Running times change with weather, adhesion and train formation.
- Holding a train in a platform blocks the platform for the next one.

## Verify
- [ ] You can state margins and running times for your key junctions.
- [ ] Conflicts decided before drivers see restrictive aspects.
- [ ] Decisions consistent with the regulation policy (or deviation logged with reason).
- [ ] Post-shift review of delay caused by your decisions.

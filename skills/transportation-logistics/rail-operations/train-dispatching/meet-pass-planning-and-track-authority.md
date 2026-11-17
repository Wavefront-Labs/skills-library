---
id: transportation-logistics.rail-operations.train-dispatching.meet-pass-planning-and-track-authority
name: meet-pass-planning-and-track-authority
category: transportation-logistics
field: rail-operations
product: train-dispatching
tags: [train-dispatching, dispatcher, rail-dispatcher, train-controller, meet-pass, meets-and-passes, passing-siding, single-track, ctc, centralized-traffic-control, track-warrant, track-warrant-control, twc, dtc, direct-traffic-control, form-d, track-authority, string-line, time-distance-graph, train-graph, conflict-resolution, disruption-recovery, service-recovery, siding-length, tonnage, priority-trains]
level: advanced
status: draft
description: "Plan meets and passes on a single-track territory with a string-line, issue track authority without overlap, and recover the plan when a train fails or runs late."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Meet-pass planning and track authority

**Goal:** move every train across your territory with the fewest total delay-minutes,
never allowing two movements authority on the same piece of track.

*Draft: authority systems differ — CTC signal indications, Track Warrant Control (TWC),
Direct Traffic Control (DTC), Form D, radio electronic token block. Copy/read-back
wording and forms are rule-specific; this covers the shared planning logic.*

## 1. The string-line (time-distance graph)
- X axis time, Y axis stations/sidings along the territory. Each train is a line; its
  slope is speed. **Where two lines cross is a meet (opposing) or pass (same direction).**
- Crossings must happen at a place able to hold one train clear: a siding long enough,
  a double-track section, a yard.
- Most dispatch systems draw this for you; sketch it by hand when learning — it
  forces you to see conflicts before they happen.

## 2. Choosing the meet point
For each conflict, list the candidate sidings and check:
1. **Fit:** the train going into the siding must fit (length vs clear siding length).
   Long trains often *must* hold the main.
2. **Who waits:** cost of delaying each train — priority (passenger, intermodal,
   hot shipments), crew hours remaining, tonnage (heavy trains are slow to restart
   and shouldn't be stopped on a grade).
3. **Timing:** both trains reach the meet point; the one arriving first takes the
   siding (or holds) only if the other is truly close. Stopping a train 40 minutes
   early at a siding is a planning failure.
4. **Knock-on:** does this meet create a new conflict further on? Look one or two
   meets ahead.

Rule of thumb: the "rolling meet" (one train enters the siding just as the other
arrives) is ideal; anticipating it requires accurate running times — learn your
territory's real times per train type, not the timetable's.

## 3. Issuing authority
- One movement authority per block/limit at a time; check your sheet/system for any
  existing authority (trains, maintenance-of-way foremen, hi-rail vehicles) on those
  limits before issuing.
- **Repeat-back discipline:** the receiver reads back every item; you confirm only
  after an exact match. Spell location names and track numbers if ambiguous.
- Release: don't re-issue the limits until the previous holder has reported clear
  (and, where required, that the full train is clear — rear-end confirmation).
- Maintenance windows: protect work limits with blocking devices/system blocks *before*
  giving the work group their authority.

## 4. Recovery when it goes wrong
- **Failed train:** protect it first (no authority into its limits), then decide:
  assist from behind/ahead, or terminate following trains elsewhere.
- **Re-plan from the bottleneck:** identify the single-track section now overloaded
  and sequence trains through it by priority, accepting delay elsewhere.
- Communicate early to crews and adjacent dispatchers; crews near hours-of-service
  limits need relief arranged before they expire on the main line.

## Gotchas
- Siding "length" on paper vs usable length (a car left at one end, a fouling point).
- A train that "will be there in five minutes" usually isn't; plan on observed times.
- Never issue authority from memory — always from the current sheet/system state.

## Verify
- [ ] Every meet on the plan uses a location that fits the train taking the siding.
- [ ] No two authorities overlap on your sheet/system.
- [ ] Every authority read back verbatim and released before re-issue.
- [ ] Delay-minutes reviewed after the shift; worst meet decision identified.

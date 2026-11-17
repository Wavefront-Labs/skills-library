---
id: transportation-logistics.spaceflight-spacecraft-operations.launch-range-operations.countdown-holds-and-launch-commit-criteria
name: countdown-holds-and-launch-commit-criteria
category: transportation-logistics
field: spaceflight-spacecraft-operations
product: launch-range-operations
tags: [launch-operations, countdown, launch-campaign, built-in-hold, hold, recycle, scrub, launch-commit-criteria, lcc, weather-rules, lightning-launch-commit-criteria, upper-level-winds, range-safety, flight-termination, afts, launch-director, launch-window, go-no-go-poll, propellant-loading, notam, hazard-area, range-clear]
level: advanced
status: draft
description: "Running a launch countdown: built-in holds, launch commit criteria (vehicle, range and weather), range-clear and hazard areas, hold/recycle/scrub decisions within a window."
sources: ["NASA/USSF public launch weather criteria (Lightning Launch Commit Criteria summaries)", "FAA 14 CFR Part 450 public guidance", "Public launch provider countdown timelines"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Countdown, holds and launch commit criteria

**Goal:** get to T-0 with every criterion green — and when one isn't, make the
hold, recycle or scrub decision fast and by rule, not by hope.

## 1. Structure of a countdown
- The count is a **scripted timeline** (the "countdown procedure") with numbered steps,
  owners and T-minus times, plus **built-in holds** at fixed points to absorb slips
  without moving later steps.
- Typical phases (vary by vehicle): vehicle power-up and checks → range readiness and
  weather briefing → **Go/No-Go poll for propellant loading** → loading (cryogenics
  last-minute on dense-propellant vehicles) → terminal count with automated sequencer
  → engine start → liftoff.
- In the terminal count the **auto-sequencer** owns the vehicle; humans can only
  hold. Know the last time a manual hold can be called and which holds are recyclable.

## 2. Launch commit criteria (LCC)
LCC are **pre-agreed red lines**: if violated at T-0, no launch. Three families:
1. **Vehicle LCC:** tank pressures and temperatures, engine readiness, avionics
   health, flight termination system (FTS) armed and checked.
2. **Range LCC:** range clear of ships and aircraft (hazard areas, NOTAMs and
   navigational warnings active), tracking and telemetry assets Go, range safety
   (or autonomous FTS) ready, collision-avoidance (COLA) closures respected.
3. **Weather LCC:** ground winds at pad, upper-level winds and shear (loads), and the
   **lightning rules** — e.g. no launch through cumulus clouds with tops colder than
   a set temperature, within set distances of lightning or anvil clouds, or with high
   field-mill readings. Natural and *triggered* lightning (the vehicle's exhaust plume
   triggers strikes) are both concerns. For crewed flights, **abort/recovery-zone
   weather** (sea state, winds) is also commit-critical.
*Exact numbers belong to each range/provider; don't quote them from memory.*

## 3. Holds, recycles and scrubs
- **Hold:** stop the clock at the next safe point to work an issue. State the
  problem, the owner, and the time to resolve.
- **Recycle:** return to an earlier point in the count (e.g. T-10 min) and try again.
  Limited by window length, propellant (boil-off, top-off limits), and how many
  recycles the vehicle/ground system tolerate.
- **Scrub:** stand down for the day. Triggers: issue can't be resolved inside the
  window, a criterion stays red, too many recycles, or crew/team fatigue limits.
- The **launch director** owns the call after a poll; each console states Go/No-Go
  plainly (see flight-control console work).
- For instantaneous windows (rendezvous, planetary), there is no recycle — any hold in
  terminal count is a scrub.

## 4. Turnaround after a scrub
- Safe the vehicle (drain propellants, secure FTS), record the cause.
- Determine next opportunity: window, range availability, weather outlook, propellant
  resupply, crew rest.
- Refresh COLA screening and NOTAMs for the new date/time.

## Gotchas
- "Go fever": a long-delayed campaign biases the room toward accepting marginal
  conditions — rules exist precisely for that moment.
- A criterion waiver must follow the written waiver process, not happen on the loop.
- Clock mismatch between sequencer, range and COLA closures can launch into a closed
  second — verify UTC sync in pre-count checks.

## Verify
- [ ] Every LCC has an owner reporting it at the final poll.
- [ ] Hazard areas confirmed clear and warnings active before terminal count.
- [ ] Recycle limits (propellant, count) known before the window opens.
- [ ] COLA closures loaded into the sequencer timeline.
- [ ] Scrub/turnaround plan exists in writing before day of launch.

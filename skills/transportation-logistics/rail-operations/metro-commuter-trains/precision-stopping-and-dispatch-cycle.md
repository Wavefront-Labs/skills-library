---
id: transportation-logistics.rail-operations.metro-commuter-trains.precision-stopping-and-dispatch-cycle
name: precision-stopping-and-dispatch-cycle
category: transportation-logistics
field: rail-operations
product: metro-commuter-trains
tags: [metro-commuter-trains, metro, subway, underground, commuter-rail, emu, dmu, multiple-unit, train-operator, train-driver, platform-stopping, stopping-marker, platform-overrun, sprt, short-platform, door-cycle, door-interlock, platform-train-interface, pti, dwell-time, dispatch, ato, automatic-train-operation, cbtc, timetable-recovery, headway]
level: practitioner
status: draft
description: "Drive a metro or commuter multiple-unit: brake to the correct stop marker every time, run a safe door and dispatch cycle, supervise ATO, and recover lost time without cutting safety margins."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Precision stopping and the door/dispatch cycle

**Goal:** stop at the right marker for the train length at every station, open the
right doors, close them without trapping anyone, and keep headway — hundreds of
times a shift without one wrong-side release or overrun.

*Draft: stopping-marker conventions, door-control sequences and ATO modes are
operator- and fleet-specific; follow your traincrew manual.*

## 1. Braking to the marker
- **Know the marker for your train length** (e.g. 4-car, 8-car, 12-car boards). Say
  it to yourself on approach: "eight-car, far end".
- Brake in **one smooth initial application** at a consistent point, then *ease off*
  as speed falls so the train stops without a jolt — the classic "two-stage" stop.
  Avoid "fishing" with repeated apply/release.
- Use fixed reference points (a lamp post, the platform ramp) learned in route
  knowledge as your braking point; adjust for **rail adhesion**: wet leaves, first
  rain after a dry spell, frost.
- Low adhesion: brake earlier and lighter; let wheel-slide protection work rather
  than releasing; report it.
- **Overrun** past the marker: stop, don't release doors, follow your rules (usually
  contact the signaller/control before setting back).

## 2. Door cycle
1. Train fully stopped, brake applied.
2. **Confirm platform side** — wrong-side door release is a major safety event.
   Check: the platform is physically there on that side, selective door operation
   (SDO) set correctly for a short platform.
3. Release/open doors on the correct side.
4. Watch the dwell — on CCTV/mirrors or by direct sight per your role (driver-only
   operation vs guard-operated).
5. **Closing:** give the audible warning, close, and **check the platform-train
   interface** before moving — the door interlock light ("doors closed and locked")
   does *not* prove nobody is trapped by a bag strap or coat.
6. Take power only when doors interlocked *and* the signal/dispatch authority is
   correct.

## 3. ATO supervision
- In ATO, you are the safety backstop: monitor the stop, door enable, and departure;
  be ready to intervene (e.g. over-run, obstruction, person on track).
- Know your fleet's mode transitions (ATO ↔ manual protected) and their speed limits.
- Report repeated ATO misses at one station — often a calibration or adhesion issue.

## 4. Recovering lost time
- Recover through **disciplined dwell** (start closing as soon as the flow stops) and
  running to the line speed, never by braking later than normal or taking power before
  checks.
- If a train ahead is late, holding back to even out headway (instructed by control)
  usually improves the service more than racing up behind it.

## Gotchas
- Fatigue errors cluster on the most familiar routes: verbalise checks.
- Starting against a red: "ding-ding and away" — always look at the signal/authority
  as a separate check from the dispatch signal.
- Reopening doors for a late passenger costs more time than it saves at peak.

## Verify
- [ ] Each stop: correct marker, smooth stop, no fishing.
- [ ] Each door release: correct side confirmed by sight, SDO correct.
- [ ] Each departure: interlock *and* PTI check *and* signal check.
- [ ] Low-adhesion and ATO anomalies reported.

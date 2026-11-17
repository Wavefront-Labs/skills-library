---
id: transportation-logistics.rail-operations.yard-marshalling.switch-list-and-hump-operations
name: switch-list-and-hump-operations
category: transportation-logistics
field: rail-operations
product: yard-marshalling
tags: [yard-marshalling, classification-yard, marshalling-yard, hump-yard, flat-yard, switch-list, switching-list, cut-list, classification, block, blocking, train-building, breaking-up-trains, hump-sequencing, retarders, bowl-tracks, pull-back, trim-job, securement, handbrakes, hand-signals, lamp-signals, yardmaster, switchman, shunter, ground-crew]
level: practitioner
status: draft
description: "Execute a switch list in a flat or hump yard: plan cuts, sequence the hump, build trains in block order, secure what's left, and use hand and radio signals without ambiguity."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Switch lists and hump operations

**Goal:** break inbound trains into their destinations and build outbound trains in
the correct block order, with the fewest moves, no misroutes and no runaways.

*Draft: hump speeds, retarder control, securement tables and hand-signal meanings
vary by railroad/country. Treat as generic practice.*

## 1. Read the switch list before you touch a car
- A switch list gives each car (in standing order) and its destination track. Mark it:
  draw lines between cuts — consecutive cars going to the same track move as one cut.
- **Count moves**: fewer cuts = fewer moves. If two adjacent cars go to the same
  track, keep them together.
- Flag special cars: dangerous goods (often with handling/coupling restrictions and
  "do not hump" rules), long cars, cars with defective brakes (bad orders),
  high-wide loads.
- Confirm track capacity: the destination track has room for the cars you'll send.

## 2. Flat-yard switching
- Sequence: pull the cut, line switches, shove/kick to the track, return. Plan so you
  line each switch once where possible and work from the far tracks inward or by
  ladder order.
- Ground crew lines and checks every switch point ("points closed, locked if
  required"), confirms derails, and protects the leading end of shoves.

## 3. Hump operations
1. **Pre-hump:** air bled off cars (so brakes don't drag in the bowl), cuts uncoupled
   per the cut list (pin pulled), "do not hump" cars removed or flagged.
2. **Hump speed:** the hump engine shoves at a slow, steady speed so cuts separate
   at the crest with enough gap for switches to throw between them.
3. Retarders and automated switches route each cut to its bowl track; watch for
   stalls (cuts stopping short — "couplings short") and overspeed impacts.
4. **Trim jobs** at the far end pull cuts together, couple up stalled cars and fix
   misroutes.
5. Hump crew reports misroutes immediately so the cut list can be corrected.

## 4. Building outbound trains
- Block order from the train plan (e.g. furthest destination at the rear or front per
  local plan), dangerous-goods placement rules, and train-make-up rules (heavy cars
  forward, empty/load restrictions, long-short car combinations).
- Couple, stretch, then air test (see
  transportation-logistics.rail-operations.conducting-onboard-operations.train-brake-tests-and-dispatch).

## 5. Securement
Before leaving any cut: apply the number of handbrakes the securement table requires
for grade and tonnage, test them, and keep clear of fouling points. Bowl tracks on a
grade need special care — rolling cars are the main yard hazard.

## 6. Signals
- Hand/lamp signals are only valid when the receiver can clearly see them; when out of
  sight, use radio with car-count instructions. **Any signal not understood = stop.**
- Radio: identify yourself, the move and the locomotive each time.

## Gotchas
- A "short" cut in the bowl leaves a gap that the next cut hits hard.
- Bad-order cars humped by mistake — always check the list for holds.
- Track capacity counted in cars, not metres, misleads with mixed long/short cars.

## Verify
- [ ] Switch list marked into cuts and move count minimised before starting.
- [ ] Special and do-not-hump cars identified and handled separately.
- [ ] Outbound train in correct block order and placement rules met.
- [ ] Every cut left in a track is secured per table.

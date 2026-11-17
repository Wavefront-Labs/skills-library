---
id: transportation-logistics.air-traffic-control.ground-control.taxi-routing-and-clearance-delivery
name: taxi-routing-and-clearance-delivery
category: transportation-logistics
field: air-traffic-control
product: ground-control
tags: [air-traffic-control, atc, ground-control, clearance-delivery, taxi-clearance, taxi-routing, pushback, start-up, ifr-clearance, cram, departure-clearance, pdc, dcl, cpdlc, hold-short, progressive-taxi, low-visibility-procedures, lvp, smgcs, a-smgcs, hot-spots, follow-me, vehicle-control, manoeuvring-area]
level: practitioner
status: draft
description: "Deliver IFR departure clearances, coordinate pushbacks and give unambiguous taxi routes, including low-visibility ground operations and hot-spot handling."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Taxi routing and clearance delivery

**Goal:** every aircraft leaves the gate with the right clearance, taxis a route it
understands, and never meets another aircraft nose-to-nose or strays onto a runway.

> Draft: general practice; local ground movement charts, "hot spots" and LVP
> procedures define the real routes. Phraseology examples use ICAO-style wording.

## 1. Clearance delivery
Order of an IFR clearance (memorise as **CRAFT**): **C**learance limit, **R**oute,
**A**ltitude (initial), **F**requency (departure), **T**ransponder code.
1. Check the filed route against the flight plan system and any flow restriction
   (slot/CTOT, EDCT) before you call.
2. Read it in that order, at a pace the crew can write.
3. **Hearback** every element; correct immediately ("negative, climb via SID
   altitude 5,000").
4. Datalink (PDC/DCL via ACARS or CPDLC): confirm the crew has accepted; a revised
   route after acceptance must go by voice or a new message, never assumed.
5. Mark the strip "cleared" so nobody re-issues or forgets.

## 2. Pushback and start
- Ask: Is the taxilane behind clear? Is another push or taxi using it in the next
  2–3 minutes? Is there a slot that makes starting now wasteful?
- Phrase the direction: "push back approved, face east/tail north". Ambiguity on
  facing direction blocks taxilanes.
- Two adjacent pushes into the same lane: approve one, "expect push in two minutes"
  for the other.

## 3. Writing a taxi route
1. **Plan the full route** on the chart before transmitting, using standard routes
   if published.
2. Transmit: destination → route → holding point → any hold-short. E.g.
   "Taxi holding point A1 runway 27 via B, C, hold short of runway 22."
3. **Every runway crossing is an explicit clearance** — never implied by a route.
   Many States require an explicit "cross" or "hold short" for each runway on the route.
4. Split long routes ("taxi via B, hold short of C") if traffic will need resequencing.
5. Avoid published **hot spots** or give a warning ("caution, hot spot 2,
   short taxiway geometry").
6. Unfamiliar crew or confusing layout → **progressive taxi** or a follow-me.

## 4. Deconflicting the surface
- Same taxiway, opposite directions = conflict. Resolve with "give way to the
  B737 crossing left to right" (only when both see each other) or a hold.
- Sequence for the runway by the departure order tower wants (wake category, SID
  divergence, slot time), not first-come.
- Vehicles: issue a separate clearance with the same discipline; tug and tow
  movements count as aircraft.

## 5. Low-visibility ground operations
Once LVPs are active (local triggers, often RVR < ~550 m or cloud base below ~200 ft):
- Reduce simultaneous movements; one aircraft per segment where you can't see.
- Use stop bars and centreline lights or A-SMGCS routing; require position reports.
- Protect the ILS sensitive/critical areas — hold at the LVP holding points, not the
  normal ones.
- Expect slow taxi; space departures accordingly and tell tower.

## Gotchas
- A crew that reads back "hold short" incorrectly *will* cross. Insist on the full
  hearback.
- Frequency transfers mid-route lose context: give the remaining route before switching.
- Construction NOTAMs change the map — read them at position takeover.

## Verify
- [ ] Each clearance followed CRAFT order and was fully read back.
- [ ] Every runway crossing had an explicit cross/hold-short instruction.
- [ ] Taxi routes avoid or warn about hot spots.
- [ ] Under LVP you used LVP holding points and protected ILS areas.
- [ ] Strips/EFS show who is cleared, pushing, taxiing and at the holding point.

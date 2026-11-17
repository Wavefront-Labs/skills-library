---
id: architecture-construction.construction-equipment-operation.tower-crane.making-a-blind-lift-with-a-dogman
name: making-a-blind-lift-with-a-dogman
category: architecture-construction
field: construction-equipment-operation
product: tower-crane
tags: [construction-equipment-operation, tower-crane, hammerhead-crane, luffing-jib-crane, flat-top-crane, blind-lift, dogman, banksman, signaller, slinger-signaller, rigger, radio-signals, hand-signals, load-swing, slew-control, trolley, luffing, anemometer, wind-limit, hook-time, crane-coordinator, bs-7121-5, as-2550-4, osha-1926-1419, mewp-landing]
level: practitioner
status: draft
description: "Making a blind tower crane lift guided by a dogman or banksman: radio protocol, slew and hoist control, load swing damping, and wind-limit stop decisions."
sources: ["BS 7121-5 Safe use of cranes - Tower cranes", "AS 2550.4 Tower cranes", "OSHA 29 CFR 1926.1419-1422 Signals"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Making a blind lift with a dogman

**Goal:** land a load the operator cannot see, accurately and without swing, by flying
it on the dogman's (AU) / banksman's or signaller's (UK) / signal person's (US)
directions, and knowing when to stop.

Only licensed or certified tower crane operators and signallers may do this, under
the site lift plan and the crane manufacturer's limits. Follow your local regulation.

## 1. Before the first lift of the shift
- Pre-start checks per the manufacturer and site: limits (hoist up, trolley in/out,
  slew zoning, rated capacity), brakes, anemometer reading, radio batteries.
- **Radio check** on the dedicated crane channel. Agree:
  - who controls the load (one voice at a time — hand over explicitly: "you have the
    load" / "I have the load");
  - the call sign, and the "all stop" word that anyone may use;
  - what happens if the radio goes silent: the operator **stops** and waits. Many sites
    require continuous talk so silence is noticed (e.g. "travel… travel… travel").
- Confirm the load weight and radius against the crane's load chart/radius plate, and
  that the trolley/luff is within the duty for that weight.

## 2. Radio protocol during the lift
Directions are given in the operator's frame or in agreed site directions — settle
which before you start. Typical sequence:
1. "Take the weight" — hoist slowly until slings are tight; pause for the dogman to
   check balance and rigging.
2. "Hoist up, slow" — clear of obstruction by a planned margin (often ~1–2 m).
3. "Slew left/right", "trolley out/in" or "luff up/down" with distance calls
   ("ten metres… five… two… one… stop").
4. "Lower, slow", "dead slow", "stop", "land it", "slack off".
Operator repeats back any unusual command before acting. If a call is unclear, stop.

## 3. Control technique
- **Feather the controls.** Ramp up and down — snapping from full speed to stop sets
  up a pendulum. Most modern cranes have stepless controls; use the first steps for
  final positioning.
- **Chase the swing.** If the load swings out, gently move the hook in the direction
  of the swing as it reaches the far end, then ease off — this damps it. Do not
  fight it by reversing hard.
- Slew and trolley/luff together only when the load is well clear; near landing, move
  one function at a time.
- Lower to about 300 mm (1 ft) above the landing, stop, let the dogman steady it with
  tag lines, then land on dunnage so slings can be removed.
- Never let anyone stand under the load or between the load and a fixed structure.

## 4. Wind and stopping decisions
- Check the cab anemometer reading regularly, and gusts, not just average. The
  manufacturer gives an in-service limit — often in the region of 20 m/s (about
  72 km/h, 45 mph) for the crane itself (unverified — read your crane's manual).
- Large-area loads (formwork, panels, glazing, cages) must stop far below that; the
  site lift plan or a sail-area calculation sets the figure, frequently 10–14 m/s
  (unverified — calculate per load).
- When out of service, the crane must weathervane: slew brake released per manual.
- Lightning in the area, loss of visibility to the dogman's position, or a
  communication failure: stop and land if safe.

## Gotchas
- Two people talking on the channel at once → the operator follows the wrong voice.
- Shadowed blind spots change as the building rises; re-brief when floors are added.
- Long hoist ropes make loads slow to swing but large in amplitude — be patient.
- Taglines are for control, not for dragging a load into place against the crane.
- Overlapping cranes: follow the anti-collision zoning and coordinator calls.

## Verify
- [ ] Radio check done; single controlling voice and stop word agreed.
- [ ] Load weight and radius within the chart for the trolley/luff position.
- [ ] Load landed without swing, on dunnage, with nobody beneath it during flight.
- [ ] Wind checked against the crane and the load-specific limits.
- [ ] Any unclear or lost signal resulted in a stop, not a guess.

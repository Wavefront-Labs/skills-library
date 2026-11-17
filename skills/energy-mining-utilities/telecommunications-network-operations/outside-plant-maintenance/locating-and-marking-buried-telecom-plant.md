---
id: energy-mining-utilities.telecommunications-network-operations.outside-plant-maintenance.locating-and-marking-buried-telecom-plant
name: locating-and-marking-buried-telecom-plant
category: energy-mining-utilities
field: telecommunications-network-operations
product: outside-plant-maintenance
tags: [outside-plant-maintenance, telecommunications-network-operations, osp, cable-locating, utility-locating, locate-ticket, one-call, 811, call-before-you-dig, damage-prevention, radiodetection, vivax, 3m-dynatel, transmitter-receiver, direct-connection, inductive-clamp, induction, tracer-wire, peak-mode, null-mode, depth-estimate, signal-bleedover, apwa-colour-code, orange-paint, marker-flags, sonde, duct-rodder, fibre-locating]
level: practitioner
status: draft
description: "Locate and mark buried telecom cable and duct for a dig: choose direct connect, clamp or induction, read peak vs null, check depth and bleedover, mark to APWA colours, and record the locate."
sources: ["Common Ground Alliance Best Practices (public, paraphrased)", "Radiodetection / Vivax locator manuals (general principles)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Locating and marking buried telecom plant

**Goal:** answer a locate request (a "one-call" or 811 ticket in the US, similar
schemes elsewhere) by finding and marking your company's buried cable and duct
accurately enough that the excavator doesn't hit it — and know when the locate isn't
good enough and you must say so.

## 1. Before you go
- Read the **ticket**: excavation area, type of work, start date, due-by time.
  Missing the deadline usually lets the excavator proceed.
- Pull the **plant records**: cable routes, depths if recorded, ducts, tracer-wire
  access points, splice points and pedestals. Records are a guide, not proof.
- Check the locator battery and transmitter, clamp, ground stake, leads, paint
  (orange for communications in the APWA colour code), flags.

## 2. Put a signal on the line
In order of preference:
1. **Direct connection:** clip the transmitter to the cable's shield or tracer
   wire at a pedestal or test point, ground stake well away (several metres) and at
   right angles to the cable route. Strongest and most selective signal.
2. **Inductive clamp** around the cable at an access point — no metallic contact
   needed, good on live cables.
3. **Induction** from the transmitter placed on the ground over the route — easiest,
   but energises everything nearby. Use only when nothing else is possible.
Choose frequency: lower (e.g. ~8 kHz) travels further with less bleed onto other
utilities; higher (e.g. ~33 kHz and up) couples more easily through poor grounds and
breaks but bleeds more. Locator models differ; check yours.
**Non-metallic fibre** with no tracer wire can't be located electronically — use a
sonde pushed through the duct or rely on records and marker balls; tell the
excavator the locate is records-based.

## 3. Trace the route
- **Peak mode:** maximum signal directly over the cable — good for accuracy.
- **Null mode:** minimum directly over the cable — sharp but easily fooled by
  distorted fields.
- Compare them: if peak and null positions disagree by more than a few centimetres,
  the field is distorted (another utility nearby, a bend, a tee). Mark a wider
  tolerance zone and say so.
- Check **signal current/direction** if your locator shows it: a strong signal on a
  line with the wrong direction is **bleedover** onto someone else's plant.
- Walk the full excavation area plus a margin, sweeping across the route every few
  metres; check for branches and drops to buildings.

## 4. Depth
Take depth readings only where the signal is clean and the cable straight; readings
over bends and near other utilities are unreliable. Depth markings are informative —
excavators must still expose by hand digging within the tolerance zone (commonly
~45–60 cm / 18–24 in each side, by jurisdiction).

## 5. Mark and record
- Orange paint dashes and/or flags along the centreline, closer spacing at bends;
  mark the company code and the width for a duct bank.
- Photograph the marks with location; close the ticket with status (marked, clear,
  or unable to locate with reason).
- If the site has changed (new road, re-grading), note it — records may be wrong.

## Gotchas
- A good signal on the wrong cable is worse than none — always check the return
  current and direction.
- Shared trenches: power and telecom often run together; induction mode lights up
  both.
- Paint fades or gets dug off; refresh for long jobs per the scheme's rules.
- Uncertain: tolerance zones, colour codes and ticket timings vary by country and
  state — check the local one-call law.

## Verify
- [ ] Ticket area, deadline and records reviewed.
- [ ] Direct connect or clamp used where possible; frequency chosen for the site.
- [ ] Peak and null agree (or a wider zone marked and explained).
- [ ] Signal direction confirmed to avoid marking bleedover.
- [ ] Marks photographed and ticket closed with the right status.

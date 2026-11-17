---
id: transportation-logistics.maritime-navigation-seamanship.radar-arpa.radar-tuning-and-collision-plotting
name: radar-tuning-and-collision-plotting
category: transportation-logistics
field: maritime-navigation-seamanship
product: radar-arpa
tags: [radar-arpa, radar, arpa, marine-radar, maritime-navigation-seamanship, x-band, s-band, gain, sea-clutter, rain-clutter, ftc, stc, cpa, tcpa, true-vectors, relative-vectors, sea-stabilised, ground-stabilised, target-acquisition, trial-manoeuvre, parallel-indexing, ebl, vrm, radar-plotting, collision-avoidance, colregs]
level: practitioner
status: draft
description: "Tune marine radar (gain, sea and rain clutter), acquire ARPA targets, read CPA/TCPA with correct true/relative and sea/ground stabilisation, run a trial manoeuvre and set up parallel indexing."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Radar tuning and collision plotting — see the small target, judge it right

**Goal:** get a radar picture that shows small and weak targets, use ARPA data
correctly to judge risk of collision, and use the radar for position monitoring.
Control names vary by maker; functions are standardised under IMO performance standards.

## 1. Tune the picture (repeat whenever range or conditions change)
1. **Band:** X-band (3 cm) gives finer detail and sees SARTs; S-band (10 cm) sees
   better through rain and sea clutter. Use both if fitted.
2. **Range scale:** long range for early detection, a shorter one alongside for
   detail; don't stay on one scale.
3. **Gain:** increase until a light speckle of background noise just appears, then
   back off slightly. Too low hides weak targets.
4. **Sea clutter (STC/anti-sea):** reduce until clutter near the centre breaks up into
   speckle — not until it's black. Over-suppression erases small boats.
   Automatic modes are useful but check against manual.
5. **Rain clutter (FTC/anti-rain):** apply only as needed to see inside a rain cell.
6. Pulse length: short at short range (resolution), long at long range (detection).
7. Check **performance monitor** and heading line alignment (a heading marker
   error shifts every bearing).

## 2. Acquire and read ARPA targets
- Acquire targets of interest manually or by guard zones; allow **~1 min for trend,
  ~3 min for full accuracy** after acquisition or after either vessel manoeuvres.
- **Relative vectors** show whether a target will pass close: extend the vector — if
  it passes through or near your position, risk exists. Read **CPA/TCPA**.
- **True vectors** show target aspect/heading — what the other ship is doing and so
  which COLREG situation applies.
- **Sea-stabilised** (log speed through water + gyro) shows heading and aspect correctly
  — use it for **collision avoidance**. **Ground-stabilised** (GNSS speed over ground)
  is right for navigation; in current it gives misleading target aspect.
- Check AIS association but remember AIS data can be wrong or absent; radar is the
  primary sensor for collision avoidance.

## 3. Trial manoeuvre
Enter proposed course/speed alteration and delay time; the ARPA shows resulting CPAs
for all targets. Check that the alteration clears **every** target to your minimum
CPA (company SMS often states e.g. 1–2 nm open sea) and doesn't create a new close
quarters situation. Then execute and **check the result** once vectors settle.

## 4. Manual plotting (when ARPA is unreliable or as a check)
Plot a target over 6 min at fixed intervals: O (first) → A (after 6 min). Your own
motion vector W→O over the same time. Relative track O–A extended gives CPA; the true
vector W–A gives the target's course and speed. Practising this keeps you able to
spot ARPA errors from wrong speed input or gyro errors.

## 5. Parallel indexing (position monitoring)
1. On the plan, choose a radar-conspicuous object (headland, isolated rock, edge of
   a breakwater).
2. Draw a line parallel to the planned track at the object's planned passing distance.
3. On the radar, set an **index line** (or EBL offset/VRM) at that perpendicular
   distance, in a heading-up or north-up stabilised display as planned.
4. Keep the echo of the object on the index line: drifting off it shows cross-track
   error immediately, independent of GNSS. Add clearing lines for danger limits.

## Gotchas
- Small craft, ice and wooden boats can vanish in clutter — look out visually too.
- Wrong speed input (log fault) corrupts sea-stabilised vectors.
- Radar shadow sectors behind masts and cranes: know your blind sectors.
- "Assumptions on scanty radar information" — COLREG rule 7 warns against them.

## Verify
- [ ] Picture retuned after range or weather change; light speckle visible.
- [ ] Collision avoidance judged on sea-stabilised data with settled vectors.
- [ ] Trial manoeuvre checked for all targets before action; result re-checked.
- [ ] Parallel index lines prepared for coastal legs and in use.

*Uncertainty:* acquisition times and CPA limits are typical; check your equipment manual and SMS.

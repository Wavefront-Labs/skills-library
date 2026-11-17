---
id: handcrafts.manual-machining.manual-turning.single-point-screw-cutting-on-the-lathe
name: single-point-screw-cutting-on-the-lathe
category: handcrafts
field: manual-machining
product: manual-turning
tags: [manual-turning, lathe, engine-lathe, centre-lathe, center-lathe, screw-cutting, thread-cutting, single-point-threading, threading-tool, 60-degree, metric-thread, unified-thread, un, whitworth, 55-degree, thread-dial, threading-dial, half-nut, leadscrew, quick-change-gearbox, change-gears, compound-slide, 29-5-degree, compound-infeed, centre-gauge, fishtail-gauge, thread-pitch-gauge, three-wire, thread-micrometer, undercut, chamfer, internal-thread, machinist]
level: practitioner
status: draft
description: "Cut an external 60° thread on a manual lathe: gear the leadscrew, grind and set the tool, feed with the compound at 29.5°, use the thread dial or keep the half-nuts closed, and gauge the fit."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Single-point screw cutting on the lathe

**Goal:** an external metric or unified 60° thread, cut on a manual lathe, that a
standard nut or a ring gauge screws onto smoothly without shake.

## 1. Prepare the blank
- Turn the major diameter **slightly under** nominal: about 0.1–0.15 mm under for
  M10–M20 (a common shop allowance; check thread tables for the class of fit).
- Chamfer the start at 45° down to just below the minor diameter.
- Cut a **thread relief undercut** at the end (width ≥ 2× pitch, depth just under
  minor diameter) if the thread runs up to a shoulder — it gives you somewhere to
  stop.
- Thread depth (external, 60°): roughly **0.613 × pitch** for metric (e.g. M12×1.75 →
  ~1.07 mm). Infeed on the compound at 29.5° is that depth ÷ cos 29.5° ≈ 1.15 × depth.

## 2. Gear the lathe
- Set the quick-change gearbox (or change gears) for the pitch from the lathe's chart.
- **Metric on an imperial leadscrew** (or vice versa) needs a translating gear (often
  127 teeth) and the half-nuts must **stay closed** for the whole job — the thread
  dial won't track. Same-system threads can use the thread dial.
- Speed: slow — 60–150 rpm for steel at hobby scale, slower near a shoulder.

## 3. Grind and set the tool
- Grind HSS to a 60° included angle against a **centre gauge (fishtail)**; small flat
  or radius at the tip (~0.125 × pitch for metric). Or use a carbide insert of the
  correct pitch.
- Tool exactly on centre height.
- Swing the **compound to 29.5°** (on most lathes measured from the cross-slide
  axis — check which side your scale reads; the infeed should take metal off the
  trailing flank).
- Square the tool to the work with the centre gauge against the true-running blank.

## 4. Cutting
1. Touch the tool on the blank; zero the cross-slide and compound dials.
2. Back out, return to start, set the cross-slide back to zero.
3. Feed in on the **compound only**: 0.2–0.3 mm first passes, shrinking to 0.05 mm
   at the end. Cross-slide is only for retracting and returning to zero.
4. Engage the half-nuts on the right number on the thread dial (any line for even
   TPI on most dials; numbered lines for odd — check the dial chart on your machine).
5. At the end: **retract the cross-slide** and disengage the half-nuts in one
   coordinated motion. With half-nuts kept closed: retract, stop, reverse the spindle
   to the start.
6. Cutting oil on steel for every pass.
7. After the calculated depth, take 2–3 **spring passes** with no added infeed.

## 5. Gauging
- Try the mating nut or ring gauge with the work still in the chuck (don't remove
  it — you cannot pick up the thread again easily).
- For accuracy, measure pitch diameter with **three wires** or a **thread
  micrometer**; tables give the over-wire measurement for each pitch.
- Too tight: 0.02–0.05 mm more on the compound and another spring pass.

## Faults
- **Drunk / double thread:** wrong dial number or half-nut picked up wrong.
- **Torn flanks:** speed too high, tool not sharp, no cutting oil, or plunge-fed on
  the cross-slide instead of the compound.
- **Lean in the thread form:** tool not squared with the centre gauge.
- **Chatter:** too much stickout; support long work with the tailstock centre.

## Safety
Keep fingers away from the leadscrew and chuck; no gloves or loose sleeves near
rotating work. Plan the stop before you reach the shoulder — at low speed with the
hand on the half-nut lever. Remove the chuck key every time.

## Verify
- [ ] Blank diameter slightly under nominal, chamfered, relief cut.
- [ ] Gearbox set and checked by a scratch pass measured with a pitch gauge.
- [ ] Compound at 29.5°; tool on centre and squared.
- [ ] Mating nut or gauge runs on smoothly by hand, no rock.
- [ ] Thread surface finish clean with no tearing.

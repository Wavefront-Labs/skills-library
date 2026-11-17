---
id: creative-arts.film-live-action.cinema-cameras.focus-pulling-marks-and-depth-of-field
name: focus-pulling-marks-and-depth-of-field
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, camera-assistant, 1st-ac, first-ac, focus-puller, focus-pulling, pulling-focus, focus-marks, marks, tape-marks, wireless-follow-focus, follow-focus, focus-motor, hand-unit, wcu-4, hi-5, nucleus, teradek-rt, cine-tape, light-ranger, rangefinder, laser-measure, depth-of-field, hyperfocal, circle-of-confusion, dof-calculator, pcam, split-focus, rack-focus, focus-pull, witness-marks, lens-mapping, focus-scale, breathing, back-focus, flange-depth, collimation, monitor-focus, peaking, zoom-to-check, measuring-distance, tape-measure, laser-rangefinder, marking-the-lens, lens-marks, focus-ring-marks, dof-tables, dof-apps, pcam-use, focus-rehearsal, reading-actors, anticipating-moves, wireless-ff-setup, lens-calibration, motor-setup, rack-focus-technique, focus-transitions, back-focus-check, flange-check, collimation-check]
level: practitioner
status: draft
description: "Pull focus like a 1st AC: measure and mark, use depth-of-field and hyperfocal numbers to set strategy, wireless follow-focus hand units with lens mapping, racks and split focus, back-focus checks."
sources:
  - "American Cinematographer Manual, 10th ed. - Depth of field tables; Camera assistant chapters"
  - "https://www.arri.com/en/camera-systems/electronic-control-system (ARRI Hi-5/WCU-4 and lens data)"
  - "https://www.preston.ws/ (Preston FIZ systems)"
  - "David E. Elkins, The Camera Assistant's Manual"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Focus pulling, marks and depth of field

**Goal:** the eyes are sharp on every take at T1.4 on a 75 mm with the actor walking
toward camera - because the puller measured, marked, understood the depth they had,
and rehearsed the move.

## 1. Understand your depth of field
Depth of field depends on focal length, T-stop, focus distance and the **circle of
confusion** (CoC: ~0.025 mm for S35, ~0.03 mm for full frame - the acceptable blur).
Use a calculator (pCAM, Cadrage DoF, ARRI/RED online tools, or the ASC Manual tables):
- 50 mm, T2, 2 m on S35 -> roughly 1.9-2.1 m (about 20 cm total). At T5.6 -> ~1.7-2.4 m.
- Depth extends roughly 1/3 in front and 2/3 behind at normal distances; nearly equal
  at close focus. Longer lenses and wider apertures = thinner.
- **Hyperfocal distance** H = f² / (N x CoC): focus at H and everything from H/2 to
  infinity is acceptably sharp - the landscape/wide-shot setting (e.g. 18 mm at T8 on
  S35, H ≈ 1.6 m).
Know the depth before the take; it tells you whether to mark two points or follow continuously.

## 2. Measure and mark
- During blocking rehearsal, stand at the camera and measure from the **sensor plane
  mark (Φ)** on the camera body to the actor's eyes at each position: tape measure for
  statics, **laser** (Leica Disto/Bosch) for speed, a **Cine Tape / ultrasonic** or
  **Light Ranger 2 / Focusbug** rangefinder for continuous reads on moves.
- 2nd AC lays **tape marks** (T-marks or toe marks, colour per actor) at each position;
  note the distance per mark; mark the focus ring/hand unit at those distances (pre-marked
  rings/discs on the hand unit).
- Witness marks: objects in the frame at known distances (a chair at 2.4 m) to track
  an actor's position when the floor marks are out of frame or the actor misses them.
- Rehearse the move with the hand unit at the monitor: start distance, the cue
  (a step, a line), end distance. Decide **lead or lag**: on a walk-in, stay slightly
  ahead of the actor; on a rack, land the second subject exactly on the cue.

## 3. Hand units and lens mapping
Wireless FIZ (focus/iris/zoom): ARRI Hi-5 / WCU-4, Preston HU3/FIZ, Teradek RT, Tilta
Nucleus. Calibrate the motor to the lens end stops, then **map the lens** (ARRI LDS/
Cooke /i lenses map automatically; otherwise enter distances per ring position) so the
hand unit reads real distances and can show **depth-of-field overlays** on the monitor
(e.g. Hi-5 with Alexa). Pre-marked focus rings per lens save time; label them.
Iris on the hand unit lets the DP ride exposure on a move without touching the lens.

## 4. Technique
- **Eyes first.** If only one plane can be sharp, it's the nearest eye (or the one the
  audience is looking at).
- **Racks**: speed matches the story - quick for a reveal, slow for a drift; never
  overshoot and come back. Rehearse the rack to the cue on the monitor three times.
- **Split focus**: two subjects at different distances - find the point where both are
  within the depth (not the midpoint; depth is asymmetric), or ask the DP to stop down.
- **Monitor checks**: use peaking/zoom to confirm the first take, then pull by marks and
  eye; monitors lag and lie on fast moves.
- Keep a **focus log**: lens, stop, marks per setup - helps reshoots and shows the DP where
  depth was thin.

## 5. Back focus and lens checks
On zoom lenses and on any lens after a knock, check **back focus / flange depth**: a
Siemens star chart at a measured distance; the lens scale must agree with the tape.
Collimate or send to the rental house if it doesn't. Also check focus breathing on the
show's lenses so the operator can frame for it.

## Gotchas
- Measuring from the front of the lens instead of the sensor plane (half a metre out on a close-up).
- Trusting the lens scale on a zoom that's off back-focus.
- Marks laid for the master, actors "feeling it" differently in the close-up; re-measure every size.
- Pulling off the monitor only - wireless video latency puts you a step behind.
- No one checking the first take at 100% zoom; soft takes discovered in dailies.

## Verify
- [ ] Depth of field known per setup; strategy (marks vs continuous) chosen.
- [ ] Distances measured from Φ to eyes for every mark; focus ring/hand unit marked.
- [ ] Rack cues rehearsed; first take checked at zoom.
- [ ] Back focus verified on every zoom and after any lens knock.

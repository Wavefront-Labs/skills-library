---
id: repair-maintenance.aircraft-maintenance.propeller-rotor-maintenance.blade-dressing-and-dynamic-balancing
name: blade-dressing-and-dynamic-balancing
category: repair-maintenance
field: aircraft-maintenance
product: propeller-rotor-maintenance
tags: [aircraft-maintenance, propeller-rotor-maintenance, propeller, blade-dressing, nick-removal, file, emery, dye-penetrant, dynamic-balancing, prop-balancing, ips, accelerometer, photo-tach, balance-weights, rotor-track-and-balance, helicopter, blade-track, sensenich, mccauley, hartzell, ac-20-37]
level: practitioner
status: draft
description: "Dress nicks out of aluminium propeller blades within manufacturer limits and dynamically balance the propeller with an accelerometer and photo-tach; notes on helicopter rotor track and balance."
sources: ["FAA AC 20-37E Aircraft Propeller Maintenance", "Hartzell Manual 133C / McCauley owner's service manuals (method structure only)", "FAA-H-8083-32 Powerplant Handbook, ch. 7 Propellers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blade dressing and dynamic balancing

**Goal:** remove stress-raising nicks from metal propeller blades without exceeding
material-removal limits, then reduce vibration to the manufacturer's target with a
dynamic balance. Dressing limits (how deep, how near the tip, how wide) are specific to
each blade model — get them from the propeller manufacturer's manual or AC 20-37 where
the manufacturer permits. Major repairs (straightening bent blades, re-pitching) belong
to a certificated propeller repair station.

## 1. Blade dressing (aluminium blades)
**Why:** a nick on the leading edge is a fatigue crack starter; blades have failed in
flight from untreated nicks.
1. Clean the blade; inspect both faces and edges under good light, with a 10× glass at
   each nick. Note distance from the tip and depth.
2. Check against the limits: typical leading-edge dressing is allowed only to a
   modest depth (often ≤ 1/8 in on the edges, less on the face), and **must not change
   the airfoil contour**. Anything bigger, or in the shank/hub area → repair station.
3. Dress with a fine file (half-round or riffler), working *along the blade span*, not
   across, until the nick is gone. Then blend a smooth, shallow depression whose
   length is ~10× its depth (a long, shallow scoop, not a notch). 
4. Finish with progressively finer abrasive (e.g. 180 → 320 → 600 grit emery cloth),
   polishing lengthwise until no cross scratches remain.
5. **Dye-penetrant inspect** the dressed area to confirm no crack remains below the surface.
6. Treat bare metal: chemical conversion coating (Alodine) then primer and paint matching
   the original — including the tip stripes (they're a safety visibility marking).
7. Large removals affect static balance; repeated dressing over time also shortens
   blade life — log each one.

## 2. Dynamic balancing (fixed-pitch or constant-speed props)
**Kit:** balancer (e.g. ACES ProBalancer, DSS Microvib-type) with velocimeter/accelerometer,
optical photo-tach and reflective tape, approved balance weights, hardware per the
propeller/spinner manufacturer.
1. Mount the accelerometer on the engine as close as possible to the propeller plane,
   vertically or radially, on a rigid bracket (crankcase or starter flange bolt).
2. Mount the photo-tach on a bracket aimed at reflective tape on one blade (blade #1);
   the tape is the phase reference.
3. Run at the balancing rpm (commonly a high cruise rpm on the ground, into wind,
   cowling installed). Record vibration in **IPS** (inches per second) and phase angle.
4. Typical targets: ≤ 0.2 IPS acceptable, ≤ 0.07–0.1 IPS good — confirm manufacturer target.
5. Add a **trial weight** at a known location (manufacturer-approved hole in the spinner
   bulkhead/starter ring), re-run, and let the balancer compute the solution weight and
   angle. Split weights between two holes if needed.
6. Install permanent weights with the approved AN/NAS hardware, locknuts, torque, and do
   not exceed the maximum weight per location (e.g. a stated grams/oz limit).
7. Final run to confirm; record readings, weights and positions.

## 3. Helicopter rotor track and balance (overview)
Same principle with a tracker (optical or strobe) per main rotor blade: adjust pitch
links to bring blades into track, trim tabs for in-flight track, and hub weights for
lateral balance — strictly per the RFM/maintenance manual's charts and in the
sequence ground → hover → forward flight. Never adjust more than one parameter per run.

## Gotchas
- Balancing hides, it does not fix: a damaged blade or loose spinner shows as
  imbalance — inspect first.
- Weights on the spinner alone can crack it; use the bulkhead locations the manual allows.
- Uncertain: dressing limits and IPS targets quoted are typical values; your blade/prop
  model may be stricter.

## Verify
- [ ] Each nick dressed within the manufacturer's depth/location limits, blended ~10:1.
- [ ] Dressed areas dye-penetrant clean and re-protected; tip stripes intact.
- [ ] Final vibration below manufacturer target in IPS; weights within per-location max.
- [ ] Hardware safetied/locknutted and torqued; spinner refitted without cracks.
- [ ] Logbook records dressing locations and balance readings/weights.

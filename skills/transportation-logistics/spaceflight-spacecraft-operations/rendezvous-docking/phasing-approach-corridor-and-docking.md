---
id: transportation-logistics.spaceflight-spacecraft-operations.rendezvous-docking.phasing-approach-corridor-and-docking
name: phasing-approach-corridor-and-docking
category: transportation-logistics
field: spaceflight-spacecraft-operations
product: rendezvous-docking
tags: [rendezvous, docking, berthing, proximity-operations, rpo, phasing, hohmann, cw-equations, hill-equations, lvlh, v-bar, r-bar, approach-ellipsoid, keep-out-sphere, approach-corridor, hold-points, manual-docking, torus, iss, canadarm2, robotic-capture, closing-rate, lidar]
level: advanced
status: draft
description: "Planning phasing burns, flying the approach corridor in LVLH (V-bar/R-bar), respecting keep-out zones and hold points, and the closing-rate and alignment limits for docking or arm capture."
sources: ["Fehse, Automated Rendezvous and Docking of Spacecraft (Cambridge, 2003)", "Curtis, Orbital Mechanics for Engineering Students, ch. 7 (relative motion)", "NASA ISS visiting vehicle public mission documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Phasing, approach corridor and docking

**Goal:** bring a chaser to a target safely: catch up in phase, close in through
defined gates, and contact within alignment and closing-rate limits — or abort to a
safe, passively drifting trajectory.

## 1. Frame and intuition (LVLH / Hill frame)
Centre on the target: **V-bar** along its velocity, **R-bar** towards Earth's centre
(or radially, by convention), H-bar out of plane. Relative motion follows the
Clohessy-Wiltshire (Hill) equations for near-circular orbits. Counter-intuitive rules:
- Thrusting **forward** (+V-bar) raises your orbit and you **drift backwards**.
- Being **lower** than the target makes you drift ahead; higher, behind.
- A radial impulse produces a closed ellipse — useful for safe fly-arounds.

## 2. Phasing (far range, hundreds to thousands of km)
1. Compute phase angle to the target; choose a lower (catch-up) orbit. Phase gained
   per orbit ≈ 3π·Δa/a radians (e.g. 20 km lower at ~6,780 km ≈ 0.53° per orbit);
   use the flight-dynamics tool for the real plan, this only for sanity checks.
2. Plan a sequence of height-adjust and coelliptic burns so you arrive at the
   **initial aim point** (several km behind or below the target) at a planned time,
   often with lighting and ground-station coverage constraints.
3. Each burn: compute, screen against the catalogue, execute, update relative
   navigation, retarget.

## 3. Close range: corridors, gates and keep-out zones
Typical ISS-style geometry (*values vary by programme*):
- **Approach ellipsoid** (~4 × 2 × 2 km around the station) — entry requires a Go
  from the target's control centre.
- **Keep-out sphere** (~200 m radius) — entry only along the approach corridor after
  a second Go.
- **Hold points** (e.g. 250 m, 30 m, 20 m) where the vehicle stops and waits for Go.
- **Approach corridor**: a cone (often ~10–15° half-angle) around the docking axis;
  leaving it triggers a retreat or abort.
Approaches are along **V-bar** (stable station-keeping in front/behind, natural for
docking ports facing forward) or **R-bar** (from below; orbital mechanics provides
natural braking, used for many arm-capture approaches).

## 4. Final approach and contact
- Closing rate decreases with range; final contact rates are typically a few cm/s
  (roughly 0.05–0.15 m/s for androgynous docking systems; near-zero relative motion
  for arm capture at the capture point).
- Lateral misalignment and angular-rate limits must be met simultaneously — know the
  docking system's capture envelope.
- Relative sensors: lidar, cameras with targets, and GNSS relative nav further out.
- **Manual docking**: fly the target cross-hair with small, separated pulses: translate
  to fix position, then let rates damp. Never correct attitude and translation at the
  same time on a jittery picture.
- **Arm capture**: chaser enters free drift at the capture box; operator grapples the
  fixture within the allowable drift time.

## 5. Abort
Every phase needs a pre-computed abort burn that results in a **passively safe**
trajectory (one that won't intersect the target for at least ~24 h with thrusters
off). Trigger it on corridor violation, sensor loss or loss of Go.

## Gotchas
- Plume impingement on the target's solar arrays/radiators — thruster use near the
  station is constrained.
- Lighting: sun in the camera at the wrong moment blinds sensors; plan arrival times.
- Comms handovers at hold points; never move past a hold point without voice/data link.

## Verify
- [ ] Each phase has a passive-safety check and a precomputed abort burn.
- [ ] Hold points, corridor angle and Go authorities are on the timeline.
- [ ] Contact closing rate, misalignment and angular rates fall inside the docking envelope in simulation.
- [ ] Lighting and comms coverage confirmed for final approach.

---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.frontal-crush-zone-energy-management
name: frontal-crush-zone-energy-management
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [crash-safety, crashworthiness, frontal-crash, crush-zone, crumple-zone, energy-absorption, crash-pulse, front-rail, crash-box, load-path, mean-crush-force, ride-down, restraint-system, airbag, seatbelt, olc, occupant-load-criterion, euro-ncap, mpdb, us-ncap, iihs, small-overlap, fmvss, fmvss-208, fmvss-305, unece-r94, unece-r137, hic, thor, hybrid-iii, ls-dyna, pam-crash, radioss, crash-cae, ev-crash, battery-protection, crash-test-protocols]
level: practitioner
status: gated
description: "Size a frontal crush zone from crash energy, target pulse and occupant deceleration, staging load paths and checking against current NCAP/FMVSS load cases."
sources:
  - "Huang, Vehicle Crash Mechanics (CRC)"
  - "Euro NCAP, IIHS and NHTSA published test protocols (check the current versions)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Frontal crush zone: energy, pulse and load paths

**Goal:** give the front structure enough crush length and the right force levels that
the vehicle absorbs the crash energy with a pulse the restraints can ride down, without
intrusion into the occupant (and battery) space.

Test speeds, overlaps and OLC geometry named below (UN R94/R137, Euro NCAP MPDB, RCAR) were not checked against the primary protocols (gated: unconfirmed, source is paywalled or blocked); IIHS small overlap 64.4 km/h and 25% were fetched, and 49 CFR 571.208 allows speeds up to 56 km/h.

**Protocols change frequently.** Test speeds, overlaps, dummies, barrier specs and
scoring limits below are orientation values; always design to the current published
version of each protocol (Euro NCAP, IIHS, US NCAP, FMVSS/UN regulations) for the target
market and model year. Euro NCAP, for instance, restructured its rating from 2026.

## 1. List the load cases that size the front end
Typical set (verify each): full-width rigid barrier ~50–56 km/h (FMVSS 208 / US NCAP at
35 mph, UN R137, Euro NCAP full width), offset deformable barrier (UN R94; IIHS moderate
overlap 64 km/h), Euro NCAP MPDB (50 km/h into a 50 km/h moving trolley, 50% overlap),
IIHS small overlap 25% at 64 km/h, plus low-speed repairability (RCAR ~15 km/h) and
pedestrian requirements. Full-width cases drive pulse severity; offset cases drive
structural intrusion and one-sided load paths; small overlap bypasses the rails entirely.

## 2. Energy and average deceleration
```
E = ½ · m · v²            a_avg = v² / (2 · d_dyn)          F_mean = E / d_dyn
```
Example (computed with python): 1600 kg at 56 km/h (15.56 m/s) → E ≈ 194 kJ. With 600 mm of dynamic crush:
a_avg ≈ 15.56² / 1.2 ≈ 202 m/s² ≈ **20.6 g**, F_mean ≈ **323 kN** shared across load
paths. A real pulse is never a square wave; peaks of 1.5–2× average are common.
Heavier EVs raise E at the same speed, and rigid packaging (motor, inverter, pack) eats
crush length.

## 3. Crush length budget ("stack-up")
Lay out the front in section view and add up genuinely crushable length: bumper beam and
crash boxes, rail length that can fold axially, then the gaps between rigid parts (motor
or engine block, compressor, radiator pack) and the dash. Rigid components "stack" and
transmit force straight to the firewall. A common failure is a pulse spike when the
powertrain hits the dash crossmember — create space or shear-off/guide mechanisms.

## 4. Occupant side: ride-down
The occupant needs crush + restraint stroke to stop. The theoretical minimum occupant
deceleration with ~300 mm of restraint travel is v²/(2·(d_dyn + d_restraint)) ≈ 13.7 g
for the example — real chest deceleration is far higher because coupling is never
perfect. Restraints (pretensioners, load limiters, airbag venting) are tuned *to the pulse*;
a change in pulse shape late in the programme forces re-tuning. Euro NCAP's MPDB uses the
**OLC** (occupant load criterion: virtual occupant free-flies 65 mm then decelerates
uniformly over 235 mm) computed from the trolley pulse to penalise aggressive structures —
check the current penalty thresholds.

## 5. Stage the load paths
1. **Crash boxes:** low force, sacrificial, protect rails in low-speed impacts.
2. **Front rails (main path):** axial progressive folding; design mean crush force per
   rail and keep peak-to-mean low with triggers (beads, holes, thickness steps).
3. **Upper load path** (shotgun / upper rail) and **subframe** path: share load, help
   offset and small-overlap cases, and spread force into the A-pillar and sill.
4. **Passenger cell:** stiff, near-zero deformation; footwell, dash and pillar intrusion
   are scored directly. For EVs, the pack must see no intrusion or penetration; HV must be
   isolated post-crash (pyro-fuse/contactors; FMVSS 305, UN R94/R137 electrical
   requirements).
For thin-walled square tubes the classic folding theory (Wierzbicki–Abramowicz) gives
mean crush force roughly ∝ σ0 · t^(5/3) · b^(1/3) (σ0 flow stress, t wall, b side) —
wall thickness is the strongest knob, material grade next, section size weakest. Use it
for trends; calibrate absolute values on drop-tower tests.

## 6. CAE discipline
LS-DYNA, Pam-Crash or Radioss. Check energy balance every run: hourglass energy below
~5–10% of internal, total energy conserved, added mass from mass scaling small (a few
percent) and not in the crush zone. Correlate sub-systems (rail drop tower, sled) before
trusting the full vehicle. Run ±5% material and thickness scatter on critical parts.

## Verify
- [ ] Load-case list and protocol versions confirmed for every target market.
- [ ] Energy, average deceleration and mean force computed; crush length budget shows
      enough truly crushable length after stack-up.
- [ ] Pulse shape agreed with the restraint team; OLC or equivalent checked.
- [ ] Each load path has a mean-force target and folding trigger design.
- [ ] Intrusion targets for footwell, dash, pillar (and battery) met in CAE with scatter.
- [ ] CAE energy balance and hourglass checks pass; sub-system correlation done.

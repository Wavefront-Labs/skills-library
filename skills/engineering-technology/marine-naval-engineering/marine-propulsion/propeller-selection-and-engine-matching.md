---
id: engineering-technology.marine-naval-engineering.marine-propulsion.propeller-selection-and-engine-matching
name: propeller-selection-and-engine-matching
category: engineering-technology
field: marine-naval-engineering
product: marine-propulsion
tags: [marine-propulsion, propeller-design, fixed-pitch-propeller, wageningen-b-series, b-series, kt-kq, open-water-efficiency, advance-coefficient, bp-delta, keller-criterion, burrill, cavitation, blade-area-ratio, engine-matching, light-running-margin, propeller-curve, layout-diagram, two-stroke-diesel, sea-margin, wake-fraction, thrust-deduction]
level: advanced
status: gated
description: "Select a fixed-pitch propeller from Wageningen B-series (optimum D or rpm, Keller blade area) and match it to a diesel with light-running and sea margins."
sources:
  - "Oosterveld & van Oossanen, Further computer-analyzed data of the Wageningen B-screw series (1975)"
  - "Carlton, Marine Propellers and Propulsion (Butterworth-Heinemann)"
  - "Engine maker propulsion-plant guides (e.g. MAN Energy Solutions 'Basic principles of ship propulsion')"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Propeller selection and engine matching (fixed-pitch, B-series)

**Goal:** choose diameter, pitch, blade number and blade area for a fixed-pitch
propeller that delivers the required thrust efficiently without harmful cavitation,
and match it to an engine so it never runs into the torque limit as the hull ages.

## 1. Inputs
- Resistance at service speed (from
  engineering-technology.marine-naval-engineering.naval-architecture.resistance-and-powering-estimate),
  wake fraction w, thrust deduction t.
- Advance speed VA = V (1 - w); required thrust T = R / (1 - t).
- Constraint on diameter: aft clearance and draft (single-screw D is often about
  0.65-0.75 of design draft (gated: unconfirmed, source is paywalled or blocked); hull clearances per class guidance, check yours).
- Engine type: low-speed two-stroke direct drive (rpm fixed by engine) or geared
  medium-speed (rpm chosen via gear ratio).

## 2. Choose the optimum
Non-dimensionals: J = VA / (nD), KT = T / (rho n^2 D^4), KQ = Q / (rho n^2 D^5),
eta0 = (J / 2 pi) (KT / KQ).

1. **Pick blade number Z**: 4 is the default for single-screw merchant ships;
   5-6 reduce vibration excitation ((gated: unconfirmed, source is paywalled or blocked)); avoid Z matching hull/engine excitation orders.
2. **Blade area from cavitation (Keller):**
   AE/A0 = (1.3 + 0.3 Z) T / ((p0 - pv) D^2) + k,
   p0 = p_atm + rho g h (h = shaft centreline submergence), pv about 1.7 kPa at 15 C (Magnus approximation computes 1.70 kPa),
   k = 0 to 0.1 for twin screw, up to 0.2 for single screw (Keller constants (gated: unconfirmed, source is paywalled or blocked)). Cross-check with Burrill.
3. **Optimum diameter at fixed rpm** (direct drive): the thrust identity gives
   KT / J^4 = T n^2 / (rho VA^4). Plot this curve on the KT-J chart of each P/D;
   pick the J that maximises eta0. D = VA / (nJ).
4. **Optimum rpm at fixed D** (geared or diameter-limited): KT / J^2 = T / (rho D^2 VA^2).
5. Use the polynomial KT/KQ fits, a Bp-delta chart, or a design tool; behind the
   ship multiply by etaR. Reduce the open-water optimum diameter by roughly 3-5 %
   for single-screw wake (a common rule of thumb, (gated: unconfirmed, source is paywalled or blocked); check with your design method).

## 3. Match the engine
1. Propeller law: P proportional to n^3 for a given hull state.
2. Design the propeller on the **heavy** curve (fouled hull, sea margin) and add a
   **light-running margin** of about 4-7 % rpm (engine makers recommend values in
   this region; up to about 10 % for ships with large power-speed variation) ((gated: unconfirmed, source is paywalled or blocked); confirm in the maker's propulsion guide).
   On a clean hull in calm water it then runs lighter (higher rpm for the same power).
3. Plot the service point at about 85-90 % of the selected MCR ((gated: unconfirmed, source is paywalled or blocked)) and confirm it is
   inside the engine's layout diagram and clear of the torque/overload limit.
4. Check barred-speed ranges from torsional vibration analysis are passed quickly.

## Worked mini-example (cavitation check)
R = 300 kN, t = 0.18: T = 366 kN. D = 5.0 m, h = 4.0 m, Z = 4, single screw (k = 0.2).
- (Recomputed: T 365.9 kN, p0 - pv 139,845 Pa, AE/A0 0.262 + 0.2 = 0.46; thrust-identity algebra for KT/J^4 and KT/J^2 re-derived.)
- p0 - pv = 101 325 + 1025 x 9.81 x 4.0 - 1 700 = about 139 800 Pa.
- AE/A0 = 2.5 x 366 000 / (139 800 x 25) + 0.2 = 0.262 + 0.2 = 0.46.
Choose B4-55 (0.55), not B4-40. Then iterate D and P/D for eta0 at that area.

## Gotchas
- A propeller matched to trial conditions runs heavy in service and cannot reach MCR
  rpm: overloaded, smoky, hot engine. Always keep the light-running margin.
- Larger diameter raises eta0 but also hull-pressure pulses; keep tip clearance.
- B-series data are open-water and model-scale; scale effects on KQ are small but real.
- Slow-steaming ships may justify a re-optimised propeller; redo the match, do not
  just derate.

## Verify
- [ ] VA and T use the same w and t as the powering estimate.
- [ ] AE/A0 from Keller (and Burrill) is no greater than the chosen series area.
- [ ] D fits the aperture with class-recommended clearances.
- [ ] Light-running margin 4-7 % (or justified) between design and heavy curves.
- [ ] Service point at 85-90 % MCR, inside the layout diagram.

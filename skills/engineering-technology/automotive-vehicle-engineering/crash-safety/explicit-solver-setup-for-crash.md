---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.explicit-solver-setup-for-crash
name: explicit-solver-setup-for-crash
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [explicit-solver, ls-dyna, radioss, pam-crash, abaqus-explicit, contact-definition, initial-conditions, termination-time, double-precision, crash-cae, solver-setup]
level: practitioner
status: gated
description: "Set up an explicit crash run: units, initial velocity, contacts, gravity preload, time step control, precision, output intervals, and checks of the first run."
sources:
  - "LS-DYNA user manual contents (keyword manual volumes I-III; vendor documentation at https://www.ansys.com)"
  - "Huang, Vehicle Crash Mechanics (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Explicit solver setup for crash

Friction values, time-step scale factor and termination times are practice values (gated: unconfirmed, source is paywalled or blocked).

## 1. Run basics
Explicit dynamics integrates equations with small time steps without matrix inversion; crash solvers include LS-DYNA, Altair Radioss, ESI PAM-CRASH, and Abaqus/Explicit. The set-up concepts transfer across them; the keywords below are LS-DYNA style.

## 2. Model assembly
- **Units:** one consistent system (for example mm, tonne, s, N, MPa); wrong units are a top cause of nonsense.
- **Initial conditions:** initial velocity on the vehicle (for example barrier test speed), not on the barrier unless stated; set wheel rotation to match speed for friction.
- **Gravity** and suspension preload: run a settling stage (dynamic relaxation or a pre-simulation) so suspension and tyres start in equilibrium; otherwise the vehicle jumps at t = 0.
- **Barrier or occupant models:** use validated barrier models (for example offset deformable barrier or MDB models from the standard) rather than invented.

## 3. Contacts
Prefer one automatic single-surface contact including all parts of the vehicle for self-contact, plus specific contacts for barrier and road. Set friction coefficients (steel on steel typically around 0.1-0.2 in crash practice; check your standard), contact thickness offsets, and soft constraint options for dissimilar stiffness. Search for initial penetrations and remove them.

## 4. Time step control
Use the automatic time step based on the element Courant limit with a scale factor below 1 (around 0.9 for shells in practice), minimum time-step termination to catch collapsing elements, and a documented mass scaling policy (see mesh checks).

## 5. Precision and parallelism
Single precision is common and fast; use double precision for models sensitive to round-off (long runs, small stiffness differences). Domain-decomposition parallel runs may give slightly different results; confirm the repeatability level.

## 6. Output and termination
Termination time is long enough to cover the event (about 100-150 ms for frontal rigid-barrier tests; side impact shorter; plus rebound for restraint timing). Write output at fine intervals for sensor channels (for example 0.1 ms for accelerations), coarse for full-state animations. Request energy, contact and force database outputs for post-check.

## 7. First-run checks
Energy balance, hourglass energy, mass added, no unexpected contacts, check the animation for part flying off, and check that velocities equal the specified initial conditions.

## Verify
- [ ] Units, initial velocity, preload and barrier model confirmed.
- [ ] Contacts defined; no initial penetrations.
- [ ] Time-step and mass scaling logged.
- [ ] Energy and output channels checked on a short test run.

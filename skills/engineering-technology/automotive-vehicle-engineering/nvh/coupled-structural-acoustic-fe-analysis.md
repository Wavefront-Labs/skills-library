---
id: engineering-technology.automotive-vehicle-engineering.nvh.coupled-structural-acoustic-fe-analysis
name: coupled-structural-acoustic-fe-analysis
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [acoustic-fea, vibro-acoustic-fea, ntf, noise-transfer-function, cavity-modes, coupled-fe, nastran-sol-108, modal-frequency-response, acoustic-mesh, nvh-cae, impedance-boundary]
level: practitioner
status: gated
description: "Run coupled structure-cavity FE for cabin noise: cavity mesh, coupling, mesh rule for wavelength, NTF set-up, absorption boundaries and correlation with measured NTF."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "FE acoustic analysis references and solver documentation (frequency response, modal and direct methods)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Coupled structural-acoustic FE analysis

## 1. Purpose
Predict noise transfer functions (NTFs, sound pressure at the ear per unit force at a body attachment, in Pa/N or dB) for the low and low-mid frequency range (about 20-300 Hz), where structure and cabin cavity modes both matter, and design to avoid booming.

## 2. Model
- **Structure:** trimmed body FE model (see body modal FEA) with mass of seats, interior, powertrain, fuel, glazing and windows as shells, door and closure attachments, correct damping.
- **Cavity:** a solid mesh of the passenger compartment (and trunk if it matters) with acoustic fluid elements having pressure as DOF; include seats as porous or impedance volumes or as acoustic absorption on their surfaces.
- **Coupling:** coupled interface at the cabin skin so structure velocity drives the fluid and fluid pressure loads the structure.
Mesh rule: use at least about six linear elements per wavelength at the highest frequency of interest (wavelength in air is 1.7 m at 200 Hz with c = 343 m/s, so elements of about 0.29 m; cabin cavities are coarse relative to body shells); structure mesh already finer.

## 3. Analysis types
Modal frequency response (fast; extract structure and cavity modes then superpose) or direct frequency response (accurate with frequency-dependent damping); in Nastran-style solvers these are the modal and direct frequency response solutions (check the solution sequence numbers in your solver version's manual). Apply unit forces at the mount points (or road inputs at subframe attachments) in three directions and request pressure at driver and passenger ear points.

## 4. Absorption and damping
Define acoustic damping through impedance boundaries or absorption coefficients for headliner, carpet and seats, and structural damping (modal damping values or frequency-dependent loss factors measured by tests). Cabin cavity damping strongly influences peak heights. The first cavity modes of a passenger car are typically in the range of a few tens of hertz (gated: unconfirmed, source is paywalled or blocked). A rigid-wall estimate for the first longitudinal mode is f = c/(2L), which gives 57-69 Hz for L = 3.0-2.5 m; real cabins differ (trunk coupling, wall compliance, seats), so take the value from the model and a measurement.

## 5. Interpreting results
Compare NTF vs frequency with the target (see NVH target cascade); identify peaks and find whether the cause is a structural mode, cavity mode or coupling; use panel participation (see panel contribution) to find the panels responsible; then change stiffness, mass, damping or trim.

## 6. Correlation
Measure NTFs on the vehicle with an instrumented hammer or shaker at mounts and microphones at ears; compare; update damping, boundary conditions and mass; accept within a stated dB band for the frequency range (the band is a programme choice (gated: unconfirmed, source is paywalled or blocked)).

## Verify
- [ ] Cavity mesh rule satisfied at the top frequency.
- [ ] Damping and absorption defined from measurements.
- [ ] NTF compared with measured NTF.
- [ ] Peaks traced to structure, cavity or coupling mechanisms.

---
id: engineering-technology.biomedical-engineering.biomechanics.segment-inertial-parameters
name: segment-inertial-parameters
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [segment-inertia, inverse-dynamics, joint-moments, anthropometric-tables, dempster, winter-table, de-leva, radius-of-gyration]
level: practitioner
status: gated
description: "Estimate segment mass, centre of mass and moments of inertia for inverse dynamics from anthropometric tables, regression and scanning, with error propagation."
sources: ["Winter, Biomechanics and Motor Control of Human Movement (anthropometry chapter; values from Dempster)", "de Leva, Adjustments to Zatsiorsky-Seluyanov's segment inertia parameters (J Biomech 1996)", "Pearsall and Costigan, The effect of segment parameter error on gait analysis results (Gait Posture 1999)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Segment inertial parameters

**Goal:** the mass, centre of mass (COM) location and moment of inertia of each body segment, needed for inverse dynamics.

## Table-based approach
For segment mass m_seg = fraction x total body mass; COM at a fraction of segment length from the proximal end; moment of inertia about the COM I = m (rho L)^2 with radius of gyration rho as a fraction of length.

Commonly quoted values from Winter (derived from Dempster; textbook source, not checked against a free primary source (gated: unconfirmed, source is paywalled or blocked)):
- Thigh: mass 0.100, COM 0.433 from the proximal end, radius of gyration 0.323.
- Shank (leg): 0.0465, 0.433, 0.302.
- Foot: 0.0145, 0.50, 0.475 (foot length axis differs).
- Upper arm 0.028, forearm 0.016, hand 0.006, trunk about 0.497, head and neck about 0.081.

Alternatives: **de Leva** (sex-specific adjustment of Zatsiorsky-Seluyanov values using joint centres), regression equations from DXA or imaging, subject-specific geometric models, or 3D body scans.

## Steps
1. Measure total mass and segment lengths between joint centres consistent with the table's definitions (landmark definitions differ between tables).
2. Compute per segment m, COM position vector, and I about the COM (full tensor or about the mediolateral axis for planar analysis).
3. For amputees or children use adjusted models (prosthesis weights measured directly; paediatric tables).
4. Document the source table.

## Error and sensitivity
- Errors in segment parameters affect joint moments mostly in swing and at proximal joints; moments in stance are dominated by GRF and kinematics, so errors matter less there (published sensitivity studies).
- Large body-mass differences (obesity) deviate from tables; soft tissue distribution matters.

## Verify
- [ ] Segment masses sum to the measured total mass.
- [ ] COM positions lie within segment geometry.
- [ ] Sensitivity run with plus or minus 10% mass and inertia changes.

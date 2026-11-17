---
id: engineering-technology.biomedical-engineering.biomechanics.ground-reaction-force-processing
name: ground-reaction-force-processing
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [ground-reaction-force, inverse-dynamics, joint-moments, force-plate, centre-of-pressure, free-moment, gait-events, plate-offset]
level: practitioner
status: gated
description: "Process force plate data: calibration check, coordinate frames, centre of pressure and free moment, event detection thresholds, zeroing drift and common errors."
sources: ["Winter, Biomechanics and Motor Control of Human Movement", "Kistler, AMTI and Bertec force platform manuals (use your plate's manual for sign conventions and offsets)", "Vaughan, Davis and O'Connor, Dynamics of Human Gait"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ground reaction force (GRF) processing

**Goal:** accurate 3D force, centre of pressure (COP) and free moment in the lab frame for inverse dynamics.

## Steps
1. **Zero the plate** (unloaded offsets) before each session; check drift during long sessions.
2. **Sensitivity check:** a known weight (or a subject standing still) should return the weight in Fz within 1-2% (gated: unconfirmed, source is paywalled or blocked).
3. **COP from forces and moments:** for a plate with the origin below the surface by z0 (use the manufacturer's definition):
   - COPx = (-My - Fx z0) / Fz and COPy = (Mx - Fy z0) / Fz, with z0 the positive depth of the plate origin below the surface (re-derived from M = r x F for a point load and recovered numerically; sign conventions and axes differ between brands, so verify with a point load test).
4. **Free moment** about the vertical axis: Tz = Mz - (COPx Fy - COPy Fx), sign by convention. It is small but affects hip rotation moments.
5. **Transform** forces and COP to the global lab frame using the plate's corner positions (measured or from calibration).
6. **Event detection:** foot contact and toe-off when vertical force passes a threshold (typically 10-20 N, above plate noise but below early-contact forces (gated: unconfirmed, source is paywalled or blocked)); use consistent thresholds.
7. **Filter** as the kinematics (see butterworth-data-filtering) and handle COP at low force (noise dominates when Fz is small): set COP to NaN below a force threshold or interpolate.
8. **Alignment:** check synchronisation between marker and plate systems; a time offset of several milliseconds changes impact moments.

## Common errors
- Using a wrong plate origin or z0, which shifts COP by several millimetres.
- A foot touching two plates (cross-over) giving wrong force assignment; check with force and marker data.
- Plates with different mounting and crosstalk.
- Wearing shoes versus bare feet changing COP interpretation.

## Verify
- [ ] Known-weight and load-point tests passed.
- [ ] COP trajectory stays under the foot's marker footprint.
- [ ] For steady walking, the vertical impulse summed over all plates for one full stride equals body weight x stride time (mean vertical force over a stride equals body weight); a mismatch of more than a few percent indicates drift, scaling or event errors.

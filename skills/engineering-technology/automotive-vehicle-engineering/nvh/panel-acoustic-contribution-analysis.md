---
id: engineering-technology.automotive-vehicle-engineering.nvh.panel-acoustic-contribution-analysis
name: panel-acoustic-contribution-analysis
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [panel-contribution, panel-acoustic-contribution, acoustic-transfer-vector, atv, reciprocity, laser-vibrometer, acoustic-intensity, body-acoustics, panel-ranking, vibro-acoustic]
level: practitioner
status: verified
description: "Rank which body panels drive interior noise: acoustic transfer vector with reciprocity, panel velocity scanning, contribution ranking and the damping or stiffening fix."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "Vibro-acoustic engineering references for panel contribution and acoustic transfer vectors"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Panel acoustic contribution analysis

## 1. Question answered
At a given frequency and operating condition, which panels radiate most to the occupant's ear? The answer directs damping, stiffening or insulation to the panels that matter.

## 2. Method
Contribution of panel k to the pressure at the ear: p_k = sum over the panel's surface of ATV(x) x v_n(x) x dA, where ATV is the acoustic transfer vector (pressure at the ear per unit normal panel velocity) and v_n is the measured or computed panel surface normal velocity.

- **ATV via reciprocity:** put a volume-velocity source (for example a calibrated loudspeaker or a compact source) at the ear position and measure sound pressure at points near the panel surfaces; by reciprocity, this gives the ATV. This is much faster than exciting each panel.
- **Panel velocity:** measure operational velocity with scanning laser vibrometry, accelerometer grids, or from FE or multibody simulation under the same excitation (road, engine order).
Sum complex contributions (phase matters; contributions can cancel).

## 3. Process
1. Choose the operating case (for example 3rd engine order at 2500 rpm, or road noise at a boom frequency).
2. Build the panel grid (the spacing must be below half the structural bending wavelength; computed for 0.8 mm steel, 50 mm spacing is adequate only up to about 790 Hz and 100 mm up to about 200 Hz, so size the grid from the highest frequency of interest).
3. Measure or compute v_n and ATV; compute contribution spectra per panel.
4. Rank panels by contribution to total SPL at the problem frequency; show both magnitude and phase to identify cancelling groups.
5. Act: add damping, stiffening beads, local mass or absorption to the top contributors; re-measure.

## 4. Alternatives
Acoustic intensity scanning of the interior surface; beamforming inside the cabin; FE-based panel participation factors; hybrid with TPA to link to the structure-borne paths (see classical TPA).

## 5. Pitfalls
Not measuring velocity in the same condition as the noise; spatial aliasing from a coarse grid; ignoring the contribution from openings (leaks, vents); low-frequency cavity modes making ATV vary strongly with ear position, so check seat positions.

## Verify
- [ ] ATV and velocity captured in the same configuration.
- [ ] Grid spacing fine enough for the frequency band.
- [ ] Contributions summed with phase; ranking presented per frequency.
- [ ] Fix validated by remeasurement.

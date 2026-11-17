---
id: natural-sciences.oceanography.ocean-observation.ctd-cast-operations-and-processing
name: ctd-cast-operations-and-processing
category: natural-sciences
field: oceanography
product: ocean-observation
tags: [ocean-observation, ctd, ctd-cast, rosette, niskin-bottles, seabird, sbe-911, seasave, sbe-data-processing, seasoft, conductivity-cell, sensor-lag, align-ctd, cell-thermal-mass, loop-edit, bin-average, salinometer, autosal, iapso-standard-seawater, dissolved-oxygen, winkler, sensor-calibration, soak, go-ship, argo-qc]
level: practitioner
status: gated
description: "Run a CTD/rosette cast and process it to publication quality: pre-cast checks, soak, descent rate, bottle firing, Sea-Bird processing chain (align, thermal mass, loop edit) and bottle calibration."
sources: ["GO-SHIP Repeat Hydrography Manual (IOCCP Report 14)", "Sea-Bird Scientific SBE Data Processing manual and application notes", "Kawano, salinity measurement with salinometer (GO-SHIP manual chapter)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CTD cast operations and processing

**Goal:** a clean downcast profile of temperature, salinity, oxygen and other sensors,
calibrated against bottle samples, with every processing step documented.

## 1. Pre-cast checks
- Sensor serial numbers and **calibration coefficients** in the configuration (.xmlcon)
  match the instruments physically mounted. Swapped sensors with old coefficients is a
  classic silent error.
- Pump tubing connected, no air traps; conductivity cell clean (rinsed with fresh water,
  no Triton residue).
- Bottles cocked, lanyards free, vents and spigots closed.
- Pressure sensor reads near zero on deck (note the offset).
- Log station, position, water depth, time (UTC), weather/sea state.

## 2. The cast
1. Lower to ~10 m and **soak** until the pump turns on and sensors stabilise (typically
   1–3 min, oxygen needs longer); come back up to just below the surface, then start the
   downcast.
2. **Descent rate** ~0.5–1 m/s (GO-SHIP-style casts often ~1 m/s at depth, slower near
   surface and bottom) (gated: unconfirmed, source is paywalled or blocked). Steady speed matters more than the exact value; ship heave causes
   loops.
3. Bottom approach: watch the altimeter, stop ~5–10 m off bottom (depending on sea state
   and wire behaviour).
4. Fire bottles on the **upcast**, stopping and waiting ~30 s at each depth to flush and
   let sensors settle, then wait again after firing (bottle-sensor comparisons use the
   CTD data averaged at the firing time).
5. Use the downcast for the profile — the upcast is in the rosette's wake.

## 3. Sampling for calibration
- **Salinity** bottles (rinse 3×, fill to shoulder, dry the neck, cap tight); run on a
  salinometer (e.g. Guildline Autosal) standardised with **IAPSO Standard Seawater**, in a
  temperature-stable room, after samples equilibrate to room temperature.
- **Oxygen** by Winkler titration, drawn first from the Niskin, fixed immediately.
- Bottle-minus-CTD differences then give conductivity and oxygen corrections (linear in
  pressure/station is common).

## 4. Processing chain (Sea-Bird SBE Data Processing, typical order; confirm in the Seasoft manual) (gated: unconfirmed, source is paywalled or blocked)
1. **Data Conversion** — raw .hex to engineering units (.cnv); also produce a .ros of
   bottle-fire scans.
2. **Filter** — low-pass pressure (and conductivity on some systems) to reduce noise.
3. **Align CTD** — advance conductivity/oxygen relative to pressure to match the
   temperature sensor (for a 911 with pumped TC duct, conductivity is often already
   aligned by the deck unit; oxygen needs several seconds). *Values are instrument-specific;
   use manufacturer recommendations then tune by minimising salinity spiking.*
4. **Cell Thermal Mass** correction (α = 0.03, 1/β = 7 s are the Seasoft V2 manual defaults for SBE 4 cells, per the ctdcal docs; published work fits other values, e.g. Johnson et al. 2007 for SBE-41).
5. **Loop Edit** — flag scans where the CTD went backward or slowed (ship heave).
6. **Derive** — salinity, density, oxygen in µmol/kg (ideally then convert with TEOS-10 in
   your own code; see natural-sciences.oceanography.physical-oceanography.water-mass-analysis-with-ts-diagrams).
7. **Bin Average** — 1 dbar or 1 m bins, downcast only.
8. **Bottle Summary** — averages at fire times for calibration.
Script the chain (batch .bat/.txt with the same .psa settings) so every cast is identical.

## 5. QC
Plot T, S and density profiles together: density inversions beyond noise, salinity
spikes at sharp thermoclines, and T–S diagrams that disagree with neighbouring casts are
flags. Apply bottle-derived corrections and record them in metadata.

## Gotchas
- Calibrating against upcast bottle values compared with downcast sensor data.
- Biofouling or a jellyfish in the conductivity cell (sudden salinity offset mid-cast).
- Salinometer drift during a long run — standardise before and after.
- Starting the downcast at depth after the soak (missing the surface layer).

## Verify
- [ ] .xmlcon coefficients match mounted serial numbers.
- [ ] Soak done; downcast starts near the surface; descent steady.
- [ ] Processing chain identical across casts and saved with the data.
- [ ] Bottle-CTD salinity residuals small (e.g. ≲0.002–0.005 after correction for
      high-quality work) and without depth trend.
- [ ] Profiles free of unexplained density inversions and spikes.

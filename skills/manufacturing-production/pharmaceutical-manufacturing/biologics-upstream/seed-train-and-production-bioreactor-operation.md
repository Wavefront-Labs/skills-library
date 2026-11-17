---
id: manufacturing-production.pharmaceutical-manufacturing.biologics-upstream.seed-train-and-production-bioreactor-operation
name: seed-train-and-production-bioreactor-operation
category: manufacturing-production
field: pharmaceutical-manufacturing
product: biologics-upstream
tags: [biologics-upstream, upstream-processing, usp, cell-culture, cho-cells, mammalian-cell-culture, fermentation, seed-train, inoculum, vial-thaw, shake-flask, wave-bag, rocking-bioreactor, n-1, perfusion, fed-batch, stirred-tank, bioreactor, single-use-bioreactor, sub, ph-control, dissolved-oxygen, do, pco2, viable-cell-density, vcd, viability, vicell, nova-bioprofile, feeds, harvest, depth-filtration, contamination, sterile-connection, tube-welding, biopharmaceutical, pharmaceutical-manufacturing]
level: practitioner
status: draft
description: "Run a mammalian seed train and production bioreactor: thaw, expand to N-1, inoculate, control pH/DO/temperature, sample VCD and metabolites, feed, spot contamination and harvest."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Seed train and production bioreactor operation

**Goal:** expand cells from a frozen vial to a production bioreactor on schedule, keep
them healthy through a fed-batch (or perfusion) run, and hand over a clean harvest.
Written mainly for CHO fed-batch; microbial fermentation shares the logic but runs
faster, hotter on oxygen demand and with different foaming problems.

## 1. Seed train
1. **Thaw** a vial from the working cell bank: quick thaw (37 °C water bath or dry
   thawer, ~1–2 min), dilute promptly into pre-warmed medium to reduce cryoprotectant exposure.
2. **Expand** through shake flasks or rocking bags, then seed bioreactors (N-2, N-1).
   Each passage targets a seeding density and passes when viable cell density (VCD) and
   viability meet the batch record criteria — typically viability >90–95% (site/process specific).
3. Keep **passage count/population doubling** within the validated limit — cells too old
   for the process can't be used.
4. Everything open is done in a biosafety cabinet; closed transfers use **sterile
   tube welding** (e.g. Terumo, BioWelder) or aseptic connectors. Log every weld.

## 2. Bioreactor setup
- **Single-use** (Cytiva Xcellerex, Sartorius Biostat STR, Thermo HyPerforma): check bag
  ID/lot, install without kinking lines, leak test, verify probe connections.
- **Stainless**: SIP record complete, hold time not exceeded.
- **Calibrate**: pH probe (two-point before installation, then one-point offline
  re-standardisation against a blood-gas/offline analyser after media fill); DO probe
  (zero/span, polarise in advance for polarographic types).
- Media fill, warm to setpoint, equilibrate gas, then inoculate.

## 3. Control during the run
| Parameter | Typical approach (process-specific) |
|---|---|
| Temperature | e.g. 36.5–37 °C, possibly a shift down to ~32–34 °C mid-run to extend production |
| pH | e.g. 6.9–7.1; CO2 sparge to lower, base (Na2CO3/NaHCO3) to raise. Too much base raises osmolality |
| DO | e.g. 30–50% air saturation, cascaded through agitation, air, then O2 |
| pCO2 | Rises at high cell density; strip with air sparge/headspace; high pCO2 depresses growth |
| Foam | Antifoam (simethicone) as needed; it can foul downstream filters, so record every addition |

Take **daily samples** aseptically: VCD and viability (Vi-CELL, Cedex), glucose, lactate,
glutamine/ammonium, osmolality (Nova BioProfile), offline pH/pCO2. Use the results to
**feed** per the batch record (bolus or continuous feed, glucose top-up to target).

## 4. Spotting trouble
- **Contamination:** sudden DO crash or pH drop, rising O2 demand that doesn't match VCD,
  cloudiness, smell from sample. Microscopy/Gram stain and bioburden on suspicion; inform QA immediately.
- **Lactate accumulating** late in the run, or not switching to consumption, often indicates stress.
- **Viability falling early:** check shear (agitation/sparge), pCO2, osmolality, feed errors.
- **Probe drift:** compare online pH with offline daily; re-standardise within allowed offset.

## 5. Harvest
- Harvest on the day or viability criterion in the batch record.
- Clarify by centrifugation and/or **depth filtration** then 0.2 µm into a bag/tank; record
  pressures — a rapid rise means filters are loading (low viability, high debris).
- Take harvest samples (titre, bioburden, mycoplasma, adventitious agents per process).
- Hand off to downstream within the hold-time limit; see
  manufacturing-production.pharmaceutical-manufacturing.biologics-downstream.running-chromatography-and-tff-skids.

## Gotchas
- Inoculating before the pH/DO have stabilised.
- Using an expired or wrong-lot media bag — scan, don't read by eye.
- Base addition pump left in auto with a failed pH probe: the reactor gets dosed to pH 8+.
- Forgetting tube clamps before cutting a weld.

## Verify
- [ ] Vial and media lots traceable; passage number within limit.
- [ ] Probes calibrated and offline checks within allowed difference every day.
- [ ] Daily sample results and feeds recorded; parameters stayed in range or deviated.
- [ ] No contamination signals unexplained.
- [ ] Harvest within criteria and hold time; samples submitted.

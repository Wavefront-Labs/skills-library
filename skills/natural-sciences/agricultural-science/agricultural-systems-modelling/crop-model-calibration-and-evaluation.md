---
id: natural-sciences.agricultural-science.agricultural-systems-modelling.crop-model-calibration-and-evaluation
name: crop-model-calibration-and-evaluation
category: natural-sciences
field: agricultural-science
product: agricultural-systems-modelling
tags: [agricultural-science, agricultural-systems-modelling, crop-model, crop-simulation, apsim, apsim-next-gen, dssat, aquacrop, stics, wofost, calibration, parameterisation, cultivar-coefficients, phenology, validation, model-evaluation, rmse, nrmse, willmott-d, nash-sutcliffe, bias, sensitivity-analysis, glue, climate-impact, yield-forecasting, agmip, ensemble, weather-data, soil-parameters, canopy-remote-sensing]
level: advanced
status: draft
description: "Calibrate and evaluate a crop model (APSIM, DSSAT, AquaCrop) honestly: good inputs first, phenology then biomass then yield, separate evaluation data, standard error metrics, and stated uncertainty."
sources: [Wallach, Makowski, Jones & Brun, Working with Dynamic Crop Models (3rd ed.), AgMIP calibration protocol papers (Wallach et al. 2021, 2023), APSIM and DSSAT documentation, Willmott 1981]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crop model calibration and evaluation

**Goal:** adapt a process-based crop model to your cultivars, soils and climate, and
show with independent data how well it predicts — before using it for climate-impact,
management or yield-forecast studies.

## 1. Inputs before parameters
Most "calibration" problems are input problems. Get these right first:
- **Weather:** daily max/min temperature, radiation, rainfall (plus humidity/wind for
  Penman-type ET). On-site stations beat gridded products; check gaps, units (MJ/m²/d
  radiation) and radiation estimated from sunshine hours.
- **Soil:** layer depths, lower limit (LL15/wilting point), drained upper limit,
  saturation, bulk density, initial water and nitrogen at sowing. **Plant-available water
  capacity** and initial conditions drive water-limited yields more than crop parameters.
- **Management:** sowing date, density, depth, cultivar, fertiliser and irrigation events,
  residue.
- **Observations:** phenology dates (emergence, flowering, maturity — BBCH or Zadoks),
  biomass and LAI time series, final yield and components, soil water if available.

## 2. Calibrate in stages
Changing everything at once lets errors cancel. Sequence:
1. **Phenology** — thermal-time/photoperiod/vernalisation parameters for the cultivar
   against observed flowering and maturity dates.
2. **Canopy and biomass** — LAI development, radiation use efficiency, partitioning.
3. **Yield and components** — grain number and weight parameters.
4. **Water and N** — only if observations exist (soil water, crop N).
Calibrate the fewest parameters justified by data; prefer literature values for the rest.
Tools: built-in optimisers (APSIM NextGen "Optimise", DSSAT GLUE/GenCalc), R
(`apsimx`, `DSSAT` packages) or Python wrappers. Run a **sensitivity analysis** (e.g.
Morris or Sobol) first to find which parameters matter for your outputs.

## 3. Evaluate on separate data
Hold out sites/years/treatments not used for calibration (or cross-validate by
site-year). Report, per variable:
- **RMSE** and **nRMSE** (% of observed mean; rough convention: <10% excellent, 10–20%
  good, 20–30% fair — treat as indicative only).
- **Mean bias** (systematic over/under-prediction).
- **Willmott's d** or **Nash–Sutcliffe efficiency (NSE)**; NSE < 0 means the observed
  mean predicts better than the model.
- Observed vs simulated plots with the 1:1 line, and residuals vs drivers (water
  stress, sowing date).
Compare the error to the **observation error** and to between-treatment differences the
model must resolve. A 0.8 t/ha RMSE is useless if treatments differ by 0.3 t/ha.

## 4. Using the model
- **Climate impact:** run baseline vs future scenarios from several downscaled GCMs;
  bias-correct weather; keep management assumptions explicit (adaptation vs none).
  Include CO2 effects and say how the model handles them.
- **Multi-model ensembles** (AgMIP style) usually beat any single model; spread
  across models is part of the uncertainty.
- **Yield forecasting:** combine historical weather analogues for the rest of season
  with in-season data; assimilate remote-sensing canopy estimates (LAI, NDVI) where
  appropriate.
- Report uncertainty from parameters, inputs, and model structure — not single runs.

## Gotchas
- Calibrating against final yield only can give correct yields for wrong reasons
  (wrong phenology compensated by RUE) — then it fails in new climates.
- Default soil files from databases are often far off for a specific field.
- Model version changes alter outputs; record version, parameter files and seeds.
- Weather station and trial site at different elevation/exposure introduces bias.

## Verify
- [ ] Weather, soil and management inputs checked and documented before calibration.
- [ ] Calibration staged (phenology → canopy → yield) with few, justified parameters.
- [ ] Independent evaluation data with RMSE, nRMSE, bias, NSE/d and 1:1 plots.
- [ ] Model version, parameter files and scenario assumptions archived for reproduction.

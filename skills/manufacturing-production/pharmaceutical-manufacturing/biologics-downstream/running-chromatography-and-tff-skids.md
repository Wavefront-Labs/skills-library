---
id: manufacturing-production.pharmaceutical-manufacturing.biologics-downstream.running-chromatography-and-tff-skids
name: running-chromatography-and-tff-skids
category: manufacturing-production
field: pharmaceutical-manufacturing
product: biologics-downstream
tags: [biologics-downstream, downstream-processing, dsp, purification, chromatography, protein-a, ion-exchange, cation-exchange, anion-exchange, polishing, column-packing, hetp, asymmetry, akta-process, chromatography-skid, uv-280, peak-cutting, tff, tangential-flow-filtration, ultrafiltration, diafiltration, uf-df, tmp, flux, nwp, viral-inactivation, low-ph-hold, viral-filtration, planova, viresolve, filter-integrity-test, buffer-preparation, conductivity, monoclonal-antibody, mab, pharmaceutical-manufacturing]
level: practitioner
status: draft
description: "Operate biologics purification at scale: column qualification, Protein A and IEX runs with UV peak cutting, low-pH viral inactivation, viral filtration, UF/DF on TFF skids, and buffer prep checks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running chromatography and TFF skids

**Goal:** take clarified harvest to purified, concentrated bulk with the right yield and
impurity clearance, without losing a batch to a wrong buffer or a bad peak cut. Typical
monoclonal antibody (mAb) sequence: Protein A capture → low-pH viral inactivation →
one or two polishing columns (CEX/AEX, often AEX in flow-through) → viral filtration →
UF/DF → final filtration into bulk.

## 1. Buffer preparation (most batch losses start here)
- Weigh by scale-printout, add to WFI, mix the specified time, then test **pH and
  conductivity** at the specified temperature (both are temperature-dependent; use
  temperature compensation correctly).
- Filter (0.2 µm) into labelled bags; record expiry/hold time.
- A buffer in spec for pH but out for conductivity usually means a weighing error —
  investigate, don't adjust with acid/base to "fix" it.

## 2. Columns
- **Pack and qualify**: after packing (or before use per schedule) run a pulse test
  (acetone or NaCl) to get **HETP** (plate height) and **asymmetry** (often 0.8–1.8 acceptable;
  process-specific). Bad asymmetry = channelling or a void; repack.
- Store in the specified solution (e.g. 20% ethanol or NaOH-based) and track
  cycles/lifetime. Protein A resin is expensive and limited by cycle count and caustic exposure.

## 3. Running a chromatography step
Skids: Cytiva ÄKTA process, Repligen, Sartorius Resolute, or custom. The recipe runs
equilibrate → load → wash → elute → strip → sanitise (CIP with NaOH) → re-equilibrate.
- Check before start: correct column, correct buffers connected to correct inlets
  (scan/verify labels), air sensors and pressure alarms active, **load volume/amount**
  within resin capacity (g protein per L resin).
- **Watch pressure**: rising ΔP across runs = fouling or bed compression.
- **Peak cutting**: elution collected on UV 280 nm thresholds (start/stop OD or % of max)
  in the recipe. A UV detector out of range (saturated at high concentration) distorts
  cuts; some skids use a shorter path-length cell or a second wavelength (e.g. 300 nm).
- Record yield; an unexpected drop means check load concentration, buffer, or column performance.

## 4. Viral clearance steps
- **Low-pH hold** after Protein A: titrate to target pH (e.g. ~3.5–3.8), hold the
  validated time at temperature, then neutralise. Mixing must be thorough — a pocket
  that never reached target pH is a clearance failure. Time starts when pH is reached.
- **Viral filtration** (Planova, Viresolve Pro, Pegasus): pre-use flush, run at the
  validated pressure — **pressure interruptions or release** can reduce virus retention
  for some filters, so follow the procedure exactly. **Post-use integrity test** is mandatory.

## 5. UF/DF on TFF
- Install cassettes (Pellicon, Sartocon), flush storage solution, **normalised water
  permeability (NWP)** check vs baseline, integrity test (air diffusion).
- **Concentrate** to target, **diafilter** the specified number of diavolumes (often
  6–8) into formulation buffer, then final concentrate. Control **TMP** and crossflow
  per recipe — too-high TMP gels the membrane and drops flux.
- Recover product with buffer chase; record final concentration and volume; yield losses
  hide in the system hold-up.
- Clean (NaOH), recheck NWP, store.

## Gotchas
- Buffer lines swapped between inlets — the recipe runs perfectly on the wrong buffer.
- Load hold times exceeded between steps (bioburden, aggregation).
- Air in the column from an empty buffer bag.
- Over-concentrating in UF and getting viscosity-driven pressure spikes.
- Skipping post-use integrity test because the run "looked fine".

## Verify
- [ ] Buffers in spec for pH and conductivity at stated temperature, in date.
- [ ] Column HETP/asymmetry and cycle count within limits.
- [ ] Peak cuts per recipe; step yields in expected range.
- [ ] Low-pH hold reached target and held validated time; viral filter integrity passed.
- [ ] UF/DF diavolumes, final concentration and NWP recorded; hold times respected.

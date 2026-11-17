---
id: engineering-technology.petroleum-engineering.well-completion-design.hydraulic-fracture-design
name: hydraulic-fracture-design
category: engineering-technology
field: petroleum-engineering
product: well-completion-design
tags: [hydraulic-fracturing, frac-design, fracture-stimulation, minimum-horizontal-stress, closure-pressure, isip, mini-frac, dfit, step-rate-test, g-function, net-pressure, nolte-smith, proppant-selection, fracture-conductivity, fcd, plug-and-perf, cluster-spacing, limited-entry, slickwater, crosslinked-gel, frac-fluids, stimulation, unconventional]
level: advanced
status: draft
description: "Design a hydraulic frac: stress and closure from DFIT/G-function, ISIP and net pressure, proppant and conductivity (FCD), stage/cluster limited-entry design and fluid choice."
sources:
  - "Economides & Nolte, Reservoir Stimulation (3rd ed.)"
  - "Barree, Barree & Craig, Holistic Fracture Diagnostics (SPE 107877)"
  - "Nolte, Determination of Fracture Parameters from Fracturing Pressure Decline (SPE 8341)"
  - "API RP 19C / ISO 13503-2, Measurement of Properties of Proppants"
  - "API RP 19D / ISO 13503-5, Measuring Long-Term Conductivity of Proppants"
  - "Cinco-Ley & Samaniego, Transient Pressure Analysis for Fractured Wells (JPT, 1981)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hydraulic fracture design — stress, diagnostics, proppant and stage layout

**Goal:** produce a frac design (stages, clusters, fluid, proppant, rate and pressure limits) grounded in measured stress and leak-off, with a conductivity target matched to the reservoir.

> Engineering guidance. Treating pressures load casing, wellhead and surface iron; respect the burst limits from engineering-technology.petroleum-engineering.drilling-engineering.casing-design-and-kick-tolerance and the operator's pressure-control standards.

## 1. Stress and closure

- Minimum horizontal stress σh controls fracture pressure and height containment. First estimate from the uniaxial-strain model: σh = ν/(1−ν)·(σv − α·Pp) + α·Pp (+ tectonic term), using dipole-sonic Poisson's ratio. Typical frac gradients: 0.65–1.0 psi/ft; layers with higher σh (often by > 500–1000 psi) act as height barriers.
- Calibrate with a **DFIT / mini-frac**: inject a few to ~20–50 bbl of water at low rate, shut in, record pressure for hours to days.

## 2. Reading the DFIT

- **ISIP** = pressure immediately after shut-in, picked after the water-hammer dies. ISIP gradient = ISIP_bottomhole / TVD.
- **Near-wellbore friction** (perf + tortuosity) = last pumping pressure − ISIP; step-down tests split it: perf friction ∝ q², tortuosity ∝ q^0.5.
- **G-function** plot: plot P, dP/dG and G·dP/dG vs G time. Closure is where G·dP/dG departs below the straight line through the origin (normal leak-off). Hump above the line = pressure-dependent leak-off (natural fissures); concave-down tail = height recession or transverse storage. Confirm with √t and log-log derivative.
- After closure: identify pseudo-linear (−½ slope) or pseudo-radial flow to estimate pore pressure and permeability (Nolte/Soliman after-closure analysis). Ultra-tight rock may never reach radial flow in practical time — say so rather than over-interpret.
- **Step-rate test** (conventional/injectors): plot BHP vs rate; the break in slope is the fracture extension pressure, an upper bound on closure.
- **Net pressure** = BHP − closure. Nolte–Smith log-log plot during the main treatment: small positive slope = confined height growth; flat = height growth or fissure opening; steep positive (~1) = tip screen-out/restriction; negative = uncontrolled height growth.

## 3. Conductivity and proppant

Dimensionless fracture conductivity: FCD = kf·wf / (k·xf). Aim for FCD ≈ 1.6 at optimum for a fixed proppant volume in moderate-k rock (Unified Fracture Design); in high-permeability frac-packs conductivity dominates, in nano-darcy shale fracture area dominates and FCD is huge regardless.

- Proppant choice by closure stress on proppant (closure − flowing BHP): local/white sand to ~6,000 psi; resin-coated sand to ~8,000 psi; intermediate/ high-strength ceramics above. Check API RP 19C crush (fines %) and RP 19D long-term conductivity, then apply realistic reductions for embedment, fines, multiphase and non-Darcy flow — field conductivity is often an order of magnitude below lab values.
- Mesh: 100-mesh and 40/70 dominate shale slickwater; 20/40 and larger where conductivity matters.

## 4. Stage and cluster design (horizontal plug-and-perf)

- Stage length 150–300 ft with 3–8 clusters is typical of current shale practice; cluster spacing 15–50 ft. Tighter spacing increases stress shadowing that starves inner clusters.
- **Limited entry**: size perforations so perf friction (often 1,000–2,000 psi at design rate) forces even distribution. Perf friction ΔP = 0.2369·q²·ρ / (Np²·d⁴·Cd²) in field units (q bpm total, ρ ppg, d in., Cd 0.6–0.9 rising with erosion). Erosion reduces it during the job; plan for it.
- Rate 60–100+ bpm for slickwater shale stages; proppant intensity 1,500–3,000+ lb/ft and fluid 30–60 bbl/ft are common ranges — basin and operator specific.

## 5. Fluid systems

| Fluid | Viscosity | Use |
|---|---|---|
| Slickwater (friction reducer) | 2–10 cP | shale, complex fracture area, small proppant |
| HVFR (high-viscosity friction reducer) | 10–50 cP | more proppant transport without gel |
| Linear gel (guar) | 10–50 cP | hybrid tail-ins |
| Crosslinked borate/zirconate | 100–1000 cP | conventional, high-perm, larger proppant, frac-packs |
| Energised/foam (N2, CO2) | variable | water-sensitive or low-pressure reservoirs |

Gels need breakers; residue damages conductivity.

## Gotchas

- Picking closure at the first inflection of P vs √t without the G·dP/dG check often over-reads closure.
- Wellhead ISIP must be converted to bottomhole using the actual fluid density in the wellbore.
- Ignoring stress shadow and parent–child depletion: child wells frac toward depleted parents.
- Screen-out risk rises with high proppant concentration in low-viscosity fluid near the end of stage; watch net pressure slope.

## Verify

- [ ] Closure stress, ISIP gradient and net pressure picked with method stated (G-function plus a second plot).
- [ ] Height containment checked against stress contrast in bounding layers.
- [ ] Proppant rated for effective closure stress with field-reduced conductivity; FCD estimated.
- [ ] Perf friction at design rate meets the limited-entry target.
- [ ] Max surface treating pressure below casing/wellhead limits with the operator's safety factor.
- [ ] Post-job net-pressure history-match and production compared with the design.

Feed the resulting fracture half-length and conductivity into engineering-technology.petroleum-engineering.production-engineering.nodal-analysis-and-artificial-lift-selection for the inflow model.

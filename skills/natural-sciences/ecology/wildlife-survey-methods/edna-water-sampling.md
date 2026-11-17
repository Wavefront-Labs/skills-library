---
id: natural-sciences.ecology.wildlife-survey-methods.edna-water-sampling
name: edna-water-sampling
category: natural-sciences
field: ecology
product: wildlife-survey-methods
tags: [wildlife-survey-methods, edna, environmental-dna, water-sampling, filtration, filter-pore-size, sterivex, field-blank, negative-control, contamination, bleach-decontamination, longmire-buffer, ethanol-preservation, qpcr, ddpcr, metabarcoding, 12s, coi, species-detection, great-crested-newt, invasive-species, fish-survey, amphibian-survey, occupancy, false-negative, false-positive, biodiversity-monitoring]
level: practitioner
status: draft
description: "Collect environmental DNA from water without contaminating it: sampling design, filtration volume and pore size, field blanks, preservation, decontamination and detection caveats."
sources: ["C. S. Goldberg et al., Critical considerations for the application of eDNA methods, Methods Ecol. Evol. 7 (2016) 1299", "C. S. Goldberg, K. M. Strickler & D. S. Pilliod, Moving eDNA surveys onto the next level, Biol. Conserv. 183 (2015) 1", "Natural England / Defra great crested newt eDNA technical advice (WC1067)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# eDNA water sampling

**Goal:** water samples whose DNA results answer "is species X (or which species)
present at this site?" — with controls good enough that a positive is believable and
a negative is interpretable.

## 1. Design before you go
- **Question:** single-species (qPCR/ddPCR assay) or community (metabarcoding with e.g.
  12S for fish/vertebrates, COI for invertebrates)? This sets volume, replication and lab.
- **Spatial replication:** eDNA is patchy. Take several samples per site (e.g. 3–5
  filters, or a composite of many sub-samples around a pond margin), not one jar.
- **Timing:** sample when the target is active and shedding DNA (breeding season for
  amphibians, spawning for fish). Avoid right after heavy rain/high flows if possible.
- Plan for **occupancy-style analysis** (sites × replicates × qPCR replicates) so
  detection probability can be estimated (see natural-sciences.ecology.statistical-ecology.single-season-occupancy-modelling).
- Coordinate with the lab: their filter type, preservative and assay requirements.

## 2. Contamination control
- Single-use sterile gloves, changed between sites; pre-sterilised or single-use bottles,
  filter housings and syringes.
- Reusable gear (boots, nets, poles, bottles): soak/wipe with **~10% household bleach**
  (fresh), rinse with DNA-free water; or use dedicated kit per site.
- Work **downstream to upstream** in rivers so you don't carry DNA up into the next site.
- Never carry tissue samples, specimens or lab PCR products in the same vehicle/kit.
- **Field blank:** filter DNA-free (distilled/bottled) water at each site or each day
  with the same gear and handling — it tests the whole field chain.

## 3. Filtration
- Filter on site when possible (DNA degrades within hours to days in warm water).
- Volume: more is better until the filter clogs; commonly 0.5–2 L per filter in clear
  water; turbid water may clog after 100–250 mL — record actual volume filtered.
- Pore size: 0.45 µm (capture-efficient, clogs faster) to 1–5 µm (faster in turbid
  water); enclosed cartridges (e.g. Sterivex) reduce handling contamination.
- Avoid stirring up sediment (old DNA persists in sediment).

## 4. Preservation and transport
- Fill/cover the filter with preservative (Longmire's buffer, ATL, or ≥ 95% ethanol) or
  freeze on dry ice; keep cool and dark. Label: site, replicate, date, time, volume.
- Ship to the lab with chain-of-custody documentation if results have regulatory use.

## 5. Interpreting results
- **Positive with clean blanks:** DNA of the target was in the water — not proof the species
  lives there (could be transported downstream, from predator faeces, from upstream
  fish farms, or from boots of the last surveyor).
- **Negative:** absence of evidence; detection probability per sample may be well below 1.
  Report the number of replicates and assay sensitivity (limit of detection).
- **Any positive blank** → the batch is suspect; report it, don't quietly drop it.

## Gotchas
- PCR inhibitors (humic acids in brown water) cause false negatives; ask the lab for
  inhibition controls.
- Sampling the same site with gear just used at a positive site is the commonest
  contamination route.
- *Uncertainty note:* volumes, pore sizes and bleach concentrations are typical values
  from published protocols; regulatory schemes (e.g. UK great crested newt eDNA) specify
  their own exact methods — follow them when results feed a licence.

## Verify
- [ ] Field blank collected per site/day and handled identically.
- [ ] Gear decontaminated or single-use between sites; upstream order respected.
- [ ] Volume filtered recorded for every filter.
- [ ] Filters preserved within the time limit agreed with the lab.
- [ ] Results reported with replicate counts, blanks and limit of detection.

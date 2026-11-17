---
id: engineering-technology.biomedical-engineering.biomaterials.biocompatibility-evaluation-iso-10993
name: biocompatibility-evaluation-iso-10993
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [biocompatibility, iso-10993-1, iso-10993-5, iso-10993-10, iso-10993-12, iso-10993-17, iso-10993-18, iso-10993-23, biological-evaluation-plan, chemical-characterisation, extractables-leachables, toxicological-risk-assessment, aet, cytotoxicity, sensitisation, irritation, implant-materials, ti-6al-4v, cocr, peek, uhmwpe, 316l]
level: advanced
status: verified
description: "Plan an ISO 10993-1 biological evaluation: categorise contact and duration, pick endpoints, run 10993-18 chemistry and 10993-17 toxicological risk, and choose implant materials."
sources: ["https://www.fda.gov/medical-devices", "ISO 10993-1 Biological evaluation of medical devices - Evaluation and testing within a risk management process", "ISO 10993-5 Tests for in vitro cytotoxicity", "ISO 10993-10 Tests for skin sensitization", "ISO 10993-12 Sample preparation and reference materials", "ISO 10993-17:2023 Toxicological risk assessment of medical device constituents", "ISO 10993-18:2020 Chemical characterization of medical device materials", "ISO 10993-23 Tests for irritation", "FDA guidance: Use of International Standard ISO 10993-1 (2023)", "ASTM F136, F75, F1537, F138, F648, F2026 material specifications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Biocompatibility evaluation to ISO 10993 — risk-based, chemistry first

**Goal:** build a biological evaluation plan (BEP) and report (BER) that justifies the device's biological safety with the minimum necessary animal testing.

Engineering guidance; final conclusions need a qualified toxicologist and the current editions (ISO 10993-1 was revised in 2025 with changes to categorisation; check which edition your regulator recognises).

## 1. Categorise the device (10993-1)

**Nature of contact:**
- Surface: intact skin; mucosal membrane; breached or compromised surface.
- Externally communicating: blood path indirect; tissue/bone/dentin; circulating blood.
- Implant: tissue/bone; blood.

**Duration (cumulative, including repeat use):** limited ≤ 24 h; prolonged > 24 h to 30 days; long-term > 30 days. Categorise each patient-contacting component; the worst case drives the device category.

## 2. Gather what you already know

Material identities and grades, formulation (additives, colourants, processing aids), manufacturing (machining fluids, cleaning, mould release), sterilisation (EtO residuals per 10993-7, irradiation effects on polymers), packaging, and clinical history of identical materials in the same use. Equivalence arguments must cover processing and sterilisation, not just the material name.

## 3. Endpoints

The 10993-1 / FDA matrix lists endpoints to *address* (by data, literature, chemistry or test), e.g.:
- All contact types: **cytotoxicity** (10993-5), **sensitisation** (10993-10), **irritation/intracutaneous reactivity** (10993-23).
- Adding with invasiveness/duration: acute systemic toxicity (10993-11), material-mediated pyrogenicity, subacute/subchronic and chronic toxicity, **genotoxicity** (10993-3), **implantation** (10993-6), **haemocompatibility** (10993-4) for blood contact, carcinogenicity for some long-term implants.

Typical acceptance (ISO 10993-5, (gated: unconfirmed, source is paywalled or blocked)): cytotoxicity (MEM elution) viability ≥ 70% of blank, or reactivity grade ≤ 2 qualitatively; sensitisation by GPMT or LLNA with no significant response.

## 4. Sample preparation (10993-12)

Extraction conditions such as 37 °C/72 h, 50 °C/72 h, 70 °C/24 h or 121 °C/1 h; ratio 6 cm²/mL for thickness ≤ 0.5 mm, 3 cm²/mL for 0.5 to 1.0 mm, 1.25 cm²/mL above 1.0 mm, or 0.2 g/mL for irregular forms (gated: unconfirmed, source is paywalled or blocked). Use polar and non-polar vehicles. Test final, sterilised, production-equivalent devices.

## 5. Chemical characterisation and toxicological risk

**10993-18:** extractables study (exhaustive or exaggerated extraction with polar, semi-polar and non-polar solvents) analysed by GC-MS, LC-MS and ICP-MS. Set the **analytical evaluation threshold (AET)** from a dose-based threshold (e.g. TTC of 1.5 µg/day for long-term exposure (gated: unconfirmed, source is paywalled or blocked), higher for shorter durations), the number of devices extracted and expected daily exposure, divided by an **uncertainty factor** for response-factor variation. Report and identify every compound above AET.

**10993-17:2023:** for each constituent derive a tolerable intake (TI) from a point of departure with modifying factors, estimate exposure dose (EEDmax), and calculate **margin of safety MoS = TI/EED**; MoS ≥ 1 generally acceptable. Robust chemistry plus MoS can replace systemic toxicity, genotoxicity and carcinogenicity testing, but rarely replaces cytotoxicity, sensitisation or irritation.

## 6. Implant material notes

| Material | Spec | Notes |
|---|---|---|
| Ti-6Al-4V ELI | ASTM F136 | E ≈ 110 GPa, excellent corrosion resistance; poor wear surface |
| CoCrMo | F75 cast, F1537 wrought | E ≈ 210-240 GPa, bearing surfaces; metal-ion and wear-debris concerns |
| 316L stainless | F138 | E ≈ 190-200 GPa; Ni sensitisation, crevice corrosion; mostly temporary implants |
| PEEK | F2026 | E ≈ 3-4 GPa, radiolucent, MRI-friendly; bioinert, needs surface treatment for ongrowth |
| UHMWPE | F648 | bearing liners; crosslinking cuts wear; vitamin E or remelting to control oxidation |

Cortical bone is ~15-20 GPa: high-modulus stems cause stress shielding.

## Gotchas

- "Material is ISO 10993 compliant" from a supplier says little about your processed, sterilised device.
- Colourants and processing aids are the usual unexpected extractables.
- Changing sterilisation method or supplier is a biological-evaluation change.
- Cumulative duration: a daily-use 2-hour device used for months is long-term.
- Particles and wear debris are outside ordinary extract tests; evaluate separately.

## Verify

- [ ] Every patient-contacting component categorised by contact and cumulative duration.
- [ ] Each matrix endpoint addressed by test, chemistry or justified rationale.
- [ ] Extractables cover all compounds above a justified AET with UF stated.
- [ ] MoS ≥ 1 (or justified) for each identified constituent.
- [ ] Tests used final, sterilised, production-equivalent samples.
- [ ] Material specs and grades traceable to ASTM/ISO standards.

---
id: defence-public-safety.forensic-science.forensic-toxicology.screening-confirmation-and-interpreting-results
name: screening-confirmation-and-interpreting-results
category: defence-public-safety
field: forensic-science
product: forensic-toxicology
tags: [forensic-toxicology, toxicology, post-mortem-toxicology, drug-screening, immunoassay, confirmation-testing, gc-ms, lc-ms-ms, hrms, blood-alcohol, bac, widmark, back-calculation, femoral-blood, cardiac-blood, vitreous-humour, urine, post-mortem-redistribution, drug-facilitated-sexual-assault, dfsa, drug-driving, duid, impairment, metabolites, nps, novel-psychoactive-substances, fentanyl-analogues, chain-of-custody, sodium-fluoride, therapeutic-toxic-lethal-ranges, soft-tox]
level: advanced
status: draft
description: "Run forensic toxicology casework: right specimens and preservatives, immunoassay/HRMS screen then MS confirmation, and interpret concentrations with post-mortem redistribution and tolerance in mind."
sources: ["ANSI/ASB Standard 036 (method validation) and 119/120 (scope of testing for DUID/DFSA/death investigation)", "SOFT/AAFS Forensic Toxicology Laboratory Guidelines", "Baselt, Disposition of Toxic Drugs and Chemicals in Man (reference)", "UK Forensic Science Regulator toxicology guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screening, confirmation and interpreting results

**Goal:** report which drugs, alcohol or poisons were present in a casework sample at
what concentration, and say — carefully — what that can and cannot mean for impairment
or cause of death.

## 1. Specimens decide what you can say
| Specimen | Use and caveat |
|---|---|
| **Peripheral (femoral) blood** | Preferred for post-mortem quantitation; less affected by redistribution |
| Cardiac/central blood | Screening; concentrations often higher than femoral post-mortem |
| **Vitreous humour** | Alcohol (supports/refutes post-mortem production), electrolytes, glucose |
| Urine | Wide detection window; shows exposure, *not* effect at the time |
| Liver, gastric contents | Overdose context, large-volume ingestion |
| Hair | Long-term/historic exposure, DFSA weeks later (segmental analysis) |
| Oral fluid | Roadside/DUID screening |

- Blood in **grey-top tubes (sodium fluoride/potassium oxalate)** to inhibit microbial
  alcohol production and cocaine breakdown; refrigerate. Note collection site and time.
- For **DFSA**, collect blood and urine as soon as possible — many sedatives are below
  detection within 24–72 h (urine extends it). Hair later if the window is missed.
- Chain of custody on every container; sealed and signed.

## 2. Analytical workflow
1. **Screen:** immunoassay (fast, class-level, cross-reactivity issues — a positive is
   *presumptive*) and/or broad chromatographic screens: GC-MS, LC-MS/MS, or LC-HRMS which
   can be re-interrogated retrospectively for **novel psychoactive substances** and new
   fentanyl analogues.
2. **Confirm:** a second, independent, more specific technique on a separate aliquot —
   typically targeted LC-MS/MS or GC-MS with an isotopically labelled internal standard
   and calibrators bracketing the result. Two ion transitions with ion-ratio criteria.
3. **Alcohol:** headspace GC with FID, duplicate analysis, often two columns.
4. **Quantitation:** within the validated calibration range; report the uncertainty of
   measurement. Results above the top calibrator are diluted and rerun, not extrapolated.
5. Validation per ASB 036 (bias, precision, LOD/LOQ, carryover, interferences, matrix effects).

## 3. Interpretation — where cases are won or lost
- **Post-mortem redistribution (PMR):** drugs with large volume of distribution (e.g.
  tricyclics, digoxin, some opioids) diffuse from tissues into blood after death, so
  concentrations can rise many-fold. Compare femoral vs cardiac; don't apply living-person
  therapeutic/toxic ranges uncritically.
- **Tolerance:** an opioid concentration fatal to a naive user may be routine in a
  long-term user. Look at history, scene findings, metabolite ratios.
- **Metabolite presence** shows time course: e.g. 6-MAM indicates heroin (rather than
  codeine/morphine); parent-to-metabolite ratios hint at recent vs earlier use, with wide
  uncertainty.
- **Alcohol back-calculation** (Widmark-based) requires assumptions — elimination rate
  (commonly ~0.10–0.25 g/L/h range), absorption complete, no drinking after the event.
  State them; give a range, not a point.
- **Impairment** from a single blood concentration is generally not determinable for most
  drugs (unlike per-se limits set by law). Say what the law asks and what the science supports.
- Present findings to the pathologist as part of the whole picture — toxicology contributes
  to cause of death, it rarely determines it alone.

## Gotchas
- Absence in a screen ≠ absence: check the scope of testing lists the drug and its LOD.
- Putrefaction produces ethanol (and some amines); vitreous and urine alcohol help separate.
- Cocaine continues to break down in unpreserved samples — benzoylecgonine-only can be an
  artefact of storage time.
- Immunoassay false positives (e.g. some medications cross-reacting with amphetamine assays)
  must never be reported without confirmation.

## Verify
- [ ] Specimen types, collection sites, preservative and times recorded.
- [ ] Every reported positive confirmed by a second, specific method.
- [ ] Quantitation within calibration range with uncertainty stated.
- [ ] Interpretation addresses PMR, tolerance and specimen limitations.
- [ ] Report gives scope of testing and LODs for "not detected" statements.

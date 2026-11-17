---
id: health-medicine.clinical-research-operations.pharmacovigilance-and-safety-assessment.sae-causality-expectedness-and-expedited-reporting
name: sae-causality-expectedness-and-expedited-reporting
category: health-medicine
field: clinical-research-operations
product: pharmacovigilance-and-safety-assessment
tags: [pharmacovigilance-and-safety-assessment, clinical-research-operations, pharmacovigilance, drug-safety, adverse-event, serious-adverse-event, sae, susar, causality-assessment, expectedness, reference-safety-information, investigators-brochure, ich-e2a, ich-e2f, dsur, ctcae, who-umc, cioms, 21-cfr-312-32, ind-safety-report, eu-ctr-536-2014, eudravigilance, signal-detection]
level: practitioner
status: verified
description: "Assess trial adverse events: seriousness (ICH E2A), severity (CTCAE), causality, expectedness vs RSI, and SUSAR clocks (7/15-day) under FDA IND safety rules and EU CTR."
sources:
  - "ICH E2A Clinical Safety Data Management: Definitions and Standards for Expedited Reporting (1994)"
  - "ICH E2F Development Safety Update Report (2010)"
  - "21 CFR 312.32 (IND safety reporting) and 312.64 (investigator reports)"
  - "FDA Guidance: Safety Reporting Requirements for INDs and BA/BE Studies (2012) and Sponsor Responsibilities draft (2021)"
  - "Regulation (EU) No 536/2014, Articles 40-44 and Annex III"
  - "Clinical Trials Facilitation and Coordination Group (CTFG/CTCG) Q&A on Reference Safety Information"
  - "NCI Common Terminology Criteria for Adverse Events (CTCAE)"
  - "CIOMS Working Group VI, Management of Safety Information from Clinical Trials (2005)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# SAE causality, expectedness and expedited reporting

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** for each adverse event, make four separate, documented calls — serious?, how
severe?, related?, expected? — and from them decide whether it is a SUSAR and which
clock is running.

## 1. Four separate questions
| Question | Standard | Answer |
|---|---|---|
| **Serious?** | ICH E2A / 21 CFR 312.32(a) | Death; life-threatening (at the time); in-patient hospitalisation or prolongation; persistent/significant disability or incapacity; congenital anomaly; **important medical event** by medical judgement |
| **Severity** | CTCAE grade (version per protocol; NCI CTEP lists v6, 2025, as current, grade definitions in the version document) or mild/moderate/severe | Intensity only — "severe" headache is not serious |
| **Related?** | Investigator and sponsor judgement | Reasonable possibility yes/no (FDA: "suspected adverse reaction"); WHO-UMC categories if used |
| **Expected?** | **Reference safety information** (RSI) in the IB or SmPC (the RSI document named in the protocol), version approved at event onset | Listed in nature, severity, specificity and outcome? |

**SUSAR** = serious + suspected (related) + unexpected.

## 2. Causality reasoning
Weigh, and write down:
- Temporal relationship (onset after exposure; plausible latency).
- Dechallenge/rechallenge (improves on stopping; recurs on re-exposure).
- Biological plausibility, class effects, known mechanism.
- Alternative explanations: disease progression, con-meds, procedures, comorbidity.
- Dose-response, if any.

Regional difference: in the EU the sponsor may not downgrade the investigator's causality
for expedited reporting (CTR Annex III: the investigator's causality assessment shall not be downgraded; if the sponsor disagrees both opinions go in the report); under FDA rules the sponsor makes the reporting
causality call using aggregate data, while recording the investigator's view.
Unblinding: SUSARs are generally reported unblinded to regulators while the study team stays
blinded; CTR Art 43 annual reports cover IMPs other than placebo (verify the unblinding rule in the current CTFG/EMA guidance and sponsor SOP).

## 3. Timelines
| Step | US (IND) | EU (CTR) |
|---|---|---|
| Investigator → sponsor (SAE) | "Immediately" (312.64(b)); the protocol usually sets 24 h | Without undue delay, not later than 24 h of obtaining knowledge unless the protocol provides otherwise (Art 41(2)) |
| Fatal/life-threatening SUSAR | FDA notified as soon as possible and **no later than 7 calendar days** after initial receipt (312.32(c)(2)) | EU database **as soon as possible, ≤7 days** after awareness (Art 42(2)(a)); an initial incomplete report followed by a complete one is allowed (Art 42(2)) |
| Other SUSAR | IND safety report **within 15 calendar days** after the sponsor determines it qualifies (312.32(c)(1)) | **≤15 days** after awareness (Art 42(2)(b)) |
| Aggregate | IND annual report (312.33) or DSUR | Annual safety report (Art 43; ICH E2F DSUR format) |
| Day 0 | US 7-day clock: sponsor's initial receipt of the information; 15-day clock: determination that it qualifies. EU: sponsor awareness (Art 42(2)) |

FDA also expects 15-day reports for aggregate findings (e.g. an imbalance of events in
the drug arm) and findings from other studies or animal data suggesting significant risk.

## 4. Narrative and follow-up
- Narrative: demographics, relevant history, exposure (dose, dates), event chronology,
  investigations, treatment, outcome, dechallenge/rechallenge, causality rationale.
- Code with MedDRA (LLT → PT); request follow-up until resolution or stabilisation.
- Pregnancy exposure is followed to outcome even though not itself an AE.

## 5. Signal evaluation
Review cumulative listings by PT/SMQ, compare rates across arms, look for clusters by
time-to-onset, dose or subgroup. A validated signal goes to the safety committee/DMC and
may change the RSI, IB, consent and protocol.

## Gotchas
- Hospitalisation for an elective, pre-planned procedure is not usually an SAE (protocol-defined).
- Expectedness uses the RSI in force at the time, not a newer IB awaiting approval.
- "Unlikely related" in a 5-point scale may map to "not related" — know the binary mapping.
- Disease-progression endpoints may be exempt from expedited reporting only if the protocol says so.

## Verify
- [ ] Seriousness, severity, causality and expectedness recorded separately with rationale.
- [ ] RSI version at onset identified.
- [ ] Day 0 and 7/15-day clock correctly calculated for each region.
- [ ] Narrative complete; MedDRA coded; follow-up scheduled.
- [ ] Cumulative review done for possible signal.

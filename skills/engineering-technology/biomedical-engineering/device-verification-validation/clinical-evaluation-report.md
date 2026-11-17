---
id: engineering-technology.biomedical-engineering.device-verification-validation.clinical-evaluation-report
name: clinical-evaluation-report
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [clinical-evaluation-report, clinical-evaluation, clinical-investigation, cer, mdr-annex-xiv, medical-devices-regulation, clinical-data, state-of-the-art]
level: practitioner
status: verified
description: "Structure an EU MDR clinical evaluation report: scope, state of the art, data sources, appraisal, analysis, conclusion on benefit-risk, and update triggers."
sources: ["https://eur-lex.europa.eu/eli/reg/2017/745/oj", "Regulation (EU) 2017/745 Medical Devices Regulation, Article 61 and Annex XIV Part A (confirm current consolidated text)", "MDCG 2020-13 Clinical evaluation assessment report template (European Commission; confirm current)", "MEDDEV 2.7/1 revision 4 Clinical evaluation (guidance under the previous directives; still referenced)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clinical evaluation report (CER)

**Goal:** document, with traceable data, that the device achieves its intended performance and that its benefit-risk profile is acceptable, per the EU MDR.

Regulatory writing; clinical and regulatory staff own the conclusions. Confirm current MDR text and MDCG guidance. This note is practice guidance.

## Sections (typical)
1. **Scope and plan:** the clinical evaluation plan (CEP) from Annex XIV Part A: intended use, target populations, indications and contraindications, clinical benefits and parameters, state of the art, questions to address.
2. **Device description and claims.**
3. **State of the art:** current standard of care and alternative devices, benchmarks for safety and performance.
4. **Data sources:**
   - Clinical investigations of the device.
   - Literature on the device or an **equivalent device** (equivalence under MDR demands technical, biological and clinical equivalence and sufficient access to the equivalent device's data; see equivalence-demonstration).
   - Post-market surveillance, registries and complaints.
5. **Appraisal:** for each data set, assess methodological quality and relevance with a defined scheme, with weighting.
6. **Analysis:** pooled or comparative analysis of safety and performance against the CEP's acceptance criteria and against the state of the art.
7. **Conclusion:** confirms conformity with relevant general safety and performance requirements, clinical benefits and residual risk, with gaps identified (and a PMCF plan, see pmcf-plan).
8. **Qualifications:** CVs or declarations of the evaluators.
9. **Update plan:** the clinical evaluation is updated throughout the life cycle with PMS and PMCF data (Art. 61(11)); for class III and implantable devices the PMCF evaluation report (and the summary of safety and clinical performance) is updated at least annually (checked in the consolidated MDR text on EUR-Lex).

## Gotchas
- Equivalence claims without data access or with differences hidden.
- Literature search without protocol, databases, search terms and dates.
- Benefit-risk analysis disconnected from ISO 14971 residual risk.

## Verify
- [ ] Every claim has a cited, appraised source.
- [ ] Conclusions meet acceptance criteria in the CEP.
- [ ] Linked to the technical documentation and PMS plan.

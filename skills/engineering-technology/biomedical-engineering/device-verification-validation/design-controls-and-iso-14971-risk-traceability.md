---
id: engineering-technology.biomedical-engineering.device-verification-validation.design-controls-and-iso-14971-risk-traceability
name: design-controls-and-iso-14971-risk-traceability
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [design-controls, qmsr, 21-cfr-820, iso-13485, iso-14971, iso-tr-24971, design-inputs, design-outputs, traceability-matrix, design-verification, design-validation, v-and-v, test-protocol, sample-size, success-run, tolerance-interval, risk-management-file, risk-control, residual-risk, benefit-risk, dhf, test-method-validation, fmea]
level: practitioner
status: gated
description: "Run design controls under the QMSR/ISO 13485 and ISO 14971: inputs to outputs, trace matrix, V&V protocols with sample-size rationale, risk-control verification and residual-risk sign-off."
sources: ["21 CFR Part 820 Quality Management System Regulation (final rule 2024, effective 2 Feb 2026; effective date confirmed via the Federal Register API, technical amendments 90 FR 55978, and 21 CFR 820.10 / 820.7 on eCFR)", "ISO 13485:2016 Medical devices - Quality management systems", "ISO 14971:2019 Medical devices - Application of risk management to medical devices", "ISO/TR 24971:2020 Guidance on the application of ISO 14971", "FDA Design Control Guidance for Medical Device Manufacturers (1997)", "ISO 16269-6:2014 Statistical interpretation of data - Determination of statistical tolerance intervals https://www.iso.org/standard/57191.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Design controls and ISO 14971 risk traceability — every requirement and every hazard closed by evidence

**Goal:** keep a design-and-development file in which each user need, design input and risk control traces forward to an output and to objective verification/validation evidence, and backward from every test to the reason it exists.

Engineering guidance; your QMS procedures and the regulation text govern. The regulatory submission itself is out of scope here.

## 1. Regulatory frame

Since **2 February 2026** FDA's **QMSR** replaces the old 21 CFR 820 QSR and incorporates **ISO 13485:2016** by reference; design controls now live in ISO 13485 clause 7.3 (planning, inputs, outputs, review, verification, validation, transfer, changes, design and development file). FDA keeps some additions (e.g. its definitions and record requirements); check the rule for those. ISO 14971:2019 (with ISO/TR 24971) is the risk process; in the EU, EN ISO 14971:2019+A11:2021 annexes link it to the MDR requirement to reduce risk as far as possible.

## 2. Inputs and outputs

- **User needs** (qualitative, from users/clinicians) → **design inputs** (verifiable: number, tolerance, test condition). "Easy to carry" becomes "mass ≤ 450 g including battery".
- Inputs come from needs, standards (IEC 60601 family, ISO 10993), usability, and **risk controls**, which become requirements in their own right.
- **Design outputs**: drawings, specs, software, labelling, process specs. Identify essential outputs (those critical to safety and performance).
- Run design reviews at planned stages with an independent reviewer.

## 3. Trace matrix

Minimum columns: user need → design input → design output → verification method and report → validation activity. A parallel risk trace: hazard → hazardous situation → harm → risk control → requirement → verification of *implementation* → verification of *effectiveness*. Tooling may be a requirements-management system (Jama, Polarion, codeBeamer-class) or a controlled spreadsheet; what matters is bidirectional links and no orphans.

## 4. ISO 14971 risk file

1. **Plan:** scope, responsibilities, risk acceptability criteria (severity × probability matrix), overall residual-risk method.
2. **Analysis:** intended use and foreseeable misuse; hazards; sequences of events; P1 (occurrence of hazardous situation) × P2 (leading to harm). Tools: PHA, FTA, design/process FMEA, URRA (see engineering-technology.biomedical-engineering.medical-device-design.usability-engineering-iec-62366).
3. **Evaluation** against the plan's criteria.
4. **Control** in priority order: inherent safety by design → protective measures → information for safety. Information alone needs justification.
5. **Verify** each control is implemented and effective; check for new hazards introduced by controls.
6. **Residual risk:** evaluate each, then **overall residual risk** and benefit-risk where needed; disclose significant residual risks in labelling.
7. **Review and production/post-production:** complaints, trends and field data update the file.

## 5. V&V protocols and sample size

Protocol: objective, traced requirements, production-equivalent units (with rationale), worst-case configuration, pre-conditioning (ageing, transport, sterilisation), validated test method, **pre-defined acceptance criteria**, statistical method.

**Attribute data (pass/fail), success-run:** n = ln(1 − C) / ln(R) with zero failures.
- 95% C / 90% R → 29; 90/90 → 22; 95/95 → 59; 95/99 → 299.
Tie confidence/reliability to the severity of the harm the requirement protects against (a documented sampling procedure).

**Variable data:** one-sided normal tolerance interval: pass if x̄ − k·s ≥ LSL. For n = 30, k ≈ 2.22 (95/95) and ≈ 3.06 (95/99) (k values recomputed with the noncentral t distribution: 2.2198 and 3.0639; verify with ISO 16269-6 tables). Check normality first; otherwise transform or use non-parametric intervals.

**Test method validation:** gauge R&R (≤ 10% of tolerance good, 10-30% conditionally acceptable (gated: unconfirmed, source is paywalled or blocked)), accuracy, and resolution at least ~1/10 of tolerance (gated: unconfirmed, source is paywalled or blocked).

**Validation** (right device built?): simulated or actual use by intended users on production-equivalent devices, including summative usability and clinical evaluation where needed.

## Gotchas

- Verifying a risk control's implementation is not verifying its effectiveness (alarm exists vs users respond to it).
- A sample size of 3 "because that is standard" has no rationale; 3 lots for process validation is a different question.
- Late requirement changes without re-running impacted tests break the trace silently; run impact analysis per change.
- Probability estimates for software failures and use errors are unreliable; many teams use severity-only evaluation for those, with justification.
- Engineering-build test results cannot be claimed for production units without an equivalence rationale.

## Verify

- [ ] Every design input traces to a need/source and to at least one verification report.
- [ ] Every risk control traces to a requirement plus implementation and effectiveness evidence.
- [ ] Each protocol has pre-approved acceptance criteria and a documented sample-size rationale.
- [ ] Test methods are validated (gauge R&R) before formal V&V.
- [ ] Overall residual risk and benefit-risk conclusions are signed off per the plan.
- [ ] Trace matrix has no orphans in either direction.

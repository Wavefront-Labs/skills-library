---
id: engineering-technology.biomedical-engineering.device-verification-validation.risk-acceptability-criteria
name: risk-acceptability-criteria
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [risk-acceptability, iso-14971, risk-management, risk-matrix, risk-policy, benefit-risk, severity-scale, probability-scale]
level: advanced
status: gated
description: "Define risk acceptability criteria under ISO 14971: severity and probability scales, matrix design, acceptable regions, benefit-risk review and EU MDR risk wording."
sources: ["ISO 14971 Medical devices - Application of risk management to medical devices (confirm edition)", "ISO/TR 24971 Guidance on the application of ISO 14971 (confirm edition)", "Regulation (EU) 2017/745 Annex I general safety and performance requirements (risk reduction as far as possible; the Annex I wording could not be read from EUR-Lex in this review (gated: unconfirmed, source is paywalled or blocked))"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Risk acceptability criteria

**Goal:** a documented, justified policy that decides, for each risk, whether it is acceptable.

Regulatory expectations differ by market (for example EU MDR wording on risk reduction versus ISO 14971 text); confirm current standards, annexes and notified body expectations.

## Elements of the policy (set by top management)
1. **Severity scale:** defined levels with clinical descriptions, such as negligible (inconvenience), minor (temporary, no intervention), serious (requires medical intervention), critical (permanent impairment or life-threatening), catastrophic (death). Keep the descriptions specific to your device.
2. **Probability scale:** levels with numeric or semi-quantitative ranges (for example frequent, probable, occasional, remote, improbable) linked to events per use or per year; define the probability of occurrence of harm (probability of the hazardous situation multiplied by probability that it leads to harm).
3. **Matrix:** map severity and probability onto acceptable and not acceptable regions; many companies use three bands (acceptable, review/ALARP-style, unacceptable) with rules for each.
4. **Rules for use:** who may accept risk in each band (for example engineering for acceptable, risk review board for the middle, top management for exceptions); required evidence for each band.
5. **Overall residual risk and benefit-risk:** rules for evaluating residual risks together and against benefits (see benefit-risk-analysis).

## Practical advice
- Calibrate with historical complaints and published adverse event data so the probability scale means something.
- Do not use the matrix alone: ISO 14971 requires reducing risk as far as practicable by priority order of inherent safe design, protective measures and information for safety, and the EU MDR requires risk reduction as far as possible without adversely affecting the benefit-risk ratio.
- Document why a risk is accepted even if the matrix says acceptable when severity is high and the risk could be further reduced.
- Apply the same criteria to use errors, software and cybersecurity.
- Review the policy in management review and after field data.

## Gotchas
- Different matrices per product line without justification.
- Probability estimates with false precision; document uncertainty.
- Accepting risk because mitigation is expensive, which is not an acceptable justification alone.

## Verify
- [ ] Policy approved, versioned and referenced from the risk management plan.
- [ ] Each risk decision references the criteria applied.
- [ ] Policy reviewed after post-market data (for example complaints).

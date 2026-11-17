---
id: computing-software.it-governance-risk-compliance.nist-csf-800-53.nist80053b-baselines-tailoring
name: nist80053b-baselines-tailoring
category: computing-software
field: it-governance-risk-compliance
product: nist-csf-800-53
tags:
- nist-csf-800-53
- nist80053b-baselines-tailoring
- sp80053-baselines
level: practitioner
status: draft
description: Select Low, Moderate or High control baselines from SP 800-53B, tailor with scoping, parameters, compensating controls and overlays.
sources:
- https://www.nist.gov/cyberframework
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/37/r2/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Baselines, tailoring and overlays (800-53B)
**Goal:** a defensible control set per system.
- Categorize system impact (low, moderate, high) per FIPS 199 for confidentiality, integrity, availability; take the high-water mark; FIPS 200 sets minimum security requirements.
- SP 800-53B provides the Low, Moderate, High baselines plus a privacy baseline.
- Tailor: identify and designate common controls, apply scoping, select compensating controls, assign parameter values, add supplements.
- Overlays (e.g. FedRAMP baselines) capture community-specific tailoring.

## Gotchas
- Tailoring needs a documented rationale or it reads as omission.

## Self-check
For five removed or modified controls show the rationale and approver.

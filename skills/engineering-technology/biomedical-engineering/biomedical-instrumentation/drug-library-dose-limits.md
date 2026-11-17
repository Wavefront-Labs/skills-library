---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.drug-library-dose-limits
name: drug-library-dose-limits
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [drug-library, dose-error-reduction, infusion-safety, soft-limit, hard-limit]
level: advanced
status: draft
description: "Design and manage infusion pump drug libraries: dose error reduction software, hard and soft limits, care areas, library governance, updates and integration with records."
sources: ["ISMP guidelines for smart infusion pump safety and drug library practice (confirm current version)", "FDA Infusion Pump Improvement Initiative and premarket guidance (confirm current text)", "https://www.ismp.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Drug library and dose limits

**Goal:** use pump software to catch programming errors before they reach the patient.

## Concepts
- A **drug library** is a curated list of medications with concentration, units, default rates, and limits per clinical care area (adult ICU, paediatrics, oncology).
- **Soft limits** warn and can be overridden with confirmation; **hard limits** cannot be exceeded without changing the library, used for doses never appropriate.
- Dose error reduction software (DERS) performs the check at programming time.

## Design and governance
1. Interdisciplinary committee (pharmacy, nursing, physicians, biomedical engineering) defines entries and limits from approved references and local practice.
2. Standardise concentrations; avoid unit ambiguity (mg versus mcg, mL/h versus dose/time); display consistent names with tall-man lettering where appropriate.
3. Pump design: library versioning, integrity check (checksum), display of the library version, safe behaviour if the library is corrupt.
4. Update process: validation on pump (test each entry), controlled rollout, back-out plan.
5. Monitor: collect pump logs to see override rates, alert fatigue and near misses; update limits using the data.
6. Integration with electronic medication records adds a risk (interoperability); validate end to end.

## Verify
- [ ] Library entries and limits approved and tested on devices.
- [ ] Version control and integrity checks functioning.
- [ ] Override and alert data reviewed on a schedule.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.

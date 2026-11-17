---
id: engineering-technology.biomedical-engineering.medical-device-design.ml-enabled-device-lifecycle
name: ml-enabled-device-lifecycle
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [ml-enabled-device, ai-medical-device, machine-learning, pccp, gmlp]
level: advanced
status: verified
description: "Manage the lifecycle of an AI or ML enabled medical device: data governance, locked versus adaptive models, validation, bias, change control plans and post-market monitoring."
sources: ["https://www.fda.gov/media/166704/download"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AI and ML enabled device lifecycle

**Goal:** treat the model as safety-relevant software with data as a controlled design input.

## Lifecycle practice
- **Intended use and users first:** performance claims depend on the population and workflow; define them before data collection.
- **Data management:** provenance, labelling quality and reference standard, representativeness (age, sex, ethnicity, device and site variety), and strict separation of training, tuning and test sets (no leakage by patient or site).
- **Model design and validation:** report performance with confidence intervals and by subgroup; test robustness to input shifts; clinical validation in the intended use setting.
- **Locked versus adaptive:** a locked model changes only through a controlled release. Planned post-market modifications require a predetermined change control plan agreed with the regulator where available; in the US see FDA's final guidance 'Marketing Submission Recommendations for a Predetermined Change Control Plan for AI-Enabled Device Software Functions' (issued December 2024, reissued 18 August 2025, read from the PDF). Confirm the current guidance and the jurisdiction.
- **Software lifecycle:** IEC 62304 and risk management still apply; add model version, training data version and validation traceability to configuration management.
- **Monitoring:** drift, failure reports, subgroup performance, user feedback; define triggers for retraining or withdrawal.
- **Transparency:** labelling states the data, performance, limitations and human-oversight expectation.
- EU: the AI Act adds obligations for high-risk AI in medical devices alongside MDR; confirm applicability dates and notified body expectations.

## Verify
- [ ] Test data independent of training data and representative.
- [ ] Subgroup performance reported and risks assessed.
- [ ] Change management and monitoring plan documented.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.

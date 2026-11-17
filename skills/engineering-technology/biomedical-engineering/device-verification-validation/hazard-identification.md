---
id: engineering-technology.biomedical-engineering.device-verification-validation.hazard-identification
name: hazard-identification
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [hazard-identification, iso-14971, risk-management, hazardous-situation, foreseeable-misuse, preliminary-hazard-analysis, harm]
level: practitioner
status: draft
description: "Identify hazards, sequences of events and hazardous situations per ISO 14971: characteristics, foreseeable misuse, energy and information hazards, and recording harm."
sources: ["ISO 14971 Medical devices - Application of risk management to medical devices (confirm edition, 2019 current at time of writing)", "ISO/TR 24971 Guidance on the application of ISO 14971 (confirm edition)", "Vincoli, Basic Guide to System Safety"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Hazard identification

**Goal:** a complete, structured list of hazards, how they can lead to harm and in what circumstances.

## Terms (ISO 14971)
- **Hazard:** potential source of harm.
- **Sequence of events** leading to a hazardous situation.
- **Hazardous situation:** circumstance in which people are exposed to a hazard.
- **Harm:** injury or damage to health.
- Risk combines probability of occurrence of harm and severity.

## Steps
1. **Intended use and reasonably foreseeable misuse:** user, patient, environment, duration of use, and likely misuse (wrong connection, reuse of single-use device).
2. **Characteristics related to safety:** go through a checklist (the guidance document has questions): energy delivered, substances in contact with the body, sterility, software, accuracy, shelf life, packaging, disposal, interactions with other devices.
3. **Hazard categories:** energy (electrical, thermal, mechanical, radiation), biological and chemical (toxic, infection, allergenic), information (labelling, instructions, display errors), operational (use error, loss of function, unclear alarm), environmental (EMC, temperature).
4. **Methods:** preliminary hazard analysis early; FMEA on components and processes (see fmea-design-process); fault tree for top-level hazards (see fault-tree-analysis); use-related hazard analysis with task analysis; analysis of complaints and similar devices (MAUDE, vigilance reports, recalls).
5. **Write sequences of events:** initiating cause, then event, then hazardous situation, then harm; include the probability of exposure and harm.
6. **Record** hazard, cause, hazardous situation, harm, severity; assign IDs for traceability.
7. **Update** through the life cycle (design changes, production, post-market data).

## Gotchas
- Listing failure modes without harm.
- Ignoring use error and software.
- Stopping at the first cause instead of considering combinations.

## Verify
- [ ] Each hazard has at least one hazardous situation and harm.
- [ ] Evidence of multiple methods and independent review.
- [ ] Complaint and recall data of similar products reviewed.

---
id: engineering-technology.biomedical-engineering.medical-device-design.software-safety-classification
name: software-safety-classification
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [software-safety-class, medical-device-software, samd, iec-62304, software-classification, software-item]
level: practitioner
status: gated
description: "Assign IEC 62304 software safety classes A B C from hazardous situations and external risk controls, decompose into items and set the process rigour that follows."
sources: ["IEC 62304 Medical device software - Software life cycle processes (Ed 1.0 2006 with Amendment 1 2015; confirm current edition)", "ISO 14971 Application of risk management to medical devices", "https://www.iec.ch"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IEC 62304 software safety classification

**Goal:** assign a safety class to the software system, and to items where justified, so the right level of process rigour is applied.

Practice guidance. Confirm which edition of IEC 62304 your regulator accepts; a second edition has been in development, so verify status rather than assume.

## The classes
- **Class A** (class definitions and the per-class process lists below are from IEC 62304 and (gated: unconfirmed, source is paywalled or blocked)): no injury or damage to health is possible from the software.
- **Class B:** injury is possible but not serious.
- **Class C:** death or serious injury is possible.

## How to classify
1. From the ISO 14971 risk analysis, list hazardous situations the software can contribute to.
2. For each, assess the severity of the harm after considering risk controls that are **outside** the software (hardware interlocks, independent alarms, clinician check).
3. Under the 2015 amendment, if the software can contribute to a hazardous situation, probability of software failure is treated as 100%, so classification is driven by severity; confirm this against the edition you apply.
4. The system takes the highest class of its contributing hazards.
5. **Decomposition:** you may assign lower classes to segregated software items if the architecture shows independence. Document the segregation rationale; items not shown to be segregated inherit the system class.

## What the class changes
- A requires the basic life cycle plan, requirements, release and configuration management.
- B adds architectural design and unit-level documentation, and integration and system testing evidence.
- C adds detailed design, unit verification criteria and more stringent verification.

## Gotchas
- Do not reduce class by arguing the software will not fail; rely on independent hardware or procedural controls.
- Reclassify when the intended use, risk file or architecture changes.
- SOUP inherits the class of the item that uses it (see soup-management).

## Verify
- [ ] Class and rationale in the risk file and software development plan.
- [ ] Segregation argument documented where classes differ.
- [ ] Review on every design change.

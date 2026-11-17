---
id: engineering-technology.biomedical-engineering.medical-device-design.software-development-plan
name: software-development-plan
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [software-development-plan, iec-62304, software-lifecycle, software-maintenance-plan, sdlc]
level: practitioner
status: gated
description: "Write a software development and maintenance plan to IEC 62304: lifecycle model, deliverables, configuration management, risk management, verification and problem resolution."
sources: ["IEC 62304 Medical device software - Software life cycle processes (confirm edition and amendment)", "FDA, Content of Premarket Submissions for Device Software Functions (final, June 2023; replaces the 2005 software-contained-in-devices guidance), https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-device-software-functions", "https://www.iec.ch"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Software development and maintenance plan

**Goal:** a plan that shows how software will be developed, verified, released and maintained in step with the software safety class.

## Contents (typical IEC 62304 planning content (gated: unconfirmed, source is paywalled or blocked))
- Lifecycle model and processes in use; scope by software safety class (A, B, C; see software-safety-classification).
- Deliverables per activity: requirements, architecture, detailed design (class C), unit and integration tests, system tests, release.
- Verification strategy, tools, and test environments; traceability from requirements to risk controls to tests.
- Configuration management: identification, change control, version numbering, build reproducibility.
- Software risk management activities tied to the ISO 14971 file; SOUP list and evaluation (see soup-management).
- Problem resolution and anomaly handling (see software-anomaly-management).
- Maintenance plan: feedback intake, change classification, regression testing, release and field update process.
- Responsibilities, staffing and standards used; cybersecurity activities (see device-cybersecurity).

## Practice
- Keep the plan living; update when class, architecture or tools change.
- Agile processes are acceptable if the required outputs and traceability exist.

## Verify
- [ ] Plan covers each IEC 62304 process required for the assigned class.
- [ ] Traceability tools and records defined.
- [ ] Plan approved and under document control.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.

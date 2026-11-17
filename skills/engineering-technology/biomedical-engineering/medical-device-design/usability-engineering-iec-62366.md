---
id: engineering-technology.biomedical-engineering.medical-device-design.usability-engineering-iec-62366
name: usability-engineering-iec-62366
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [usability-engineering, human-factors, iec-62366-1, iec-62366-2, urra, use-related-risk-analysis, use-specification, user-profile, hazard-related-use-scenario, critical-task, formative-evaluation, summative-evaluation, human-factors-validation, pca-analysis, task-analysis, uoup, iso-14971, fda-human-factors-guidance, reprocessing, ifu, use-error]
level: practitioner
status: gated
description: "Run IEC 62366-1 usability engineering: use specification, user profiles, URRA and hazard-related use scenarios, critical tasks, formative studies and a 15-per-group summative validation."
sources: ["IEC 62366-1:2015+AMD1:2020 Medical devices - Application of usability engineering to medical devices", "IEC TR 62366-2:2016 Guidance on the application of usability engineering", "FDA guidance: Applying Human Factors and Usability Engineering to Medical Devices (Feb 2016, revised 3 Aug 2026), https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices", "FDA final guidance: Content of Human Factors Information in Medical Device Marketing Submissions (May 2026; the 2022 draft is finalised)", "ISO 14971:2019 Medical devices - Application of risk management", "ANSI/AAMI HE75:2009/(R)2018 Human factors engineering - Design of medical devices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Usability engineering to IEC 62366-1 — design out use error and prove it

**Goal:** produce a usability engineering file that identifies use-related hazards early, shapes the user interface through formative work, and closes with a summative (HF validation) study that regulators accept.

This is engineering guidance, not a substitute for your QMS procedures, a qualified human-factors specialist or the current text of the standards and FDA guidance.

## 1. Use specification and user profiles

Write the **use specification** first (IEC 62366-1 cl. 5.1 (gated: unconfirmed, source is paywalled or blocked)): intended medical indication, patient population, body part/tissue, **user profiles**, **use environment** and operating principle. Each distinct user group needs its own profile: e.g. ICU nurse, lay patient with reduced dexterity, biomedical technician, reprocessing staff. Separate groups when training, physical/cognitive capability or tasks differ enough that performance could differ. Record environment factors (lighting, noise, gloves, PPE, interruptions, home vs. ambulance).

## 2. Task analysis and URRA

1. Decompose every task (set-up, use, alarms, maintenance, cleaning/reprocessing, disposal) into steps.
2. For each step apply **PCA** analysis: what must the user *perceive*, *understand* (cognition) and *do* (action)? Each is a failure point.
3. Mine **known use problems**: complaint files, FDA MAUDE, recalls, predicate devices.
4. Build the **URRA** (use-related risk analysis): step → potential use error → hazard → hazardous situation → harm → severity. Feed this into the ISO 14971 risk file (see engineering-technology.biomedical-engineering.device-verification-validation.design-controls-and-iso-14971-risk-traceability).
5. Extract **hazard-related use scenarios** (62366 term). FDA's **critical tasks** are those which, if performed incorrectly or not at all, would or could cause serious harm. Rate on severity, not on estimated probability: use-error probability is not reliably estimable, which is why validation, not a P-number, closes these risks.

Legacy interfaces may use the **UOUP** route (Annex C, user interface of unknown provenance (gated: unconfirmed, source is paywalled or blocked)) but only with post-market evidence and no unacceptable residual risk.

## 3. User interface specification and design

Write testable UI requirements tied to URRA lines: e.g. "connector shall be physically non-interchangeable with Luer", "dose confirmation requires two distinct actions". Apply the risk-control hierarchy: design out the error (forcing functions, keyed connectors), then protective measures (alarms, confirmations), then labelling/training last. HE75 gives detailed guidance (gated: unconfirmed, source is paywalled or blocked) on displays, alarms, connectors and labelling.

**Design-for-sterilisation note:** reprocessing is a use task. Lumens, hinges, mated surfaces and blind holes make cleaning error-prone; choose geometry and materials compatible with the intended method (steam, EtO, gamma/e-beam, VHP) early, and treat each IFU cleaning step as a task in the URRA. Validate that reprocessing staff can follow the IFU, not only that the process works in the lab.

## 4. Formative evaluation

Iterative, small-n (typically 5-8 per round (gated: unconfirmed, source is paywalled or blocked), not specified in the FDA guidance), any method: cognitive walkthrough, heuristic review, simulated-use with think-aloud. Purpose is to find problems, so change the design between rounds. Document findings and design changes; this evidence is what lets you argue the summative design is mature.

## 5. Summative (HF validation) evaluation

- Production-equivalent device, final IFU/labels, realistic simulated environment, representative users trained as real users would be (allow a realistic training decay interval: FDA says a break of an hour such as lunch is acceptable in some cases and a gap of one or more days is appropriate in others).
- **At least 15 participants per distinct user group** (FDA human factors guidance: "in general, the minimum number of participants should be 15", higher for some devices); this is a floor, not a statistical power calculation.
- Test **all critical tasks**; capture use errors, close calls and use difficulties by observation, then a root-cause debrief interview for each.
- Acceptance is qualitative: every use error on a critical task needs root-cause analysis and a residual-risk argument. If the cause is UI-related and risk is not acceptable, fix the design and re-test (at least the affected tasks).
- Knowledge tasks (e.g. understanding contraindications) are tested by questioning, not observation.

## Gotchas

- Summative is not a satisfaction survey. Pass rates or SUS scores do not substitute for root-cause analysis.
- Training participants beyond what real users get invalidates the study.
- Forgetting secondary users (cleaning staff, installers, caregivers) is the commonest gap in reviews.
- Labelling "warnings" as the only control for a critical task is weak and usually challenged.
- Changing the UI after summative usually needs a justified partial re-validation.
- IEC 62366-1 and FDA vocabulary differ (hazard-related use scenario vs critical task); map them explicitly in the file.

## Verify

- [ ] Use specification lists every user group, environment and the reprocessing/maintenance users.
- [ ] Every URRA line traces to a hazard in the ISO 14971 file and to a UI requirement or justification.
- [ ] Critical tasks are defined by severity and each appears in the summative protocol.
- [ ] Formative rounds are documented with resulting design changes.
- [ ] Summative used production-equivalent devices, realistic training, ≥15 users per distinct group.
- [ ] Every critical-task use error has a root cause and a residual-risk conclusion.

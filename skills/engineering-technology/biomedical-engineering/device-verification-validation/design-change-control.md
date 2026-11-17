---
id: engineering-technology.biomedical-engineering.device-verification-validation.design-change-control
name: design-change-control
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [design-change, design-controls, design-and-development-planning, change-control, engineering-change-order, impact-assessment, regulatory-change-assessment]
level: practitioner
status: verified
description: "Control design changes: request, impact assessment on risk and V&V, approval, implementation, regulatory impact check, effective date and records under ISO 13485."
sources: ["https://www.fda.gov/regulatory-information/search-fda-guidance-documents/deciding-when-submit-510k-change-existing-device", "ISO 13485 Medical devices - Quality management systems (control of design and development changes; confirm edition)", "FDA guidance Deciding When to Submit a 510(k) for a Change to an Existing Device (2017; confirm current)", "Regulation (EU) 2017/745 (significant change provisions and notified body notification; confirm current text)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Design change control

**Goal:** every design change is evaluated, verified, approved and traceable before it reaches the market.

## Workflow
1. **Change request:** a record describing the proposed change, reason (complaint, supplier, cost, improvement, regulatory), affected parts and documents.
2. **Impact assessment** by a cross-functional team:
   - **Design:** affects requirements, specification, interfaces, software or labelling?
   - **Risk:** new hazards, changed severity or probability, risk controls affected (update the risk file).
   - **Verification and validation:** which tests must be repeated (for example EMC after PCB change, biocompatibility after a material or process change, sterilisation validation after packaging change).
   - **Manufacturing and suppliers:** tools, process validation, incoming inspection, supplier approval.
   - **Regulatory:** does the change need a new submission or notification? In the US, assess against the FDA guidance for 510(k) changes (a new 510(k) may be needed for changes that could significantly affect safety or effectiveness); in the EU, the notified body must approve changes to an approved design or type under the MDR (check Annex VII and the notified body procedure for what counts as significant); other markets have their own rules.
   - **Clinical, usability, and software** impact.
3. **Approval** by the design authority and quality (and regulatory affairs when needed).
4. **Implementation plan:** tasks, owners, dates, effectivity (serial or lot cut-in, field retrofit, use-up or scrap of old stock).
5. **Verification and validation** results reviewed, with deviations dispositioned.
6. **Update documents:** drawings, bills of materials, specifications, work instructions, DHF or technical file, labelling, training.
7. **Closure:** confirm implementation, record effective date, trend change history, notify distributors where required.

## Gotchas
- Treating small supplier changes (resin, adhesive, plating) as non-design; they are changes.
- Not updating the risk file.
- Implementing the change before approval ("temporary" deviations).

## Verify
- [ ] Each change has a documented regulatory assessment (including the decision not to submit and why).
- [ ] V&V evidence matches the impact assessment.
- [ ] Effectivity recorded for traceability from device history to design version.

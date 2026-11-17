---
id: engineering-technology.biomedical-engineering.medical-device-design.design-transfer-to-production
name: design-transfer-to-production
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [design-transfer, manufacturing-transfer, device-master-record, process-validation, pilot-build]
level: practitioner
status: verified
description: "Plan design transfer: convert design outputs into production specifications, validate processes, train staff and control suppliers before commercial release."
sources: ["https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Design transfer to production

**Goal:** make sure the design can be built repeatedly to specification, and that production documents match verified design outputs.

## Steps
1. Define transfer scope and checklist: drawings and specifications, bill of materials, work instructions, inspection plans, labelling, packaging, test methods and equipment.
2. Review manufacturability: tolerance stacks, process capability (see process-capability), assembly steps with error-proofing.
3. Qualify suppliers and incoming inspection for critical components.
4. Run pilot builds with production tooling and operators; compare against verification builds; resolve differences.
5. Validate processes whose output cannot be fully verified (see process-validation-iq-oq-pq): sealing, sterilisation, welding, bonding, software installation.
6. Train operators; record qualification.
7. Final transfer review confirms readiness; the production record set is released under change control. (Under the US QMSR, 21 CFR Part 820 no longer has the device master record or design history file sections; 820.30 is reserved and 820.10 requires an ISO 13485 QMS, so use the ISO 13485 medical device file and clause 7.3 wording. eCFR checked 2026-10-19.)

## Traps
- Verification built on prototype tooling, then production tooling changes dimensions without re-verification.
- Transfer treated as a document hand-off; the process needs proven capability.

## Verify
- [ ] Each design output maps to a production specification.
- [ ] Process validation or verification complete for special processes.
- [ ] Residual open issues have owners and dates; release authorised.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.

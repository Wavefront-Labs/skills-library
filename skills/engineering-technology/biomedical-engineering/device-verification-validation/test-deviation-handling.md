---
id: engineering-technology.biomedical-engineering.device-verification-validation.test-deviation-handling
name: test-deviation-handling
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [test-deviation, protocol-deviation, verification-deviation, test-failure-investigation, ncr]
level: practitioner
status: draft
description: "Handle verification test deviations and failures: documentation, impact assessment, protocol amendment, retest rules, avoiding cherry-picking and linking to nonconformance."
sources: ["ISO 13485 control of nonconforming product and design verification clauses (confirm edition)", "Good documentation practice guidance (confirm company procedures)", "https://www.iso.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Test deviation handling

**Goal:** keep test records trustworthy when something does not go to plan.

## Types
- **Protocol deviation:** the test was run differently from the approved protocol (equipment, setting, sample, environment, step order).
- **Test failure:** a sample misses the acceptance criterion.
- **Anomaly:** unexpected result or equipment fault during the test.

## Process
1. Stop and record at the time: what happened, date, who, equipment and sample IDs; do not erase or overwrite data.
2. **Assess impact:** does the deviation affect validity of the result for this sample, for the protocol as a whole, or none? Obtain approval by a qualified reviewer (quality or technical lead).
3. For failures, **investigate** root cause (specimen, setup, method, true design failure) before any retest; open a nonconformance report and CAPA if the failure may represent the design or process.
4. **Retest rules:** a retest is allowed only when a documented assignable cause shows the first result invalid, and the retest plan is approved before running; do not keep testing until a pass; report original and retest results.
5. **Amend the protocol** by approved change before affected tests, not after; or write a deviation report that is attached to the final report.
6. In the report, list all deviations with impact assessment and conclusion.

## Traps
- Excluding a failed sample as an outlier without a documented cause.
- Retrospective protocol edits to fit what was done.

## Verify
- [ ] Every deviation has a record, impact assessment and approval.
- [ ] Failures traced to NCR or CAPA where appropriate.
- [ ] Final report discloses all deviations and retests.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.

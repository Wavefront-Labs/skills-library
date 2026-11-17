---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-policy-escalation
name: error-budget-policy-escalation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [policy-escalation-path, policy-disagreement, error-budget-policy, escalation, slo-governance]
level: practitioner
status: docs-checked
description: "Write the escalation clause of an error budget policy: a named arbiter for disputes about budget calculation or the agreed actions, per the Google SRE Workbook."
sources: ["https://sre.google/workbook/error-budget-policy/", "https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error budget policy escalation

The Workbook's example policy has a one-sentence escalation clause: "In the event of a disagreement between parties regarding the calculation of the error budget or the specific actions it defines, the issue should be escalated to the CTO to make a decision." The Workbook's guidance on policy contents asks for "a clear escalation path to follow if there is disagreement on the calculation or whether the agreed-upon actions are appropriate in the circumstances".

## Clause template (illustrative, not from the Workbook)
```
Escalation policy
Disputes about (a) the SLI calculation, (b) whether an incident counts against the budget, or
(c) whether the agreed actions (such as a release freeze) apply, are raised in writing.
1. The dev lead and SRE lead attempt resolution within <N business days>.
2. Unresolved -> <named role> decides within <N business days>.
3. The decision and rationale are recorded with the policy.
```
The deadlines and the choice of arbiter role are your decision; the Workbook example names the CTO and gives no deadlines.

## Disputes the example policy already settles
The Workbook example policy lists when the team must work on reliability: a code bug or procedural error caused the miss; a postmortem reveals an opportunity to soften a hard dependency; miscategorised errors failed to consume budget that would have caused an SLO miss. It lists when the team may continue feature work: a company-wide networking problem; a dependency owned by another team that has itself frozen releases; budget consumed by out-of-scope users (for example load tests or penetration testers); miscategorised errors consume budget though no users were impacted. Writing these cases into your policy removes most arguments before they reach escalation.

## Dependency-caused misses
The Workbook describes two schools of thought on a miss caused by another team's dependency, says the second approach (taking action even when the dependency is at fault) makes users happier, and says to record your decision in the documented policy.

## If stakeholders will not enforce the policy
The Workbook says that when a service exhausts its budget but not all stakeholders agree that enacting the policy is appropriate, return to the error budget policy approval stage.

## Running an escalation
- State the decision needed in one sentence.
- Bring the budget consumption data and the incident list with the share of budget each consumed (the Workbook uses "this outage consumed 30% of my quarterly error budget" style reporting).
- Record the outcome; repeated escalations on one topic suggest the policy needs revision.

## Verify
- [ ] The policy names who decides when parties disagree about the calculation or the actions.
- [ ] The policy document lists authors, reviewers, approvers, approval date and next review date, as the Workbook advises.

## Checked
Confirmed against the Workbook "Example Error Budget Policy" (escalation, SLO miss and background sections) and "Implementing SLOs" (policy documentation list, dependency schools of thought, return-to-approval advice). Removed: the 2 and 5 business day deadlines, the "default positions" table, and unsourced gotchas. The template is marked illustrative.
Method: docs-only read of cited pages, 2026-11-08

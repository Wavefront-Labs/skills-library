---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-outage-policy
name: error-budget-outage-policy
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [outage-policy, single-incident-budget-threshold, error-budget-policy, postmortem, slo]
level: practitioner
status: docs-checked
description: "Define the outage clause of an error budget policy: a single incident consuming more than 20% of the budget over four weeks triggers a postmortem with a P0 action item."
sources: ["https://sre.google/workbook/error-budget-policy/", "https://sre.google/workbook/postmortem-culture/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error budget outage policy (single-incident threshold)

The Workbook's example policy: "If a single incident consumes more than 20% of error budget over four
weeks, then the team must conduct a postmortem. The postmortem must contain at least one P0 action to
address the root cause." Also: a single *class* of outage consuming more than 20% of budget over a quarter
gets a P0 item on the team's quarterly plan.

## Writing the clause
```
Outage policy
- Any incident consuming more than 20% of the error budget over four weeks requires a postmortem with at
  least one P0 action item addressing the root cause.
- Any class of outage consuming more than 20% of the error budget over a quarter gets a P0 item on the
  team's quarterly planning document, to address it in the following quarter.
```

## Computing an incident's budget spend
Budget is a count of allowed bad events; an incident's share is its bad events divided by that count.
The Workbook's example: 1,000,000 requests in four weeks with a 99.9% availability SLO is a budget of 1,000
errors, so 340 failed requests spend 34%. For time-based SLOs: `incident_minutes / allowed_bad_minutes_in_window`.

Record the figure in the incident record and postmortem header.

## Why 20%
Five such incidents exhaust the budget, so each is individually significant. The 20% is the Workbook's
example; choose your own threshold with the policy's signatories.

## Gotchas
- Classify outage classes consistently (use the outage tracker tags, see `outage-tracking-and-tagging`) or
  the quarterly clause never fires.
- A P0 action item that is "monitor more" rarely addresses a root cause; reviewers should reject it.
- Count the full impact window from first bad event, not from detection.

## Checked

2026-11-01. Confirmed against the Workbook page Example Error Budget Policy (the 20% over four weeks postmortem
clause with a P0 action item, the 20% over a quarter outage-class clause, the 1,000,000 request example; P0 is the
highest priority bug). Removed: the 5 business day deadline, the PromQL query, the 10% and 30% tuning figures and
the claim that the clauses apply regardless of exhaustion.
Method: documentation only; no commands were run.

## Verify
- [ ] Budget-consumed figure computed for the last 3 incidents and recorded.
- [ ] Each incident over the threshold has a postmortem with a P0 item and owner.

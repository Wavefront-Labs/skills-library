---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-exceptions-and-silver-bullets
name: error-budget-exceptions-and-silver-bullets
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [error-budget, exceptions, release-freeze, slo-governance, sre]
level: practitioner
status: docs-checked
description: "Define what may proceed during an error-budget freeze, using the Google SRE Workbook's example policy exceptions and change-freeze guidance."
sources: ["https://sre.google/workbook/error-budget-policy/", "https://sre.google/workbook/implementing-slos/", "https://sre.google/sre-book/embracing-risk/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error budget exceptions

A freeze with no stated exceptions is hard to enforce. Write the exceptions into the policy rather than negotiating them mid-incident.

## What the Workbook's example policy allows
When the service has exceeded its error budget for the preceding four-week window, it halts all changes and releases "other than P0 issues or security fixes" until the service is back within its SLO. The policy's non-goals say halting change is undesirable and the policy "gives teams permission to focus exclusively on reliability".

The example also lists when the team may continue feature work despite a miss:
- the outage was caused by a company-wide networking problem;
- the outage was caused by a service maintained by another team that has itself frozen releases;
- the budget was consumed by users out of scope for the SLO (for example load tests or penetration testers);
- miscategorised errors consumed budget although no users were impacted.

And when the team must work on reliability: a code bug or procedural error caused the miss; a postmortem reveals a chance to soften a hard dependency; miscategorised errors failed to consume budget that would have caused a miss.

The appendix footnote defines P0 as the highest priority of bug: all hands on deck, drop everything else.

## Emergencies
The Workbook says a team can declare an emergency, with high-level approval, to deprioritise all external demands until the service meets exit criteria, typically within SLO plus steps to reduce the chance of a repeat (improved monitoring or testing, removing dangerous dependencies, rearchitecting).

## Freeze scope
The Workbook says the production freeze "halts certain changes", so decide which change types the freeze covers and record that. Dependencies: the Workbook favours freezing even when another team's dependency caused the miss, but accepts that freezing may be impractical and says to record the decision.

## Disputes
If stakeholders disagree that the policy should be enacted, the Workbook says to return to the policy approval stage; the example policy escalates calculation and action disputes to the CTO.

## Not in the sources
The SRE Book "Embracing Risk" chapter does not describe a "silver bullet" quota in the text read for this review, so no such mechanism is described here. If you design a scarce-exception scheme, treat quotas, approvals and pipeline enforcement as your own design choices and write them into the policy.

## Verify
- [ ] The policy lists changes that proceed during a freeze and the cases where feature work may continue.
- [ ] Each use of an exception is recorded and reviewed.

## Checked
Confirmed against the Workbook "Example Error Budget Policy" (SLO miss policy, non-goals, P0 footnote) and "Implementing SLOs" (emergency, freeze, dependency, return-to-approval text), and the SRE Book "Embracing Risk" (searched for silver bullets: not present). Removed: the silver-bullet quota, CI pipeline bypass YAML, quarterly exception counts and the retroactive-exceptions gotcha.
Method: docs-only read of cited pages, 2026-11-08

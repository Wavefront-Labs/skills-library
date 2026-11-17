---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-incident-review
name: cost-incident-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-anomaly-detection, cost-incident-review, cost-postmortem, blameless-review, preventive-controls]
level: practitioner
status: docs-checked
description: "Run a blameless review after a large cost anomaly: set triggers in advance, document impact and root cause, track preventive actions."
sources: ["https://www.finops.org/framework/capabilities/anomaly-management/", "https://sre.google/sre-book/postmortem-culture/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost incident review

Treat large unexpected spend like an outage: it has a cause, a detection gap and a fix.

## Frame it
- The FinOps Framework defines anomalies as levels of spending that differ (usually higher)
  from normal historical or expected spend. Resolving one usually involves investigation and
  then a change to the environment, a change to the expected cost of the affected scope, or
  simply acknowledging the anomaly and documenting why it was detected. Anticipated launches
  can trigger alerts too, so teams should document those rather than let other personas
  chase them.
- The Framework lists "analysis results in full root cause analysis post-mortem where
  appropriate" among the practices of a mature anomaly process.
- SRE guidance defines a postmortem as a written record of an incident, its impact, the
  actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to
  prevent recurrence.

## Trigger
Define postmortem criteria before an incident occurs so everyone knows when one is needed;
any stakeholder may also request one. The SRE book's examples of triggers are availability
and data-loss events; for cost, agree a spend or percentage-of-budget threshold with the
stakeholders (the Framework has teams establish anomalous percentage thresholds that
trigger action, set differently per persona).

## Template
1. **Summary**: what happened, cost impact, duration.
2. **Timeline**: change made, spend started, detected (by what), mitigated, resolved.
3. **Detection gap**: time from start to detection, and why earlier signals did not fire.
   Detection that works from billing data a week late, or only on budget alerts, is the
   least mature end of the Framework's scale.
4. **Contributing causes**: write blamelessly. Assume everyone acted with good intentions
   on the information they had, and look for systemic reasons they had incomplete or
   incorrect information.
5. **Actions**: preventive and detective actions, each with an owner.

## Review and share
Share the first draft internally and have senior engineers assess it. The SRE book's
review questions: was key incident data collected, are impact assessments complete, was the
root cause sufficiently deep, is the action plan appropriate and prioritised, and was the
outcome shared with stakeholders. Store finished reviews in a repository of past incidents
so others can learn from them.

## Verify
- [ ] Action items tracked to completion.
- [ ] The review is added to the shared repository of past incidents.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Framework Anomaly Management page and the SRE book "Postmortem Culture" chapter (both downloaded and read around the cited passages).
Removed as unconfirmed by the pages read: example trigger values ($10k, 20% of monthly budget), security-driven-spend trigger, UTC timeline, provider billing-adjustment/credit section and the claim that providers sometimes grant credits, "do not include in forecasts" advice, tagging reviews by cause category.

---
id: computing-software.systems-network-administration.patch-management.change-success-and-failure-rate-metrics
name: change-success-and-failure-rate-metrics
category: computing-software
field: systems-network-administration
product: patch-management
tags: [change-success-rate, change-failure-rate, change-enablement, dora-metrics, post-implementation-review, itil]
level: practitioner
status: draft
description: "Measure change enablement properly: change success and failure rates, what counts as failed, emergency change ratio, lead time, and using the numbers to adjust approval levels."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
  - https://dora.dev/guides/dora-metrics-four-keys/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change success and failure metrics

## Definitions
- **Failed change**: a change that caused an incident, was backed out, or needed remediation
  (hotfix, follow-up emergency change). Not just "implementation failed to complete".
- **Change success rate** = successful changes / implemented changes, per change model
  and per team. ITIL uses it to justify moving change types to standard/pre-authorised.
- **Change failure rate** (DORA) = deployments causing degraded service needing remediation
  / total deployments.
- **Emergency change ratio** = emergency / total; high values signal poor planning or a
  bypass culture.
- **Change lead time**: request to implementation (for normal changes), separate approval
  wait time.
- **Unauthorised changes**: detected changes without a record (from drift/config
  monitoring).

## Data capture
At closure every change records outcome: Successful / Successful with issues / Failed
(backed out) / Failed (caused incident). Link incidents to the causing change (incident
"caused by change" field) so failures are counted even when the implementer marked success.

## Using the numbers
| Signal | Action |
|---|---|
| Change model ≥ 98% success over 6 months, low impact | propose as **standard change** (pre-approved) |
| Team/model failure rate rising | require peer review, better testing, smaller batches |
| High emergency ratio | review planning, maintenance windows, patch cadence |
| Long approval waits with high success | delegate authority closer to teams |
Patch changes are a good candidate for standard change models once rings + automated tests
exist.

## Reporting
Monthly by team and model: volume, success %, failure % with linked incidents, emergency %,
median lead time; trend over quarters. Review in the change/CAB meeting.

## Gotchas
- Self-reported outcomes understate failure: reconcile with incident links.
- Counting a big release as one change hides risk; count deployable units.

## Verify
Every closed change has an outcome; failures reconcile with incidents; at least one
change model promoted or demoted per year based on data.

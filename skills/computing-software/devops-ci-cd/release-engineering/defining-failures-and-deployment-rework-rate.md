---
id: computing-software.devops-ci-cd.release-engineering.defining-failures-and-deployment-rework-rate
name: defining-failures-and-deployment-rework-rate
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, deployment-rework-rate, change-failure-rate, four-keys]
level: practitioner
status: docs-checked
description: "Define what counts as a failed deployment for change failure rate, and measure the newer deployment rework rate (unplanned deploys fixing production issues)."
sources: ["https://dora.dev/guides/dora-metrics-four-keys/", "https://dora.dev/research/2024/dora-report/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining failures and deployment rework rate

## Change failure rate needs a definition
A deployment "fails" if it causes degraded service requiring remediation: rollback, hotfix, fix-forward,
patch, or an incident linked to the change. Write it down per organisation, e.g.:
- Counted: rollback, revert PR deployed, incident with the deployment as cause, hotfix within 24 h for a regression.
- Not counted: failed pipeline before production, a deploy blocked by a gate, unrelated incidents.

Data linkage:
- Deployment events with commit SHA and service.
- Incidents with `caused_by_deployment` (id/SHA) filled at triage or postmortem.
- Revert detection: commits whose message starts with `Revert "` or PRs labelled `rollback`/`hotfix`.

`CFR = failed deployments / total deployments` per service per period.

## Deployment rework rate
DORA's metrics guide defines **deployment rework rate** as the ratio of deployments that are unplanned but happen as a result of an incident in production. Measure by labelling deployments (PR label such as `hotfix`, or
deploys from a hotfix branch):
`rework rate = unplanned fix deployments / total deployments`.
It complements CFR: teams that fix-forward quickly may show low rollbacks but high rework.

## Pitfalls
- Teams avoid declaring incidents to keep CFR low; reward honest reporting.
- Tiny denominators (few deploys) make percentages noisy; show counts too.

## Verify
- [ ] Definitions documented; dashboard shows CFR and rework rate with counts per service per month.

## Checked

2026-10-28. Confirmed against the DORA metrics guide: deployment rework rate is the ratio of deployments that are unplanned but happen as a result of an incident in production. Corrected: the skill described it as unplanned deploys fixing a user-facing bug and tied it to the 2024 report; the guide wording is used and the report attribution removed (not shown on the fetched report page).

Method: documentation only; no commands were run.

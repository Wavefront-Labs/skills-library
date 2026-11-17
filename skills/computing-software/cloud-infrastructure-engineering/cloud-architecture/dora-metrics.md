---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dora-metrics
name: dora-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, dora-metrics, four-keys, deployment-frequency, lead-time-for-changes, change-failure-rate, failed-deployment-recovery-time]
level: practitioner
status: draft
description: "Measure delivery performance with DORA metrics: definitions, data sources (VCS, CI/CD, incidents), automation, benchmarks and using them for improvement, not ranking."
sources: ["https://dora.dev/guides/dora-metrics-four-keys/", "https://github.com/dora-team/fourkeys", "https://cloud.google.com/devops/state-of-devops"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Delivery performance metrics (DORA)

## Metrics
| Metric | Definition | Source |
|---|---|---|
| Deployment frequency | How often changes deploy to production | CD system |
| Lead time for changes | Commit to running in production | VCS + CD timestamps |
| Change failure rate | % of deployments causing failure needing remediation | Deploy + incident/rollback records |
| Failed deployment recovery time | Time to restore after a failed deployment | Incident tooling |
| (Rework rate - added in recent DORA reports) | Unplanned deployments to fix user-facing issues | Deploy records |

## Implementation
1. Emit deployment events (service, commit SHAs, environment, time, result) from pipelines.
2. Link incidents/rollbacks to the deployment that caused them (tag in incident tool).
3. Compute per service/team weekly; median lead time; show trends (Four Keys project or
   platform tooling like DX/LinearB/GitLab Value Stream).
4. Compare to DORA benchmark clusters for context.
5. Review in team retrospectives; pick one constraint to improve (batch size, test time, approvals).

## Gotchas
- Gaming (splitting deploys) when metrics are targets; use them as diagnostics.
- Comparing teams with different contexts.
- Missing failure linkage makes change failure rate meaningless.

## Verify
- [ ] Metrics computed automatically from systems, not self-reported.

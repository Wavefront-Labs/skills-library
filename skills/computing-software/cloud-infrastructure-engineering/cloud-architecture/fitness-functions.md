---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.fitness-functions
name: fitness-functions
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-change-management, togaf, fitness-functions, evolutionary-architecture, architecture-tests]
level: advanced
status: draft
description: "Define architecture fitness functions that run in CI or production to guard quality attributes: dependency rules, latency, cost, security and policy checks."
sources: ["https://www.thoughtworks.com/insights/articles/fitness-function-driven-development", "https://www.archunit.org/", "https://www.openpolicyagent.org/docs/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture fitness functions

From Building Evolutionary Architectures (Ford, Parsons, Kua): a fitness function is an
objective, automated check of an architectural characteristic. It turns principles into tests.

## Examples by characteristic
| Characteristic | Fitness function |
|---|---|
| modularity | ArchUnit / dependency-cruiser rule: domain packages do not import infrastructure |
| security | OPA/Conftest or Checkov on Terraform plan: no public buckets, CMK required |
| performance | k6 test in CI fails if p95 > budget |
| cost | Infracost diff fails PR if monthly delta > threshold without label |
| resilience | scheduled chaos experiment; alert if steady-state hypothesis fails |
| operability | every service exposes health endpoint and SLO (catalogue check) |
| currency | dependency age or end-of-life check fails build within 90 days of EOL |

## Steps
1. Pick the 3-5 characteristics that matter most (from NFRs).
2. Write each as a check with a clear threshold and owner; triggered (CI) or continuous (production).
3. Start in warn mode, fix existing violations, then enforce.
4. Review thresholds quarterly; delete functions that never fire or are always overridden.

## Gotchas
- Flaky performance tests get disabled; run them on stable environments and compare trends.
- Too many gates slow delivery; keep holistic checks scheduled rather than per commit.

## Verify
- [ ] Each fitness function has owner, threshold and run history.
- [ ] Violations are visible on a dashboard.

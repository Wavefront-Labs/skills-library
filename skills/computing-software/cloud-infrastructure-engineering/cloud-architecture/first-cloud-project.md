---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.first-cloud-project
name: first-cloud-project
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, first-cloud-project, pilot-workload, caf-strategy, adoption-pilot, quick-win]
level: practitioner
status: draft
description: "Select the first cloud adoption project: business value, low dependency and risk, visible outcome, team learning, and criteria that make it a credible template for later waves."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/first-adoption-project", "https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-readiness/welcome.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Selecting the first adoption project

## Criteria
| Criterion | Good first project |
|---|---|
| Business value | Real users and outcome, not a throwaway demo |
| Dependencies | Few integrations; no tight coupling to on-prem databases over latency |
| Data | Non-sensitive or well-understood classification |
| Criticality | Not tier-0; tolerable if go-live slips |
| Team | Motivated owners, available SMEs |
| Learning | Exercises landing zone, identity, network, CI/CD, monitoring, cost tags |
| Duration | Production in weeks to ~3 months |

## Steps
1. Shortlist 5-10 candidates from the portfolio discovery.
2. Score on the criteria; discard anything blocked by unfinished foundations.
3. Confirm the landing-zone minimums are ready (identity, network, logging, policy, budgets).
4. Define success measures (deployed, KPI moved, lessons recorded).
5. Run it as the template: capture runbooks, IaC, migration checklist for subsequent waves.

## Gotchas
- Choosing the hardest system "to prove cloud can do it" - stalls the programme.
- Choosing something so trivial it teaches nothing (static site already on a CDN).

## Verify
- [ ] Scored shortlist with rationale.
- [ ] Retrospective outputs fed into the migration factory playbook.

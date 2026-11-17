---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.iac-maturity-assessment-and-adoption-roadmap
name: iac-maturity-assessment-and-adoption-roadmap
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, iac-maturity, adoption-roadmap, platform-engineering, dora-metrics, change-management, coverage-metrics]
level: sme
status: draft
description: "Assess an organisation's IaC maturity across coverage, workflow, testing, security and operations, then build a staged adoption roadmap with measurable exit criteria per stage."
sources: ["Kief Morris - Infrastructure as Code, 2nd/3rd edition (O'Reilly): core practices and adoption", "DORA - Accelerate State of DevOps reports and capabilities catalogue (https://dora.dev/capabilities/)", "AWS Well-Architected Framework - Operational Excellence pillar: perform operations as code"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IaC maturity assessment and adoption roadmap

Goal: replace "we should do more IaC" with a scored baseline, a staged plan, and numbers that show
progress to leadership.

## 1. Assess (score each 0–4)
| Dimension | 0 | 2 | 4 |
|---|---|---|---|
| **Coverage** | Console/manual | New resources in code, legacy manual | ≥95% of resources in code, imports done |
| **Workflow** | Local applies | PRs + CI plan, manual apply | PR → plan → approval → automated apply, no human creds in prod |
| **State & drift** | Local state | Remote locked state | Scheduled drift detection with alerts and owners |
| **Testing** | None | Lint/validate | Policy as code, unit/integration tests, ephemeral environments |
| **Security** | Secrets in code | Secret scanning | Secret manager refs only, least-privilege pipeline roles, signed artifacts |
| **Reuse** | Copy-paste | Shared modules | Versioned module catalogue with owners and upgrade automation |
| **Operations** | Manual DR | Runbooks | Rebuild-from-code tested; game days |
Gather evidence, not opinions: cloud inventory vs state (coverage %), CI logs (who applies),
audit logs (console changes per week), drift reports.

## 2. Baseline metrics
- **IaC coverage %** = resources tracked in state / resources in cloud inventory (AWS Config, Azure Resource Graph, GCP Asset Inventory).
- **Click-ops rate** = console/API changes by humans per week (CloudTrail/Activity log, excluding pipeline roles).
- **Lead time** for an infra change (PR open → applied) and **change failure rate** (DORA).
- **Drift MTTR**: time from detected drift to resolved.

## 3. Roadmap in stages (each with exit criteria)
1. **Foundation** (1–2 months): remote state with locking, repo layout, CI plan on PR, secret scanning. *Exit:* no local state; every change has a PR.
2. **Automation**: pipeline applies with OIDC/role creds; humans lose write in prod (break-glass only). *Exit:* click-ops rate near zero outside break-glass.
3. **Coverage**: brownfield import programme by criticality (network, IAM, data first). *Exit:* coverage ≥ 90% in prod.
4. **Guardrails**: policy as code, tagging enforcement, cost estimates in PRs, drift detection. *Exit:* policy violations blocked pre-merge; drift MTTR < 1 week.
5. **Self-service**: module catalogue, golden paths, templates (Backstage/AAP surveys). *Exit:* product teams ship infra without platform tickets.
6. **Resilience**: DR rebuild tests, game days. *Exit:* successful timed rebuild of a prod-like environment.

## 4. Run it
- Pick one pilot team/service per stage; publish the before/after metrics.
- Remove the old path when the new one works (revoke console write) — adoption stalls when both stay open.
- Re-score quarterly.

## Gotchas
- Measuring "lines of IaC" or "number of modules" rewards the wrong thing; measure coverage and click-ops.
- Big-bang mandates without import tooling or training produce shadow resources.
- Locking humans out before break-glass exists creates outages during incidents.

## Verify
- [ ] Assessment scorecard with evidence links exists and is dated.
- [ ] Each roadmap stage has an owner, exit metric and target date; metrics are reported monthly.

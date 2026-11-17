---
id: computing-software.systems-network-administration.patch-management.patch-kpis-versus-kris
name: patch-kpis-versus-kris
category: computing-software
field: systems-network-administration
product: patch-management
tags: [key-risk-indicator, kpi, kri, patch-metrics, risk-appetite, patch-management]
level: practitioner
status: draft
description: "Separate patching KPIs (process performance) from KRIs (risk exposure): choose each, set thresholds tied to risk appetite, and present both to IT and risk committees."
sources:
  - https://csrc.nist.gov/pubs/sp/800/55/v1/final
  - https://csrc.nist.gov/pubs/ir/8286/final
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# KPIs vs KRIs for patching

- **KPI** (key performance indicator): how well the patch process runs. Audience: IT operations.
- **KRI** (key risk indicator): how much exposure the organisation currently carries, against a risk appetite. Audience: risk committee, board.

A team can hit every KPI (95% success per wave) while KRIs are red (internet-facing KEV unpatched on the 5% that failed).

## Example KPIs
- Deployment success rate per wave (target >= 95%).
- Mean time to patch by severity (critical <= 14 days).
- Client health / reach (>= 98%).
- Change success rate for patch changes.
- Test cycle duration.

## Example KRIs (with thresholds)
| KRI | Green | Amber | Red |
|---|---|---|---|
| Internet-facing assets with KEV older than 7 days | 0 | 1-2 | >2 |
| Critical vulnerabilities older than SLA on tier-1 assets | <5 | 5-20 | >20 |
| % of assets on EOL OS | <1% | 1-3% | >3% |
| Accepted-risk exceptions on criticals older than 90 days | 0 | 1-5 | >5 |
| Unmanaged assets discovered (not in patch tool) | <0.5% | 0.5-2% | >2% |
Thresholds come from the documented risk appetite statement; amber/red trigger defined actions (escalation, budget, freeze).

## Presenting
- Ops dashboard: KPIs weekly with drill-down.
- Risk report: 4-6 KRIs monthly, trend arrows, narrative for anything red, owner and date.
- Link KRI breaches to risk register entries.

## Gotchas
- Using averages as KRIs hides the tail; KRIs should count exposures that matter.
- Too many KRIs dilutes attention; keep them few and stable.

## Verify
Each KRI has a defined query, threshold source (appetite statement) and owner; the committee minutes show actions on red KRIs.

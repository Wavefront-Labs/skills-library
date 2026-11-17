---
id: computing-software.cloud-infrastructure-engineering.azure.landing-zone-review-and-governance-maturity
name: landing-zone-review-and-governance-maturity
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, landing-zone, landing-zone-review, governance-benchmark, design-areas, caf, azure-review-checklist]
level: advanced
status: draft
description: "Review an existing Azure landing zone against the eight CAF design areas with the ALZ review checklist and governance benchmark, score gaps and produce a remediation backlog."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-areas", "https://github.com/Azure/review-checklists", "https://learn.microsoft.com/assessments/21765fd5-6e3b-4b30-8ed1-fd0d5aa4c8a2/", "https://learn.microsoft.com/azure/cloud-adoption-framework/govern/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Landing zone review and governance maturity

**Goal:** an evidence-based assessment of an existing Azure estate against CAF, with a prioritised
backlog the platform team can execute — not a slide of opinions.

## 1. Inputs
- Reader at the tenant root MG (plus Security Reader, Billing Reader).
- Microsoft Learn **Azure Landing Zone Review** assessment (online questionnaire) and the
  **ALZ checklist** from `Azure/review-checklists` (Excel or the `checklist_graph.py` automation).
- Interviews: platform, network, security, finance, 2–3 app teams.

## 2. The eight design areas
| Area | Evidence to collect |
|---|---|
| Azure billing & Entra tenant | EA/MCA structure, tenant count, break-glass accounts |
| Identity & access | PIM coverage, Owner count per sub, CA policies for admins |
| Resource organisation | MG tree, subscription per workload?, naming/tag compliance |
| Network topology & connectivity | hub-spoke/vWAN, IP plan overlap, private DNS centralisation |
| Security | Defender plans, secure score, Sentinel, key management |
| Management | central LAW, diagnostic coverage, Update Manager, backup coverage |
| Governance | policy assignments per MG, exemptions with expiry, cost budgets |
| Platform automation & DevOps | IaC coverage, pipelines with OIDC, subscription vending |

## 3. Automate the evidence
```bash
# checklist queries against live tenant (review-checklists repo)
python3 ./scripts/checklist_graph.py --checklist-file=./checklists/alz_checklist.en.json \
  --technology alz --output-file alz_results.json
```
ARG spot checks:
```kusto
resourcecontainers | where type == "microsoft.resources/subscriptions"
| join kind=leftouter (resourcecontainers | where type =~ "microsoft.management/managementgroups" | project mg=name) on $left.properties.managementGroupAncestorsChain[0].name == $right.mg
| project subscriptionName=name, parentMg=tostring(properties.managementGroupAncestorsChain[0].displayName)
```

## 4. Score and report
- Per checklist item: Fulfilled / Open / Not required / N/A, severity High/Medium/Low (from checklist).
- Maturity per area 1–5 (ad hoc → optimised). Present a heat map, not 300 rows.
- Backlog: High-severity Open items first, grouped into epics (e.g. "Centralise private DNS"), each with owner and target date.

## 5. Re-run
Quarterly with the same checklist version; trend the % fulfilled per area.

## Gotchas
- Checklist items marked "Not required" must have a written reason, or the next reviewer re-opens them.
- Brownfield: refactoring the MG tree is disruptive (policy re-evaluation, RBAC inheritance) — plan it as a migration with a canary subscription.
- Don't score from interviews alone; every "yes" needs a query result or screenshot.

## Verify
- [ ] Results file stored with date and checklist version.
- [ ] Every High-severity open item has an owner and a backlog ID.
- [ ] Next review date scheduled.

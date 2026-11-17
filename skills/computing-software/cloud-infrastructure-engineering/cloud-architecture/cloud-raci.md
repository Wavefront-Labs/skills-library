---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-raci
name: cloud-raci
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, cloud-raci, organisational-alignment, caf-organize, cloud-roles, responsibility-matrix]
level: intro
status: docs-checked
description: "Build a cross-team cloud RACI using the Cloud Adoption Framework capability columns, with one accountable team per function, for each team structure."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/organize/raci-alignment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organisational alignment and cloud RACI

Based on the Cloud Adoption Framework "RACI alignment" article: a cross-team matrix of responsible, accountable,
consulted and informed parties.

## Constructs used
- Accountable: the one team accountable for a function.
- Responsible: teams responsible for the outcomes.
- Consulted: teams consulted during planning.
- Informed: teams informed when work is completed.

## Capability columns (the article's tables)
Solution delivery, business alignment, change management, solution operations, governance, platform maturity,
platform operations, platform automation.

## Team structures with example matrices
Cloud adoption team only; MVP best practice; central IT team; strategic alignment; operational alignment; cloud
center of excellence (CCoE). Examples from the article:
- Adoption team only: the cloud adoption team is Accountable for every column.
- MVP best practice: the adoption team is Accountable for solution delivery, business alignment, change management
  and solution operations; a cloud governance team is Accountable for governance, platform maturity, platform
  operations and platform automation.
- Full CCoE: strategy team Accountable for business alignment and change management; adoption team for solution
  delivery; operations team for solution operations and platform operations; governance team for governance;
  platform team for platform maturity; automation team for platform automation.
The last row of each table (except the first) refers to the most-aligned cloud capability for more information.

## Steps
1. Pick the team structure closest to your organisation and the capabilities your teams must cover.
2. Fill the matrix with each team's role per capability; one Accountable team per function.
3. Resolve gaps (no Accountable) and overlaps with leadership.
4. Revisit when the team structure changes.

## Verify
- [ ] Every capability column has exactly one Accountable team.

## Checked
2026-11-09. Confirmed against the CAF RACI alignment article (downloaded HTML; intro and all six tables read).
Removed unconfirmed material: the function list and activity-row example (landing-zone, policy, commitment
purchases), the 40-60 activity guidance, the gotchas on passive workload teams and access alignment, and the
organize landing-page source (not read).
Method: docs-checked 2026-11-09 against learn.microsoft.com/azure/cloud-adoption-framework/organize/raci-alignment downloaded HTML; documentation only, no commands run.

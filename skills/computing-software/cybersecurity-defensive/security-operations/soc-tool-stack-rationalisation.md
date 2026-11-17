---
id: computing-software.cybersecurity-defensive.security-operations.soc-tool-stack-rationalisation
name: soc-tool-stack-rationalisation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-tool-rationalisation, soc-management, tool-consolidation, attack-coverage, cost-optimisation, security-architecture]
level: advanced
status: draft
description: "Rationalise a SOC tool stack: inventory tools vs use cases and ATT&CK coverage, overlap and utilisation analysis, cost per capability, consolidation decisions and migration."
sources: ["https://center-for-threat-informed-defense.github.io/", "https://mitre-attack.github.io/attack-navigator/", "https://www.ncsc.gov.uk/collection/building-a-security-operations-centre"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SOC tool stack rationalisation

## Inventory
For each tool: owner, cost (licence, infra, people hours), contract end date, data produced, use
cases served, integrations, actual usage (logins, queries, alerts actioned), and ATT&CK techniques
detected/prevented (from vendor mappings validated by testing).

## Analysis
- **Overlap matrix**: capability x tool (EDR, NDR, SIEM, SOAR, TIP, CASB, email security, DLP,
  vulnerability scanning). Mark primary vs redundant.
- **Coverage**: Navigator layers per tool; union shows total coverage; techniques covered only by
  one tool are dependencies.
- **Utilisation**: tools producing alerts nobody actions, or dashboards nobody opens.
- **Cost per capability** and per true positive.

## Decide
- Keep/consolidate/replace/retire per tool with rationale.
- Platform consolidation (e.g. XDR suite replacing point products) trades best-of-breed depth for
  integration and fewer consoles; check coverage gaps after consolidation.
- Align with contract renewal dates to avoid paying twice.

## Migrate
1. Run in parallel; compare detections on the same attack simulations.
2. Migrate content (detections, playbooks, allowlists) and data retention requirements.
3. Decommission: remove agents, revoke API keys, archive data per retention obligations.

## Gotchas
- Vendor ATT&CK claims are marketing until tested.
- Removing a "quiet" tool can drop a unique data source used in investigations; ask analysts.
- People cost of operating many consoles often exceeds licence savings; count both.

## Verify
After rationalisation: coverage layer unchanged or improved, cost reduced, analyst console count down,
and simulation results meet the same detection benchmarks.

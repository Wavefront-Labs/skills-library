---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-policy
name: cost-policy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-governance, cost-policy, cloud-policy, governance-framework]
level: practitioner
status: docs-checked
description: "Write cost policies teams follow using the FinOps Governance, Policy and Risk capability: policy types, guidelines vs guardrails vs automation, and shift-left enforcement."
sources: ["https://www.finops.org/framework/capabilities/policy-governance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud cost policies

The FinOps Framework describes policy as turning governance direction into specific, authoritative
statements. A good policy is specific enough to be useful, proportionate to the risk it
addresses, and backed by real authority; poorly scoped or unenforced policies create "compliance
theater".

## Policy types the Framework lists
- Preferred, required and restricted technology services across scopes.
- Data storage lifecycle and retention.
- Technology modernisation and decommissioning.
- Technology and spend-based commitment guardrails (see `commitment-policy`).

## Example policy statements from the Framework
- A defined, agreed proportion of optimised compute usage must be covered by a discounted
  commitment at all times, reviewed as usage changes.
- Resources with sustained zero or near-zero utilisation for a defined period will be
  decommissioned unless a documented business justification is approved.
- Services not on the approved catalog need architectural review and FinOps impact assessment
  before procurement.

## Implementing policy
1. **Guidelines**: advisory best-practice approaches.
2. **Guardrails**: mandatory pathways such as approval workflows, configuration enforcement,
   access controls or automated blocking of non-compliant provisioning.
3. **Automation**: encode compliance into systems (policy-as-code, configuration management,
   FinOps platforms) for detection, alerting, remediation and reporting. The share enforced by
   automation should rise with maturity.
4. **Shift left**: Crawl is documented policy checked manually in design review; Walk checks
   pull requests or provisioning templates automatically; Run adds runtime thresholds,
   escalation paths and exception records fed back into design.

## Steps
1. Define and communicate policies across scopes with Finance, Engineering, Procurement,
   Security and Risk.
2. Set a regular review cadence and report compliance to stakeholders.
3. Track KPIs such as policy adherence rate and governance automation coverage.

## Verify
- [ ] Each policy has an owner, an enforcement mechanism and a compliance measure.
- [ ] Policy exceptions have a defined path (see `cost-policy-exceptions`).

## Checked

Method: docs-checked 2026-11-09 against the FinOps Governance, Policy and Risk capability page (read in full). The Azure Cloud Adoption Framework and AWS whitepaper sources were not readable and were dropped. Removed unconfirmed: the five-item typical policy set (mandatory tags, non-production schedules, sandbox cleanup, marketplace, storage lifecycle size rule), report-only-first phasing, provider policy tooling, the quarterly review and the gotchas.

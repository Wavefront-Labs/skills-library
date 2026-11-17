---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-procurement
name: finops-procurement
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-practice, finops-procurement, intersecting-disciplines, itam, finance-partnership]
level: practitioner
status: docs-checked
description: "Coordinate FinOps with procurement, finance, ITAM and other intersecting disciplines using the Framework: shared data, renewal and exit ownership, and signals of success."
sources: ["https://www.finops.org/framework/capabilities/intersecting-disciplines/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working with procurement, finance and ITAM

The Intersecting Disciplines capability does not tell FinOps how to perform other disciplines. It
gives FinOps ways to coordinate with those already in place (ITFM, ITAM or SAM, ITSM, security,
enterprise architecture, platform engineering, DevOps or SRE and portfolio management). Not every
organisation has all of them; in some, the FinOps team performs SAM itself.

## Procurement
- Use information from FinOps and allied personas to pick the best procurement method for
  resources and licences.
- Identify contracts in the procurement system of record.
- Make sure provider and reseller agreements give allied personas access to cost data.
- Define renewal, exit and consumption accountability, assigned at signature alongside
  procurement and finance (Walk) and monitored continuously against usage and entitlement data
  (Run), rather than left undefined until the contract nears expiry (Crawl).
- Project forward use by licence type to plan whether to create, change or stop licence agreements.

## Finance
- Use FinOps and intersecting-discipline information for budget planning and forecasting.
- Decide how to identify costs in the accounting system of record and share relevant costs with
  those who need them.
- Confirm the accuracy of cost model calculations and reporting, and establish IT financial
  governance with FinOps and allied personas.

## ITAM / SAM
- Include SAM when proposing Bring Your Own Licence models, because of the impact on existing
  commitments with software publishers.
- FinOps validates demand, entitlements and contract flexibility; allied personas track the licence
  position using FinOps data.

## Steps
1. Define shared data, resources and terminology (for example FOCUS), plus metadata, data access,
   resolution, exchange format and refresh cadence.
2. Define common decision workflows, communication channels and cross-team notifications.
3. Agree shared objectives and responsibilities with leadership.
4. Revisit the arrangement regularly as part of maturity evolution.

## Signals of success
- Consistent reporting from the same data sources, and consultation before policy or tooling
  changes. Example KPIs named: tag compliance, percent of costs unallocated, untagged or
  tagging-policy compliant, and licence compliance and optimisation.

## Verify
- [ ] Renewal, exit and consumption owners are named at contract signature.
- [ ] FinOps and allied teams report from one shared data source.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Framework Intersecting Disciplines capability page (read in full).
Removed as unconfirmed: EDP and MACC negotiation inputs, the monthly and quarterly touchpoint cadence, the RACI step, accounting treatments (amortisation, capitalisation, accruals), and the practice-operations and personas sources (not read).

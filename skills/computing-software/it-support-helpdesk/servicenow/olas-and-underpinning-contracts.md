---
id: computing-software.it-support-helpdesk.servicenow.olas-and-underpinning-contracts
name: olas-and-underpinning-contracts
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, sla, service-level-management, ola, underpinning-contract, uc, resolver-group-targets, vendor-sla, itil-4]
level: practitioner
status: draft
description: "Back customer SLAs with internal OLAs and vendor underpinning contracts: setting targets that add up, measuring OLAs per group in ServiceNow, and managing vendor SLA evidence."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# olas-and-underpinning-contracts

Goal: when the service desk promises users "resolved in 8 business hours",
every team and vendor behind it has a target that makes that possible.

## Definitions
- **SLA**: agreement between IT and its customers (users/business).
- **OLA** (operational level agreement): between internal teams — e.g.
  network team responds to assigned P2 tickets in 1 hour, resolves in 6.
- **UC** (underpinning contract): with external suppliers — e.g. hardware
  vendor next-business-day on-site, ISP 4-hour fix.

## Make the numbers add up
SLA resolution time ≥ desk triage + OLA of resolver group + any UC time
in the path. If the laptop vendor's UC is next business day, a 4-hour P3
hardware SLA is a fiction — adjust the SLA, buy a better UC, or hold spares.

## OLAs in ServiceNow
- SLA definitions with type **OLA**, condition on `assignment_group` (e.g.
  starts when assignment group = Network and state not resolved; stops on
  reassignment away or resolution).
- One OLA per group per priority; reset on group change so each group is
  measured on its own time.
- Report OLA achievement per group monthly; review in service review
  meetings, not as blame tool.

## UCs
- Record vendor contracts (Contract Management / vendor records) with
  their SLA terms, support numbers, escalation contacts, renewal dates.
- Vendor ticket numbers in the incident; track vendor response/fix times
  (UC-type SLA or manual fields) to have evidence for service credits.
- Escalation path in the contract — use it when the vendor misses
  (see vendor escalation skill).

## Gotchas
- OLAs nobody agreed to (imposed by the desk) get ignored — negotiate with
  team leads, sign off, review yearly.
- Measuring OLAs while tickets bounce between groups requires reset rules,
  or the receiving group inherits the previous group's delay.

## Verify
For each customer SLA you can show the OLAs/UCs in its path and that their
sum fits; OLA reports exist per group.

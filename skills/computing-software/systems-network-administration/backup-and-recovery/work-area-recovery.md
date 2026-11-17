---
id: computing-software.systems-network-administration.backup-and-recovery.work-area-recovery
name: work-area-recovery
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [work-area-recovery, alternate-sites, business-continuity, remote-work, seats, workplace-recovery]
level: practitioner
status: draft
description: "Plan work area recovery for staff after losing an office: seat counts from the BIA, shared recovery centres, remote working, desk images, telephony redirection, and testing."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://www.iso.org/standard/75106.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Work area recovery

**Goal:** the people who run critical processes have somewhere to work, with working devices and phones, within the process RTO.

## Size it
From the BIA: for each process, the minimum staff needed per time bucket (e.g. 10 seats in 24 h, 40 in 72 h). Sum per site. Do not plan for full headcount.

## Options
| Option | Notes |
|---|---|
| Remote work | default for most knowledge work; needs laptops at home, VPN/ZTNA capacity, MFA not tied to office |
| Shared recovery centre (syndicated seats) | vendor-provided desks; check oversubscription and how seats are allocated in a regional event |
| Dedicated recovery seats | guaranteed, expensive |
| Other company offices | reciprocal or internal; displaces their staff |
| Hotels/pop-up | for short events |

## Technical checklist
- Desktop provisioning: VDI/DaaS or a standard image that can be deployed to vendor PCs quickly.
- Telephony: contact-centre and DDI numbers re-routable to recovery site or softphones; test the redirection.
- Printing, scanning, cheque printers, card readers, specialist peripherals.
- Network: VPN concentrator/ZTNA capacity for 100% remote, not the normal 30%.
- Identity: password resets and MFA enrolment without visiting the office.

## Gotchas
- Trading, contact centre and secure-room work often cannot go remote; these need real seats.
- VPN licences sized for normal remote use.

## Verify
Annual seat test: the named staff log in at the recovery centre or from home on the recovery path and perform a real process step; record time to productive.

---
id: computing-software.systems-network-administration.backup-and-recovery.mobile-recovery-sites
name: mobile-recovery-sites
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [mobile-site, alternate-sites, alternate-processing-site, disaster-recovery, nist-800-34, contingency-plan]
level: practitioner
status: docs-checked
description: "Plan a mobile recovery site (trailer or containerised data centre): vendor contracts, delivery time, power and network, staging, and when to choose it."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mobile recovery sites

**Goal:** know when a trailer or containerised data centre is the right alternate site and have it truly deployable within RTO.

## What it is
NIST SP 800-34 Rev. 1 (section 3.4.3) describes mobile sites as self-contained, transportable shells custom-fitted with the telecommunications and system equipment needed to meet system requirements. It treats them as a variation on cold, warm and hot sites. The guide says that in many cases a mobile site can be delivered to the desired location within 24 hours, but equipment installation and setup can increase that time. It also notes that equipment kept at a mobile or warm site is one equipment-replacement strategy.

## When it fits
Judgement, not from the guide:
- RTO of days, not hours.
- Facility loss is the main risk (fire, flood) but staff and network region survive.
- Regulatory or latency reasons keep systems near the primary location.
- Field operations that move.
It is a poor fit for minute-level RTOs or regional disasters that block roads. The guide warns that transportation may be limited or halted in a catastrophic disaster.

## Contract and prep checklist
- Vendor contract (guide, section 3.4.3): adequate testing time, work space, security, hardware and telecommunications requirements, support services, and recovery days (how long you can occupy the space) negotiated and stated in the contract. Several customers may contract for the same site; negotiate the vendor's policy on priority if too many declare at once.
- Pre-surveyed **pad**: level hard standing, truck access, generator hook-up or utility drop of the right capacity, fibre or carrier circuit pre-terminated, physical security (practice).
- Equipment list in the trailer vs what you ship: servers, storage, network, cellular backup (practice).
- Staging procedure: who meets the truck, power-on order, network turn-up, restore from offsite backups or replicated copies (practice).
- Permits (local authority, fire code) obtained in advance (practice).
- Check the site's security, management, operational and technical controls are compatible with your system (guide).

## Gotchas
- Restoring a large dataset from tape or cloud inside the trailer often dominates RTO; measure it.
- Shared-subscription vendors may not deliver in a regional event.
- Cooling capacity in summer.

## Verify
A deployment test to the pad (or at least a vendor demo plus power/network test at the pad), with timed delivery-to-service.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (full PDF from nvlpubs.nist.gov, the document behind the csrc.nist.gov page), sections 3.4.3 and 3.4.4. Targeted reads, not the whole 149 pages. Confirmed: mobile site definition, 24-hour delivery note with setup caveat, contract elements, shared-vendor priority issue, transport limits in a catastrophe. Removed: "24-72 h" delivery, the ready.gov source (not read), "oversubscription ratio", "annual" deployment test, "tens of TB" figure. Practice items are labelled.

Method: documentation only; no commands were run.

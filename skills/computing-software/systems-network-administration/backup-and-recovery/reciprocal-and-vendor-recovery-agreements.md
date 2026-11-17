---
id: computing-software.systems-network-administration.backup-and-recovery.reciprocal-and-vendor-recovery-agreements
name: reciprocal-and-vendor-recovery-agreements
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [reciprocal-agreement, service-level-agreement, dr-contract, alternate-site, draas, nist-sp-800-34]
level: practitioner
status: docs-checked
description: "Evaluate reciprocal agreements and vendor recovery contracts: compatibility, capacity, invocation SLAs, oversubscription, testing rights and exit."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reciprocal and vendor recovery agreements

**Goal:** an alternate-site or recovery service you can actually invoke when needed, with terms that survive a regional disaster.

## Reciprocal agreements (between organisations)
NIST SP 800-34 Rev. 1 (section 3.4.3): two or more organisations with similar or identical system configurations and backup technologies may agree, by a reciprocal agreement or memorandum of understanding (MOU), to serve as alternate sites for each other or to enter a joint contract for a site.
- Enter carefully: each site must support the other as well as its own workload, and the recovery sequences of both organisations must be prioritised jointly.
- Test at the partner sites for extra processing thresholds, compatible system and backup configurations, sufficient telecommunications, compatible security measures, and the sensitivity of data that other privileged users might reach.
- Consider system interconnections and interconnection security agreements (the guide points to NIST SP 800-47).
- Practice (not in the guide): both parties can be hit by the same regional event, and enforceability is weak, so use reciprocal arrangements for lower-criticality systems or as a supplement.

## Vendor contracts (commercial alternate sites, DRaaS, cloud)
The guide says the MOU or SLA should be written for your needs and the partner's capabilities, and reviewed and approved by each party's legal department. Minimum elements it lists include:
| Element | Notes from the guide |
|---|---|
| Duration, termination, extension | Contract duration, termination conditions, process to negotiate extension of service |
| Cost | Fees for disaster declaration and occupancy, administration, testing, annual increases, transport |
| Disaster declaration | Circumstances constituting a disaster and notification procedures |
| Priority, availability, guarantee | Site priority access, availability, guarantee, other subscribers and total number of site subscribers |
| Compatibility and requirements | Guarantee of compatibility, hardware, software, data and telecommunications requirements, change management |
| Security | Security requirements including special needs |
| Testing | Scheduling, availability, test time and duration, additional testing |
| Service levels | Performance measures and quality management |
| Records management | Onsite and offsite, electronic and hardcopy |
| Support | Staff support, facility services, work space, supplies provided or not |
Also negotiate recovery days (how long you may occupy the site). Customers should be aware that a vendor site may be unable to accommodate every customer if one disaster affects many of them; negotiate the vendor's policy and how priority is decided.

Exit terms (data return and deletion, transition help) and certifications or audit rights are good practice but not in the guide's list.

## Gotchas
- A provider's "first come, first served" clause makes regional disasters a lottery.
- Untested contracts often fail on connectivity and identity, not compute.

## Verify
A test invokes the service under contract terms and meets the stated time to availability.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (full PDF from nvlpubs.nist.gov, the document behind the csrc.nist.gov page), section 3.4.3. Targeted read, not the whole 149 pages. Confirmed: reciprocal agreement and MOU description, joint prioritisation and testing points, SLA/MOU minimum elements, vendor oversubscription caveat, legal review. Removed: the claim that the guide says to review agreements annually, the ISO source (not read), "hours from invocation" and "credits for misses" terms, and "annual test". Items beyond the guide are labelled practice.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.backup-and-recovery.alternate-sites-hot-warm-cold
name: alternate-sites-hot-warm-cold
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [alternate-site, recovery-strategy, hot-site, warm-site, cold-site, mirrored-site, nist-sp-800-34, disaster-recovery]
level: practitioner
status: docs-checked
description: "Choose an alternate site per NIST SP 800-34r1: cold, warm, hot, mobile and mirrored sites, matched to the BIA's MTD, with cost and contract checks."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alternate sites: cold, warm, hot and mirrored

**Goal:** a recovery location whose readiness matches each system's maximum tolerable downtime (MTD), at a cost the business accepted.

## Site types (NIST SP 800-34r1)
| Type | What exists | Cost and recovery time |
|---|---|---|
| Cold | Basic infrastructure and environmental controls (electrical, HVAC), room for equipment, no equipment or telecommunications in place | Least expensive; longest recovery, as all equipment must be acquired, installed and tested and software and data loaded; several days to weeks depending on size and complexity |
| Warm | Cold-site infrastructure plus enough computer and telecommunications equipment to operate the system, but not loaded with the software or data; should have backup media readers compatible with the backup strategy | More than cold; recovery takes several hours to several days depending on complexity and data to restore |
| Hot | Fully operational equipment and capacity, current production software, adequate storage, the most recent backed-up data loaded; needs a way to move users' connectivity quickly | Most expensive of the three, with operational support nearly equal to production; quick takeover |
| Mobile | Self-contained transportable shells fitted with telecommunications and system equipment | Often deliverable within 24 hours, but installation and setup can add time |
| Mirrored | Fully redundant facilities with automated real-time mirroring, identical to the primary site | Most expensive; virtually 100 percent availability |

SP 800-34 treats cold, warm and hot as the common three, with mobile and mirrored as variations; hybrids exist.

## Choosing
1. Use the BIA to find the critical processes, the MTD and the impact of losing the system.
2. A strategy can combine site types: highly critical functions may need a hot site while a reporting or batch function that can be down for days only needs space for equipment bought later.
3. Check the site's security, management, operational and technical controls are compatible with the system (firewalls, physical access, personnel security).
4. For a fixed site, consider how long staff and equipment take to get there, and place it where the same hazard is unlikely to affect both primary and alternate sites.

## Commercial sites
Negotiate and state in the contract: adequate testing time, workspace, security, hardware and telecommunications requirements, support services and recovery days (how long you may occupy the space). Several customers may contract for the same site and it may be unable to hold them all if a disaster hits many at once, so negotiate the vendor's priority policy.

## Gotchas
Do not choose on cost alone; the BIA MTD sets what readiness you need.

## Verify
Each system's row shows site type, the recovery time achieved in the last test, and any gap against the BIA target.

## Checked

2026-11-09. Read NIST SP 800-34 Rev. 1 sections 3 (alternate site paragraphs, Table 3-34) and 5.1 (cold, warm and hot sites). Removed: the typical RTO column (weeks, days, hours, minutes), cloud DR/DRaaS row, tiering examples by RTO, power and carrier diversity, yearly warm-site test, capacity-for-all-tier-1 and remote work gotchas (not stated).

Method: documentation only; no commands were run.

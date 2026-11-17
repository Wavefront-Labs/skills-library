---
id: computing-software.systems-network-administration.backup-and-recovery.equipment-replacement-strategy
name: equipment-replacement-strategy
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [equipment-replacement, alternate-sites, vendor-agreements, spares, disaster-recovery, nist-800-34]
level: practitioner
status: docs-checked
description: "Plan IT equipment replacement after a disaster: vendor quick-ship agreements, held spares, existing compatible equipment and configuration records."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equipment replacement strategy

**Goal:** you can obtain working replacement hardware within RTO when the originals are destroyed.

## Three options (SP 800-34 Rev. 1, section 3.4.4)
| Option | How | Trade-off (from the guide) |
|---|---|---|
| Vendor agreements | SLAs with hardware, software and support vendors for emergency maintenance; specify how quickly the vendor must respond, priority for shipment of replacement equipment over normal orders, and priority in a catastrophic disaster involving many vendor clients | In such a disaster, organisations with health- and safety-dependent processes often get the highest shipping priority; keep the SLA with the contingency plan |
| Equipment inventory | Buy in advance and store at a secure offsite location, for example a warm or mobile alternate site | Needs money committed up front; kit can become obsolete or unsuitable as technology and requirements change |
| Existing compatible equipment | Equipment at the contracted hot site or elsewhere in the organisation | Hot-site and reciprocal agreements stipulate that similar, compatible equipment is available for contingency use |

The guide adds: buying equipment when needed is cost-effective but adds overhead while waiting for shipment and setup; storing unused equipment is costly but lets recovery start sooner. Transportation may be limited or halted in a catastrophic disaster, so consider mass equipment replacement and transport delays, using the BIA impacts. Keep detailed lists of equipment needs and specifications in the contingency plan.

## Steps (practice)
1. From the BIA resource list, note every hardware item with its model, firmware, and minimum quantity.
2. For each, check the current lead time. Anything over the RTO needs a spare, a quick-ship contract, or a cloud fallback.
3. Write the order specs ahead of time: exact SKUs, NIC/HBA/RAID models, transceivers, cables, rails, licences. Store a bill of materials per system in the plan appendix.
4. Keep config backups for network devices, firewalls, storage arrays and BMC/firmware settings so new kit can be configured identically.
5. Keep hardware-bound licences in mind (dongles, MAC- or host-ID-locked licences); get DR licence terms in writing.
6. Review at hardware refresh and when the BIA or plan changes.

## Gotchas
- Spares sitting in the same building as production.
- Restoring a backup to a newer server generation without drivers; keep driver packs with the BOM.
- Vendor quick-ship covering "equivalent" models that need different drivers or firmware.

## Verify
For each critical system, the replacement path and its lead time are documented and shorter than RTO; spare kit is powered on and updated on a schedule you define.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (PDF behind the csrc.nist.gov page), sections 3.4.4 and 3.4.5. Targeted reads, not the whole 149 pages. Confirmed: the three strategies, vendor SLA content, inventory drawbacks, trade-off statement, transport caveat. The section number is 3.4.4, not 3.4.3 as the earlier draft said. Removed: the NIST SP 800-53 source (not read), "N hours" quick-ship wording, "lead times can be weeks", "review annually", "twice a year". Steps list is labelled practice.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.backup-and-recovery.iscp-contact-lists-and-appendices
name: iscp-contact-lists-and-appendices
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [contact-list, iscp-appendix, contingency-plan, iscp, nist-800-34]
level: practitioner
status: docs-checked
description: "Choose the ISCP plan appendices per NIST SP 800-34r1 section 4.5: contacts, vendors, BIA, procedures, equipment lists, interconnections, SLAs, vital records."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ISCP appendices and contact lists

**Goal:** the appendices carry the details the plan body leaves out, so recovery can proceed from the plan alone.

## Common appendices (SP 800-34r1 section 4.5)
- Contact information for contingency planning team personnel.
- Vendor contact information, including offsite storage and alternate site POCs.
- BIA.
- Detailed recovery procedures and checklists.
- Detailed validation testing procedures and checklists.
- Equipment and system requirements lists of the hardware, software, firmware and other resources needed to support operations, with model or version number, specifications and quantity for each entry.
- Alternate mission/business processing procedures that may run while the system is recovered.
- ISCP testing and maintenance procedures.
- System interconnections (systems that directly interconnect or exchange information).
- Vendor SLAs, reciprocal agreements with other organisations, and other vital records.

## Contact tables
The NIST ISCP templates in the appendices of SP 800-34r1 include a Key Personnel table with a contact information column, to be filled in for the system. Reuse that layout, adding primary and alternate for each role (see iscp-recovery-roles-and-teams).

## Gotchas
- Appendices that sit only on the system being recovered cannot be read when needed; keep a copy that is reachable during an outage (practice guidance, not stated by NIST).

## Verify
Every appendix in the list above that applies to the system exists, is current, and is referenced from the plan body.

## Checked

2026-11-09. Read NIST SP 800-34 Rev. 1 section 4.5 and the Key Personnel table in the sample ISCP templates. Removed: ready.gov source (403, not read), the A to L lettering, contact field list (personal email, Signal), quarterly test page, 30 day and 90 day limits, HR leaver feed and privacy distribution notes (none stated).

Method: documentation only; no commands were run.

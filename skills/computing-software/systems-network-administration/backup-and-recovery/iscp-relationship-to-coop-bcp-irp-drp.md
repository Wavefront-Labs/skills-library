---
id: computing-software.systems-network-administration.backup-and-recovery.iscp-relationship-to-coop-bcp-irp-drp
name: iscp-relationship-to-coop-bcp-irp-drp
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [iscp-related-plans, contingency-plan, coop, bcp, drp, incident-response-plan]
level: practitioner
status: docs-checked
description: "Position the ISCP among related plans per NIST SP 800-34r1 section 2.2: BCP, COOP, crisis comms, CIP, cyber IRP, DRP and OEP, and how they hand off."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# How the ISCP fits with other plans

**Goal:** recovery strategies and resources that neither negate each other nor duplicate effort, so plans are coordinated during development and updates (SP 800-34r1 section 2.2). NIST notes definitions are not universal, so an organisation's actual plans may differ from these descriptions.

## Plan types
- **BCP**: sustains mission/business processes (for example payroll or customer service) during and after a disruption; may cover one business unit or the whole organisation, or only priority functions. Can support long-term recovery alongside COOP. The planner must coordinate with information system owners so BCP expectations match system capabilities.
- **COOP**: restores mission essential functions at an alternate site and performs them for up to 30 days before returning to normal. Minor disruptions that need no relocation are typically not covered. Mandated for federal organisations (HSPD-20/NSPD-51, FCD 1); non-government organisations typically use BCPs.
- **Crisis communications**: standard procedures for internal and external communications in a disruption; typically names the only individuals allowed to give information to the public, so COOP and BCP planners need to follow it.
- **CIP**: policies and procedures to protect and recover critical national infrastructure and key resources.
- **Cyber incident response plan**: procedures for security personnel to identify, mitigate and recover from malicious computer incidents; may be an appendix of the BCP.
- **DRP**: information-system-focused plan for major, usually physical disruptions that deny access to the primary facility for an extended period; restores the system, application or facility infrastructure at an alternate site. Addresses only disruptions that require relocation. May be supported by multiple ISCPs, and may support a BCP or COOP.
- **ISCP**: procedures to assess and recover one system after a disruption, regardless of site; includes roles, inventory, assessment, detailed recovery procedures and testing.
- **OEP**: first-response procedures for occupants for threats to health and safety (fire, bomb threat, chemical release, medical emergency, shelter in place); facility level, executed separately and first.

## Handoffs stated by NIST
- DRP then ISCP: once the DRP moves a site to an alternate site, each affected system uses its ISCP to restore, recover, test and return to operation.
- ISCP vs DRP: the ISCP is site-independent and can be activated at the current location or an alternate site; the DRP is site-specific.
- Crisis communications procedures go to COOP and BCP planners so only approved statements are released.
- COOP: information systems that support COOP functions need RTOs that meet COOP requirements.

## Gotchas
Do not treat COOP, ISCP, DRP and BCP as interchangeable; federal directives distinguish COOP from ISCPs, DRPs and BCPs.

## Verify
Each plan lists related plans and the trigger and handoff point to them, agreed by the owners.

## Checked

2026-11-09. Read NIST SP 800-34 Rev. 1 section 2.2 (2.2.1 to 2.2.8) and the COOP vs ISCP boxes. Removed: SP 800-61r3 source (not read), the owner/trigger table, the IRP-before-recovery gate and evidence-destruction gotcha, joint annual exercise advice, shared plan diagram (none stated).

Method: documentation only; no commands were run.

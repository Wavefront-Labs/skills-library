---
id: computing-software.systems-network-administration.backup-and-recovery.contingency-plan-activation-and-notification
name: contingency-plan-activation-and-notification
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [contingency-plan, iscp, activation-criteria, call-tree, notification, damage-assessment, nist-sp-800-34, disaster-recovery]
level: practitioner
status: docs-checked
description: "Write the ISCP activation and notification phase (NIST SP 800-34): activation criteria, who declares, call trees, outage assessment, status updates."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contingency plan: activation and notification phase

**Goal:** when a disruption happens, the right people are notified promptly, a named
person decides whether to activate the plan, and nobody wastes the first hour working out
who to call.

## ISCP structure (NIST SP 800-34r1, Figure 4-1)
1. Supporting information (introduction and concept of operations, including roles and responsibilities).
2. **Activation and notification** (this skill): activation criteria, notification procedures, outage assessment.
3. Recovery: sequence of recovery activities, recovery procedures, escalation and notifications.
4. Reconstitution: validation testing, notifications, cleanup, offsite data storage, backup, documentation.
5. Appendices (BIA, point-of-contact lists, procedures, and so on).

## Activation criteria
NIST (section 4.2.1): criteria are unique to each organisation and stated in the contingency planning policy. They may be based on:
- extent of damage to the system (physical, operational or cost);
- criticality of the system to the mission;
- expected outage duration longer than the RTO.
The designated authority (typically a senior manager or CIO) activates the plan once the ISCP Coordinator has determined the criteria are met. NIST says only one individual should hold this authority, with a successor clearly identified.

## Notification
- Document procedures for both outages with prior notice (for example a predicted hurricane) and without (equipment failure, a criminal act), covering business and non-business hours.
- Methods named in the guide: telephone, pager, email, cell phone, messaging, and automated notification systems. Email gives no assurance of receipt and acknowledgement, and personal email may help if the LAN is down.
- A common manual method is a **call tree**: notification duties assigned to specific individuals who notify others. It should account for primary and alternate contact methods and say what to do if someone cannot be contacted.
- Contact lists appended to the plan identify people by team position, name and contact details (home, work, cell, email).
- Also notify points of contact at external organisations and interconnected systems that may be affected.
- Content of a notification (as necessary): nature of the outage, known outage estimates, response and recovery details, where and when to convene, instructions to prepare for relocation, and call-tree instructions.
- Practice beyond the guide: use an out-of-band bridge that does not depend on the affected systems (corporate email and chat may be down or compromised), pre-write message templates, and keep the roster outside the systems it is needed to recover. Keep copies of procedures securely at alternate locations.

## Outage assessment
The Outage Assessment Team is usually notified first. Personnel safety stays the top priority. Minimum areas (section 4.2.3): cause; potential for additional disruption or damage; status of physical infrastructure; inventory and functional status of equipment; type of damage to equipment or data; items to be replaced; estimated time to restore normal services. Results decide whether to notify further teams and how the plan is carried out.

## Maintenance
Contact details go stale first. NIST says contact lists need more frequent review than the rest of the plan, and gives testing call tree lists against prescribed time limits as an example test. Set the review and drill frequency in your own policy.

## Verify
In the last notification drill, all primary or alternate contacts responded within the
target time; the plan names the activation authority and criteria, and the roster exists
offline.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (full PDF from nvlpubs.nist.gov, the document behind the csrc.nist.gov page), sections 3.5 (testing), 3.6, 4.1 and 4.2. Targeted reads of those sections, not the whole 149 pages. Confirmed: five-component structure, activation criteria bases, single designated authority with successor, notification methods and call tree, notification content, outage assessment minimum areas. Removed: the "fraction of the RTO" trigger example, "SMS", "within minutes", and the quarterly review and yearly drill frequencies (not stated by the guide). The out-of-band bridge, templates and offline roster are labelled as practice beyond the guide.

Method: documentation only; no commands were run.

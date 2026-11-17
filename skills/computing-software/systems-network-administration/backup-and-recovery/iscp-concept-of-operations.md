---
id: computing-software.systems-network-administration.backup-and-recovery.iscp-concept-of-operations
name: iscp-concept-of-operations
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [concept-of-operations, contingency-plan, iscp, nist-800-34, recovery-phases, plan-structure]
level: practitioner
status: docs-checked
description: "Write the ISCP concept of operations section per the NIST SP 800-34r1 template: system description, the three phases, and roles and responsibilities."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ISCP section 2: concept of operations

**Goal:** a section that gives details about the system, an overview of the three plan phases, and who does what during a contingency activation (SP 800-34r1 Appendix A template, section 2).

## 2.1 System description
Can be copied from the System Security Plan (SSP) or reference it and attach the latest version. Give a general description of architecture and functionality, the operating environment, physical location, general location of users, partnerships with external organisations/systems, and other technical considerations important to recovery, such as backup procedures.

## 2.2 Overview of the three phases
The phased approach recovers the system in a methodical sequence, to maximise effectiveness and minimise outage time from errors and omissions.
- **Activation and Notification**: activation occurs after a disruption or outage that may reasonably extend beyond the system's RTO (for example severe damage to the facility or loss of equipment). Once activated, system owners and users are notified of a possible long-term outage and an outage assessment is performed; its results go to system owners and may modify recovery procedures for the cause of the outage.
- **Recovery**: activities and procedures to recover the affected system, written so an appropriately skilled technician can recover it without intimate system knowledge, and including notification and escalation procedures for communicating recovery status.
- **Reconstitution**: test and validate capability and functionality at the original or new permanent location, in two activities. Validation (functionality or regression testing, concurrent processing and/or data validation) ends with system owners declaring the system recovered and operational. Deactivation notifies users of status, finalises documentation and activity logs, incorporates lessons learned into plan updates and readies resources for future events.

## 2.3 Roles and responsibilities
Describe each team and role for recovery and reconstitution, with responsibilities, leadership roles and coordination with other teams. At a minimum establish a system owner or business unit point of contact, a recovery coordinator and a technical recovery point of contact. Leadership includes an ISCP Director (overall management responsibility for the plan) and an ISCP Coordinator (oversees recovery and reconstitution progress, starts escalations or awareness communications, and coordinates with other teams). See iscp-recovery-roles-and-teams.

## Gotchas
Do not omit reconstitution: the template treats validation and deactivation as part of the plan, not an afterthought.

## Verify
A newcomer can say from this section what triggers activation (an outage that may extend beyond the RTO), what the three phases are and who holds the minimum roles.

## Checked

2026-11-09. Read NIST SP 800-34 Rev. 1 Appendix A sample ISCP section 2 (2.1 to 2.3). Removed: page-length rule, measurable-trigger example (8 h), diagram advice, backup type and alternate site summary list, the team list and line-of-succession content (not in this section of the template), and the "roles by person" gotcha.

Method: documentation only; no commands were run.

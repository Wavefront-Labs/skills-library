---
id: computing-software.systems-network-administration.backup-and-recovery.contingency-plan-recovery-phase-procedures
name: contingency-plan-recovery-phase-procedures
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [recovery-procedures, recovery-sequence, contingency-plan, iscp, reconstitution, nist-sp-800-34, disaster-recovery]
level: advanced
status: docs-checked
description: "Write the recovery phase of a contingency plan: dependency-ordered sequence, step-level procedures with roles, escalation, reconstitution and deactivation."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovery phase procedures and sequence

**Goal:** after activation, the team restores systems in the right order with procedures detailed enough to follow under stress.

## NIST SP 800-34 phases
1. Activation and notification.
2. **Recovery**: implement recovery strategies to restore system capabilities, repair damage and resume operations at the original or an alternate location. It may be temporary manual processing, an alternate system, or an alternate site. Possibly only resources rated high priority in the BIA are recovered at this stage.
3. **Reconstitution**: test and validate system capability, resume normal operations, deactivate the plan.

## Recovery sequence
NIST (section 4.3.1): recovery procedures should reflect the priorities from the BIA, and the sequence should reflect the system's MTD. Write them stepwise and sequentially so components are restored logically. Examples from the guide: recover the most critical servers before less critical devices such as printers; for an application server, restore and verify the operating system before the application and its data.

A typical dependency order to refine from your own dependency map and BIA (illustrative, not from the guide):
1. Facilities, power, network core, firewalls, DNS.
2. Identity: directory services, PKI, privileged access, MFA.
3. Virtualisation/compute platform and storage; backup infrastructure.
4. Databases and messaging.
5. Application tiers (back end before front end).
6. Integrations, batch jobs, reporting.
7. End-user access (VPN, VDI, portals).
Document why each item precedes the next.

## Writing procedures
- Assign procedures to the appropriate recovery team. The guide lists typical actions: obtaining authorization to access damaged facilities, notifying internal and external partners, obtaining and installing hardware, obtaining and loading backup media, restoring critical operating system and application software, restoring data to a known state, testing functionality including security controls, connecting to the network, and operating alternate equipment.
- Write in a straightforward step-by-step style; assume and omit no steps; a checklist format helps document the sequence and troubleshoot.
- Include exact commands, consoles, credentials location (vault, break-glass envelope) and vendor support numbers, with a role responsible, not only a named person.
- Note decision points ("if backup older than RPO, escalate to plan coordinator").

## Escalation and status
- Include escalation steps and coordination with other teams for: an action not completed in the expected time frame, a key step completed, items that must be procured, and other system-specific concerns.
- Define the events, thresholds or triggers that call for additional notifications to recovery staff, status updates to leadership and notices for additional resources.

## Reconstitution
- Validation per the guide: concurrent processing (run at two locations until assured the recovered system is correct and secure; NIST notes the 800-53 controls do not require systems to have this capability), validation data testing (complete and current to the last available backup) and validation functionality testing.
- Declare reconstitution complete in a recovery/reconstitution log or other documentation. The Coordinator, with the system owner and with the Authorizing Official's concurrence, decides whether significant change requires reassessment and reauthorization.
- Deactivation: notify users using predefined procedures, clean up work space and temporary locations, return backup media to offsite storage, take a full backup of the recovered system as soon as reasonable, document all recovery events, and produce an after-action report with lessons learned to update the plan. Then formally deactivate and announce to business and technical contacts.

## Gotchas
- Procedures that assume staff from the failed site are available, or that the documentation server is up; store plans offline and off-site.
- Circular dependencies (backup server needs AD; AD restore needs backup server) must be broken explicitly.

## Verify
In an exercise, a team member who did not write the procedure follows it to restore the system within the RTO.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (full PDF from nvlpubs.nist.gov, the document behind the csrc.nist.gov page), sections 4.3 to 4.4. Targeted reads of those sections, not the whole 149 pages. Confirmed: phase definitions, sequence reflecting BIA priorities and MTD, example orderings, procedure action list, escalation triggers, reconstitution validation steps, deactivation activities and after-action report. The seven-layer dependency order is marked as illustrative practice, not a NIST list. Removed: the claim that reconstitution is "often its own planned failback" and the shared status board detail (not in the guide).

Method: documentation only; no commands were run.

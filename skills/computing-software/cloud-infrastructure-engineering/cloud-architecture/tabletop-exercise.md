---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.tabletop-exercise
name: tabletop-exercise
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, tabletop-exercise, incident-response-exercise, ir-simulation, injects, cloud-incident-response]
level: practitioner
status: draft
description: "Run a cloud incident response tabletop: scenario and injects, roles, decision points, timing, gaps captured and turned into playbook and tooling actions."
sources: ["https://www.cisa.gov/resources-tools/services/cisa-tabletop-exercise-packages", "https://csrc.nist.gov/pubs/sp/800/84/final", "https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident response tabletop exercises

## Design
1. **Objective**: test a specific playbook or decision (e.g. ransomware in cloud backups, leaked
   admin credential, data exfiltration via public bucket, provider region outage + security event).
2. **Participants**: incident commander, cloud platform, security operations, app owners, legal,
   comms, exec sponsor for escalation decisions.
3. **Scenario with injects** released over time:
   - T0: GuardDuty/Defender alert of anomalous API calls from unknown IP.
   - T+15: attacker created an IAM user; billing spike in a far region.
   - T+30: journalist asks about data leak; legal asks about notification deadlines (GDPR 72 h).
4. **Decision points**: isolate account? shut down production? notify regulator? pay ransom?

## Running it (60-120 min)
- Facilitator presents injects; participants say what they'd do, who, with which tool/access.
- Scribe records actions, times, blockers ("we don't know who can revoke sessions").
- Ask "show me": open the actual log query or runbook.

## After
Hot wash, written report, actions with owners: missing access, playbook gaps, logging gaps,
contact lists. Repeat at least annually; vary scenarios.

## Verify
- [ ] Actions tracked to closure before the next exercise.

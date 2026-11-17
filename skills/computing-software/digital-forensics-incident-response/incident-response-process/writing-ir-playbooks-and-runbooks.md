---
id: computing-software.digital-forensics-incident-response.incident-response-process.writing-ir-playbooks-and-runbooks
name: writing-ir-playbooks-and-runbooks
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [playbook-authoring, ir-runbook, playbook, soar, ir-preparation, dfir]
level: practitioner
status: draft
description: "Write incident-type playbooks and runbooks that responders actually follow: trigger, decision points, step owners, evidence to collect, and SOAR-ready structure."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/sites/default/files/2024-08/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf", "https://github.com/certsocietegenerale/IRM"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing IR playbooks and runbooks

**Goal:** for each common incident type, a short decision-oriented procedure that a tired
analyst can follow, and that maps cleanly to SOAR automation.

## Playbook vs runbook
- **Playbook**: incident-type level (phishing, ransomware, cloud key leak). Phases, decision
  points, who to involve. 2-5 pages.
- **Runbook**: one technical task (isolate host in CrowdStrike, revoke Entra sessions, pull
  CloudTrail for a key). Exact clicks/commands.

## Playbook structure (CERT-SG IRM and CISA federal playbook style)
1. **Trigger / entry criteria**: alerts or reports that start it.
2. **Preparation prerequisites**: access, tools, contacts needed.
3. **Identification**: questions to answer with the queries/runbooks that answer them.
4. **Decision points** as explicit yes/no: "Is the account privileged? yes -> SEV2 and
   page IC". Draw as a flowchart.
5. **Containment / eradication / recovery** steps with owner role per step.
6. **Evidence to preserve** before any destructive step (memory, mailbox export, logs).
7. **Communication and notification** checkpoints (legal, privacy, regulator clocks).
8. **Exit criteria** and closure checklist.

## Writing rules
- Imperative verbs, numbered steps, one action per step.
- Link runbooks instead of embedding commands that change with tool versions.
- Mark steps safe to automate (enrichment, ticket creation) vs human-approval (disable a VIP
  account, isolate a server).
- Version and owner on every playbook; review after each use.

## Starter set
Phishing/credential harvest, BEC, malware on endpoint, ransomware, compromised cloud keys,
compromised privileged account, web shell, data exfiltration/insider, DDoS, lost device.

## Verify
Hand the playbook to an analyst who did not write it and run a simulated alert; every place
they stop to ask a question is an edit.

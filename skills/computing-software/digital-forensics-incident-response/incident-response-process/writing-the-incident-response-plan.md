---
id: computing-software.digital-forensics-incident-response.incident-response-process.writing-the-incident-response-plan
name: writing-the-incident-response-plan
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [incident-response-plan, ir-plan, ir-policy, nist-sp-800-61, csf-2, governance, dfir]
level: practitioner
status: draft
description: "Write an incident response plan and policy that survive audit and a real 3am incident: scope, authority, roles, severity, comms, and approval path."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/resources-tools/resources/incident-response-plan-irp-basics"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing the incident response plan

**Goal:** a short, approved document that tells people at 3am who decides, who acts and
who must be told, plus a policy that grants the authority to do it. NIST SP 800-61r3
places this under CSF 2.0 *Govern* (GV.PO policy, GV.RR roles) and *Respond* (RS.MA).

## Three documents, not one
| Document | Owner | Changes | Content |
|---|---|---|---|
| **IR policy** | CISO / exec sponsor | yearly | Authority (who may isolate a production system, seize a laptop, call law enforcement), definitions of *event* vs *incident*, mandatory reporting to the IR team, data handling. 2-4 pages. |
| **IR plan** | IR lead | twice a year | Mission, scope, roles, severity matrix, escalation tree, comms plan, third parties, metrics, plan maintenance. 10-20 pages. |
| **Playbooks** | IR team | continuously | Per incident type (ransomware, BEC, insider, cloud key leak). Step lists, not prose. |

Mixing them is the commonest failure: a 60-page plan nobody reads during an incident.

## Plan skeleton
1. Purpose and scope (entities, subsidiaries, cloud tenants, OT; what is out of scope).
2. Authority: quote the policy clause that lets the incident commander take systems offline.
3. Definitions: event, alert, incident, breach (breach is a *legal* term; only counsel declares it).
4. Roles: incident commander, technical lead, scribe, comms lead, legal, HR, exec sponsor
   (see computing-software.digital-forensics-incident-response.incident-response-process.ir-roles-and-raci).
5. Severity matrix and SLAs (time to acknowledge, to bridge, to exec notification).
6. Escalation tree with **24x7 phone numbers**, deputies, and the out-of-band channel.
7. Third parties: retainer firm, cyber insurer hotline (call them *before* hiring anyone),
   outside counsel, MSSP, cloud providers' support case process.
8. Evidence handling expectations (chain of custody, who images).
9. Communications: internal, customers, regulators, media; who approves wording.
10. Post-incident review requirement and metrics.
11. Maintenance: owner, review cadence, change log, tabletop test at least yearly.

## Approval path
Draft, IR team review, legal (privilege, notification wording), privacy officer, CISO
sign-off, executive sponsor or risk committee acknowledgement. Record version and approval
date in the header; auditors (ISO 27001 A.5.24-5.28, SOC 2 CC7.3-7.5, PCI DSS 12.10) look for
evidence of approval and an annual test.

## Gotchas
- Keep the contact list as a separate annex so updating a phone number does not need a
  full re-approval.
- Print it. A plan stored only on the file server that just got encrypted is useless; keep
  a copy offline and in the jump kit.
- Do not promise timelines you cannot meet ("contain within 1 hour"); they become evidence
  against you in litigation.
- Make the incident commander role explicitly separate from the most senior technician.

## Verify
Run a tabletop against the plan; every inject should be answerable by pointing to a section.
Anything answered with "we'd figure it out" is a plan gap.

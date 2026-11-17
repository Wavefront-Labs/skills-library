---
id: computing-software.cybersecurity-defensive.security-operations.incident-response-plan
name: incident-response-plan
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, incident-response-plan, nist-800-61, ir-roles, raci, playbooks, csirt, ir-program]
level: practitioner
status: docs-checked
description: "Write and maintain an incident response plan: scope, roles and RACI, declaration criteria, communication paths, playbook set, contact lists and review cadence."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident response plan and roles

**Goal:** a short, usable plan that tells people at 3am who decides, who to call and what
to do first. NIST SP 800-61r3 maps IR onto CSF 2.0: Govern, Identify and Protect cover preparation and lessons learned; Detect, Respond and Recover cover the response.

## Contents (keep playbooks separate)
1. **Purpose and scope:** systems, subsidiaries, cloud tenants, third parties covered.
2. **Definitions:** event, alert, incident, breach; severity levels (link the severity matrix).
3. **Roles (RACI):**
   - Incident commander (IC): runs the response, owns decisions and the timeline.
   - Technical lead(s): investigation and containment.
   - Communications lead: internal/exec updates, customer and media with PR.
   - Legal/privacy: privilege, regulatory and contractual notification decisions.
   - Executive sponsor: business decisions (shutdowns, ransom stance, spending).
   - Scribe: decision and action log.
   - IT operations, HR, facilities, external IR retainer, cyber insurer as needed.
   Name primary and backup for each with out-of-hours contact.
4. **Declaration and escalation:** who can declare, criteria, escalation times by severity.
5. **Communication:** war room channels including an out-of-band option (if email/chat may be
   compromised), update cadence, approved templates.
6. **Phases:** preparation, detection and analysis, containment, eradication, recovery,
   post-incident; with authority statements (e.g. the IC may isolate any system without
   change approval).
7. **Evidence handling and chain of custody.**
8. **External parties:** IR retainer number, insurer hotline, law enforcement contacts, regulators and their deadlines.
9. **Playbook index:** ransomware, BEC, account compromise, malware outbreak, data
   exfiltration, insider, DDoS, cloud tenant compromise, third-party breach.
10. **Maintenance:** owner, review periodically and after major incidents (NIST: revisit plans periodically or when a need arises).

## Make it usable
- One-page quick reference card: declare, call list, first five actions, war room bridge.
- Store copies offline/out-of-band (printed, or a separate tenant); ransomware can take
  out the wiki that holds the plan.
- Pre-authorise actions so responders do not wait for change boards.

## Gotchas
- Plans written for auditors (long, generic) are ignored during incidents.
- Stale contact lists are the most common failure; verify them on a set schedule.
- Legal must be involved before external communications and before writing conclusions in
  shared channels.

## Verify
A tabletop run using only the plan and call list: participants find roles, contacts and
first actions without asking the author.

## Checked
2026-11-01. Confirmed against NIST SP 800-61r3 (CSF 2.0 function mapping, roles incl. legal, periodic review and exercises) and the CISA Federal Government Incident and Vulnerability Response Playbooks (phases: preparation, detection and analysis, containment, eradication and recovery, post-incident; out-of-band communications; law enforcement). Removed: the 15-page length figure, the annual review figure, the quarterly contact check, and the insurer-hotline rule, which those documents do not state. The CIS source was not read and was dropped.
Method: documentation only; no commands were run.

---
id: computing-software.digital-forensics-incident-response.incident-response-process.reviewing-and-updating-the-ir-plan
name: reviewing-and-updating-the-ir-plan
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ir-plan-review, incident-response-plan, ir-plan, dfir, nist-800-61]
level: practitioner
status: draft
description: "Run the annual and post-incident review of the IR plan: triggers, what to re-test, contact validation, version control and sign-off."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing and updating the IR plan

**Goal:** keep the incident response plan true to the organisation as it is today, not as it was
when someone wrote it. SP 800-61r3 places this under Improvement (ID.IM): lessons from incidents,
exercises and assessments feed back into policy, plan and procedures.

## Review triggers (write them into the plan itself)
- Calendar: at least annually, signed off by the plan owner (usually CISO).
- After every Sev-1/Sev-2 incident and every tabletop or purple-team exercise.
- Organisational change: merger, new cloud tenant, new outsourced SOC/MSSP, new regulator.
- Technology change: EDR swap, SIEM migration, identity provider change, new backup platform.
- Legal change: new notification law or sector rule (NIS2, SEC 8-K, CIRCIA, state laws).

## Review checklist
1. **Contacts:** dial every number in the call tree and escalation matrix; confirm out-of-band
   channels (Signal group, bridge line) still work. Stale contacts are the most common failure.
2. **Roles:** RACI still maps to real job titles; deputies named for every role.
3. **Severity matrix:** compare last year's incidents against it; were any mis-rated?
4. **Authority:** delegated authority to isolate hosts, disable accounts and engage retainers is
   still signed by the right executive.
5. **Tooling:** EDR console access, Velociraptor/KAPE availability, forensic licences, break-glass
   accounts tested (log in, then rotate).
6. **Third parties:** retainer hours, insurer panel requirements, law firm contact, MSSP SLAs.
7. **Regulatory clock table:** each notification deadline and who decides.
8. **Playbooks:** every playbook referenced still exists and was exercised in the last 12 months.

## Version control
- Keep the plan in a document system with version history; record version, date, changes,
  approver on a change-log page at the front.
- Distribute a printed / offline copy to the core team; the plan must be readable when the
  network and SSO are down.
- Retire old copies explicitly (announce the new version number).

## Gotchas
- Reviewing only the prose and never re-testing the contacts and accesses.
- Plans that name individuals instead of roles go stale within months.
- Not routing lessons-learned action items into the plan review means the same gap recurs.

## Verify
A random responder can find the current version offline, reach every listed contact, and the
change log shows the last incident's lessons reflected.

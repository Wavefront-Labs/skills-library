---
id: computing-software.digital-forensics-incident-response.incident-response-process.declaring-an-incident
name: declaring-an-incident
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [incident-declaration, incident-triage, case-management, nist-sp-800-61, dfir]
level: practitioner
status: draft
description: "Declare an incident and open the case: declaration criteria, the first 30 minutes checklist, initial notifications, and preserving the evidence trail."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/61/r2/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Declaring an incident

**Goal:** move from "investigating an alert" to "running an incident" deliberately, with a
time-stamped declaration that starts the clocks (regulatory, SLA, insurance).

## Declare when
- The severity matrix says SEV3 or above, or
- Confirmed unauthorised access, malware execution, or data exposure, or
- The validating analyst cannot rule out compromise of a critical asset within the triage window.
Declaring and later downgrading is cheap; declaring late is expensive.

## First 30 minutes
1. **Open the case**: ID, codename, declared time (UTC), declarer, initial severity,
   classification, one-paragraph summary.
2. **Assign IC** and technical lead; open the bridge (out of band if identity/mail may be
   compromised).
3. **Preserve**: stop any automated reimaging/cleanup on affected hosts; extend log
   retention; snapshot cloud resources; capture memory on key hosts before containment.
4. **Initial scoping questions**: what assets, what accounts, since when, still active?
5. **Notify** per plan: IR lead, legal (starts privilege), CISO; insurer if the policy
   requires prompt notice (often "as soon as practicable").
6. **Start the scribe log**: every action with time, actor, host, and result.
7. Set the next sync time.

## Regulatory clocks often start at "awareness"
GDPR 72 h from awareness of a personal data breach; NIS2 early warning 24 h; DORA initial
notification 4 h after classification as major; SEC 8-K 4 business days after materiality
determination. Record when you became aware of what; counsel decides when clocks start.

## Gotchas
- Do not alert the attacker: no mass password reset or host reimage on declaration unless
  the attack is actively destructive.
- Avoid the word "breach" in the case title.

## Verify
At closure, check the declaration time against the first alert; long gaps feed the
alert-validation improvement backlog.

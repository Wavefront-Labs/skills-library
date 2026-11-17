---
id: computing-software.digital-forensics-incident-response.incident-response-process.incident-lifecycle-playbook
name: incident-lifecycle-playbook
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [incident-response, ir, incident-lifecycle, nist-sp-800-61, picerl, preparation, detection, triage, containment, eradication, recovery, lessons-learned, postmortem, incident-commander, severity, scoping, communications, playbook, csirt, soc, ransomware, business-email-compromise, dfir]
level: practitioner
status: draft
description: "Run a security incident end to end: declare and staff it, scope before containing, contain without tipping off, eradicate, recover with monitoring, run the review."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.sans.org/white-papers/33901/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident lifecycle playbook

**Goal:** turn "something looks wrong" into a controlled response with clear roles, a
scoped understanding of the intrusion, containment that actually holds, and a review
that changes something. Tool-agnostic.

The classic phases (NIST SP 800-61 / SANS PICERL) are Preparation, Identification,
Containment, Eradication, Recovery, Lessons learned. NIST's 2025 revision (r3) re-maps
these onto the CSF 2.0 functions; the practical work below is the same either way.

## Preparation (before anything happens)
- Contact list that works when email/SSO is compromised: phone numbers, an
  **out-of-band chat channel**, legal, comms, execs, cyber-insurer hotline, external
  IR retainer.
- Logging you will need: endpoint telemetry (EDR), authentication logs, DNS, proxy,
  cloud audit logs — with retention ≥ 90 days (intrusions are often found weeks late).
- Pre-approved authority: who may isolate a host, disable an account, take a
  production system offline, without a meeting.
- Tested backups that are offline or immutable (ransomware deletes reachable ones).

## Declare and staff (first 30 minutes)
1. **Declare** an incident with a severity (e.g. SEV1 = active attacker/data loss/major
   outage, SEV3 = contained single-host malware). Over-declaring and downgrading is cheap.
2. Assign an **Incident Commander** (coordinates, decides, does not do forensics), a
   **technical lead**, a **scribe** (timestamped log of every action and finding, UTC),
   and a **comms lead**.
3. Open the case log and a fixed cadence of updates (e.g. every 60 min for SEV1).
4. Bring in legal early if personal data, regulated systems or law enforcement may be
   involved — notification clocks (e.g. GDPR's 72 hours from awareness) may start now.

## Identification and scoping — before you contain
- Preserve volatile evidence from key hosts **first** (memory, running processes,
  network connections) — see
  computing-software.digital-forensics-incident-response.evidence-handling.forensic-acquisition-and-chain-of-custody.
- Build the picture: patient zero, initial access vector, accounts used, hosts touched,
  persistence, data accessed. Pivot every indicator (IP, hash, account, domain) across
  all telemetry (see
  computing-software.digital-forensics-incident-response.log-analysis.windows-event-log-threat-hunting).
- The core trade-off: **contain too early** and the attacker, still holding other
  footholds, switches tactics and you lose visibility; **contain too late** and damage
  grows. Active destruction (ransomware encrypting, data leaving now) → contain
  immediately. Quiet espionage → scope first, then contain everything at once.

## Containment
- Short-term: network-isolate hosts via EDR (keeps them powered for forensics),
  block IOCs at egress, disable/reset compromised accounts, **revoke sessions and
  tokens** (password resets alone don't kill OAuth refresh tokens or cookies).
- Coordinated: do account resets, host isolation and firewall blocks in the same
  window so the attacker can't use one foothold to rebuild another.
- Assume the attacker reads your email: discuss the response on the out-of-band channel.

## Eradication
- Remove every persistence mechanism found (scheduled tasks, services, Run keys,
  web shells, new accounts, mailbox rules, OAuth app grants), close the initial vector
  (patch, MFA, config), and **rebuild** rather than clean compromised servers where possible.
- If a domain controller was compromised, plan a krbtgt double reset (two resets, spaced
  by more than the ticket lifetime) and review all privileged accounts.

## Recovery
- Restore from known-good backups dated before the earliest intrusion evidence.
- Return systems in stages under heightened monitoring (detections for the exact
  IOCs and TTPs seen) for at least a few weeks; re-entry attempts are common.
- Define "recovered" up front: business owner signs off, monitoring shows no recurrence.

## Lessons learned (within ~2 weeks)
Blameless review: timeline (detect time, contain time, recover time), what worked,
what slowed you, root cause, and **owned action items with dates**. A review with no
tracked actions didn't happen.

## Verify
- [ ] Roles named and the scribe's UTC log exists from minute one.
- [ ] Volatile evidence preserved before containment actions.
- [ ] Containment executed as one coordinated step, including token/session revocation.
- [ ] Every found persistence item has an eradication record.
- [ ] Post-incident actions have owners and due dates.

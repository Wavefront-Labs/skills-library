---
id: computing-software.cybersecurity-defensive.security-operations.incident-response-coordination
name: incident-response-coordination
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, ir, soc, nist-800-61, incident-commander, containment, containment-strategy, eradication, recovery, lessons-learned, comms-plan, legal-hold, chain-of-custody, war-room, severity-matrix, breach-notification]
level: advanced
status: docs-checked
description: "Run an active incident from declaration to closure: incident commander role, containment-before-eradication order, comms discipline, evidence handling and post-incident review."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Incident response coordination — run the room, not just the box

**Goal:** take a confirmed incident from declaration to closure without losing
evidence, without leaking status to the wrong channel, and with the business
decisions (isolate a revenue system? notify customers?) made by the people who own
that risk, not by whoever is on shift.

## 1. Declare and assign roles
Declaring is a decision, not a vibe — use a written trigger (confirmed malicious
activity with lateral movement, data exfiltration, ransomware behaviour, or anything
Tier 1 escalated as "undetermined, high confidence bad"). On declaration, name an
**incident commander (IC)** — one person, not a committee, who owns the decision
log and the next update time. The IC is not automatically the most senior security
person; it's whoever runs the process best. Technical lead(s), comms lead, and a
scribe are separate roles even if doubled up in a small team.

## 2. Contain before you eradicate
Order matters: **scope → contain → eradicate → recover**. CISA warns that some
adversaries watch defensive measures and shift methods to evade containment, so build
as complete a picture as possible to avoid "tipping off" the adversary, while weighing
the risk of letting them persist until scope is known. When choosing a course of
action, weigh mission and service impact, duration and effectiveness (full vs partial
containment), and the effect on evidence. Typical activities: isolate systems or
segments, update firewall filtering, block unauthorised access and malware sources,
change admin passwords and rotate keys where compromise is suspected. If new signs of
compromise appear, go back and re-scope. Never let the first
analyst on scene unilaterally reset all domain admin passwords — that is a
business decision with outage impact; the IC authorises it.

## 3. Comms discipline
Run incident comms on a channel the attacker cannot plausibly read (not the
general IT Slack if the attacker has mailbox/Teams access — assume compromised
accounts can read anything they're a member of). Status updates go out on a fixed
cadence to a named list, written by the IC or comms lead,
never ad hoc from whoever has news. Decide legal and
notification involvement early for anything touching regulated data: NIST SP 800-61r3
expects legal to be consulted on incidents with legal ramifications, and notification
deadlines come from the laws and contracts that apply (check them with counsel, do not
assume a window).

## 4. Evidence and chain of custody
Image or snapshot before you remediate a host wherever feasible (disk image or at
minimum memory capture + key logs) — rebuilding first destroys the only record of
how they got in. Log who collected what, when, and where it's stored; label it in
case of later legal action or insurance claim. A spreadsheet with
`artefact | collected_by | timestamp | hash | storage_location` beats nothing.

## 5. Recovery and closure
Don't restore from backup until you know the backup predates compromise and the
entry vector is closed — restoring into the same hole reinfects. Recovery is phased
(critical systems first, verified clean, then the rest), with heightened monitoring
on recovered systems. Close the incident only when the IC
signs off against written exit criteria (vector closed, persistence removed,
monitoring confirms no recurrence for an agreed window).

## 6. Post-incident review
Run a lessons-learned review with everyone involved (both CISA and NIST call for it). Timeline (detection → declaration
→ containment → recovery, with timestamps), what worked, what didn't, and concrete
actions with owners and dates — not just "communication could be better." Feed
detection gaps straight to detection engineering and vulnerability management as
tracked tickets, not a line in a report nobody reopens.

## Gotchas
- Using the compromised network's own tools (RDP, PsExec, admin shares) to
  investigate hands the attacker a live feed of your response — use out-of-band
  access (EDR console, OOB management network) wherever possible.
- A "quiet" period after initial containment is not confirmation the attacker is
  gone; CISA's step is to confirm no new signs of compromise before moving on.
- Mixing IC and hands-on-keyboard technical work in one person creates a
  bottleneck and blind spots; split the roles even under pressure.
- Skipping the legal/privacy conversation because "it's probably not reportable"
  is itself a liability — get the call made by someone qualified to make it.

## Verify
- [ ] An IC was named in writing at declaration, with a decision log.
- [ ] Containment order followed scope-confirm-before-isolate for multi-host incidents.
- [ ] Evidence was collected (image/memory/logs) with custody recorded before remediation.
- [ ] Comms ran on a channel assumed safe from the attacker, on a fixed cadence.
- [ ] Recovery verified the entry vector was closed before restoring from backup.
- [ ] A post-incident review produced owned, dated action items.

Related: computing-software.cybersecurity-defensive.security-operations.alert-triage,
computing-software.cybersecurity-defensive.security-operations.threat-hunting-methodology,
computing-software.cybersecurity-defensive.endpoint-security.edr-deployment-and-tuning

## Checked
2026-11-01. Confirmed against the CISA Federal Government Incident and Vulnerability Response Playbooks (containment considerations and activities, tipping off, forensic images, out-of-band communication, reimage from clean backups, lessons learned) and NIST SP 800-61r3 (legal role, lessons learned). Removed: the 30-60 minute cadence, the 72-hour notification claim, the two-week review window, the days-to-weeks monitoring claim, the dormant-actor claim and the 2-of-10 hosts heuristic, none of which those documents state.
Method: documentation only; no commands were run.

---
id: computing-software.cybersecurity-defensive.security-operations.alert-triage
name: alert-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [security-operations, soc, alert-triage, incident-triage, siem, soar, true-positive, false-positive, benign-true-positive, severity, escalation, playbooks, runbooks, enrichment, alert-enrichment, case-management, mttd, mttr, alert-fatigue, nist-800-61, splunk, sentinel, edr, case-notes]
level: practitioner
status: draft
description: "A repeatable SOC triage loop: scope the alert, enrich, classify TP/BTP/FP, decide severity and escalation, document, and feed tuning back to detection."
sources: ["NIST SP 800-61 Rev. 3 - Incident Response Recommendations", "MITRE ATT&CK Enterprise matrix", "SANS Incident Handler's Handbook", "CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Alert triage — decide fast, decide right, leave a trail

**Goal:** take any alert from queue to a defensible decision (close, contain,
escalate) in a consistent time, with notes another analyst could pick up, and turn
every false positive into a tuning request.

## 1. Before you open it: queue order
Work by severity × asset criticality, then age. A medium alert on a domain controller
outranks a high on a kiosk. Set targets per severity and measure them (example
starting points, set your own: critical acknowledged in 15 min, high in 1 h,
medium same shift). Claim the alert in the case tool so no one duplicates work.

## 2. Read the alert properly (5 minutes)
Answer, in writing, in the case:
- **What fired and why** — open the rule logic. What exact condition matched?
- **Who / what / where / when** — user, host, process, source/destination IP, time in UTC.
- **What ATT&CK technique** the rule claims, and is the evidence actually that?
- **Is it still happening?** Check the last hour, not just the triggering event.

## 3. Enrich
- **Identity:** role, department, manager, privileged? Recent password reset or MFA
  registration? Travel/VPN usual pattern?
- **Asset:** owner, criticality, internet-facing, EDR present, last patch.
- **Artefacts:** hash, domain, IP reputation (VirusTotal, internal TI platform),
  first-seen in your environment (prevalence — one host or 500?).
- **Timeline:** pivot ±30 minutes around the event on the same host and user: process
  tree, network connections, logons (Windows 4624/4625/4648/4672), file writes.
Rarity in *your* environment beats global reputation: a clean-reputation binary seen
on one host only, run from `%AppData%`, deserves a look.

## 4. Classify
- **True positive (malicious):** proceed to containment/escalation.
- **Benign true positive:** the rule worked, the activity is authorised (admin ran
  PsExec in a change window). Close with the evidence of authorisation (change ticket).
- **False positive:** the rule matched something it shouldn't. Close and file tuning.
- **Undetermined:** you can't decide within the time box → escalate, don't close.
Never close on "user said it was them" alone for credential-related alerts — verify
through a second channel (call the known number, check the device).

## 5. Severity and escalation
Score on impact and confidence: privileged account, sensitive data, multiple hosts,
active C2 or lateral movement → incident. Escalation path: Tier 2/IR on-call, with
the case link. Containment you may take at Tier 1 should be written in the playbook
(e.g. isolate a workstation in EDR, disable a user, revoke sessions), with a rule for
servers (owner approval first unless ransomware behaviour is seen).

## 6. Document (template)
```
Summary: <one line verdict>
Evidence: <queries run + key results, links>
Entities: user=<>, host=<>, ip=<>, hash=<>
Classification: TP | BTP | FP | Undetermined
Actions taken: <isolation, resets, time UTC>
Tuning request: <rule id, proposed exclusion with owner/expiry> | none
```
Save the exact queries; "checked logs, nothing found" is not evidence.

## 7. Feed back
Weekly: FP rate per rule, time-to-triage, top noisy entities. Rules with an FP rate
above an agreed threshold go to detection engineering with your notes. Automate the
enrichment you repeat (SOAR playbook: auto-pull user/asset/hash context into the case).

## Gotchas
- Time zones: SIEM shows local, EDR shows UTC — normalise before building a timeline.
- Deduplicated/throttled alerts hide repeats; look at the raw events behind the alert.
- An alert on host A is often the *second* stage; check what happened on the source
  of the logon or the parent process.
- Isolating a host tips off a hands-on-keyboard attacker; for suspected intrusion,
  coordinate scope with IR before containment.
- Closing as FP without a tuning request guarantees the same alert tomorrow.

## Verify
- [ ] The case records rule logic, entities, time window and queries run.
- [ ] Classification is one of TP/BTP/FP/Undetermined with supporting evidence.
- [ ] Benign TPs cite an authorisation (change ticket, owner confirmation).
- [ ] Escalations reached the on-call within the severity target.
- [ ] Every FP produced a tuning request with an owner.

Related: computing-software.cybersecurity-defensive.splunk.spl-detection-searches,
computing-software.cybersecurity-defensive.endpoint-security.edr-deployment-and-tuning

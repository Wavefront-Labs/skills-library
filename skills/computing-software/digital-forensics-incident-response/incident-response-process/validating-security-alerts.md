---
id: computing-software.digital-forensics-incident-response.incident-response-process.validating-security-alerts
name: validating-security-alerts
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [alert-validation, incident-triage, false-positive, true-positive, soc, dfir]
level: practitioner
status: draft
description: "Validate a security alert as true or false positive quickly: context gathering, corroboration across sources, common benign explanations and escalation criteria."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Validating security alerts

**Goal:** within minutes, decide whether an alert is malicious, benign-true-positive
(real activity, authorised), or false positive, and record why.

## Triage loop
1. **Read the rule**: what logic fired, on which fields? Many "false positives" are analysts
   misunderstanding the detection.
2. **Context**: asset (criticality, owner, role), user (privileged? on leave? new joiner?),
   time (business hours, user's time zone), prior alerts on the same entity (30 days).
3. **Corroborate** with an independent source:
   - Endpoint alert: EDR process tree, parent/child, command line, signer, file prevalence.
   - Identity alert: sign-in logs (IP, ASN, device, MFA result), whether the user confirms.
   - Network alert: DNS/proxy for the same host, destination reputation, first seen date.
4. **Benign explanations** to rule out: IT admin tools (PsExec, PowerShell remoting by the
   helpdesk), vulnerability scanners, pen test (check the authorised schedule), backup
   software touching every file, software deployment (SCCM/Intune), VPN egress making
   "impossible travel".
5. **Decide** and document: verdict, evidence, and reasoning in the ticket.

## Escalate to an incident when
- Execution confirmed from an unexpected source (user-writable path, Office child process).
- Credential use from attacker infrastructure or confirmed by the user as not theirs.
- Multiple stages correlate (phish click, then new process, then outbound to new domain).
- Any alert on a domain controller, IdP, or backup system that is not explained in 15 min.

## Tuning feedback
Each false positive gets a tuning ticket with the exact exclusion proposed (field + value +
reason). Exclusions by user or host only, never by whole command line pattern without review.

## Verify
Sample 10 closed alerts weekly for peer review; disagreement rate is the quality metric.

---
id: computing-software.digital-forensics-incident-response.incident-response-process.prioritizing-concurrent-incidents
name: prioritizing-concurrent-incidents
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [incident-prioritization, triage, severity, resource-allocation, nist-sp-800-61, dfir]
level: practitioner
status: draft
description: "Prioritize concurrent incidents by functional impact, information impact and recoverability, and reallocate responders when a bigger incident lands."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prioritizing concurrent incidents

**Goal:** with limited responders and several open incidents, work the ones that reduce the
most business risk first, and be able to justify the choice.

## Factors (NIST SP 800-61r2 3.2.6)
- **Functional impact**: current and *likely future* effect on business functions.
- **Information impact**: confidentiality, integrity, availability of data; regulated data.
- **Recoverability**: time and resources to recover; whether recovery is possible at all.
Plus: attacker activity (active hands-on-keyboard beats a dormant commodity infection),
spread potential (a worm or domain admin compromise beats a single workstation), and
external clocks (regulatory deadlines, extortion deadlines).

## Practical ranking
1. Active attacker with privileged access or destructive intent (ransomware staging).
2. Confirmed data exfiltration in progress.
3. Compromise of identity infrastructure (DC, IdP, PAM, backup console).
4. Single-system compromises with sensitive data.
5. Contained commodity malware, policy violations.

## Reallocation
- IC of the bigger incident requests people via the IR lead; the smaller incident gets a
  documented "holding state" (containment applied, evidence preserved, next steps listed).
- Check for **linkage**: concurrent incidents are often one intrusion. Compare IOCs, accounts
  and timeframes before treating them separately.
- Communicate the deprioritisation to the affected business owner.

## Gotchas
- Priority by who shouts loudest (VIP mailbox) rather than impact.
- Forgetting to revisit: re-rank at every daily review.

## Verify
At weekly review, check whether any lower-priority incident escalated because it was parked;
if so, the holding-state criteria were too loose.

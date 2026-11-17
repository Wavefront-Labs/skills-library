---
id: computing-software.digital-forensics-incident-response.incident-response-process.defining-intelligence-requirements-for-an-incident
name: defining-intelligence-requirements-for-an-incident
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [intelligence-requirements, pir, cyber-threat-intelligence, intelligence-cycle, dfir]
level: practitioner
status: draft
description: "Define priority intelligence requirements (PIRs) for an incident: turn stakeholder decisions into answerable questions, task collection and report against them."
sources: ["https://www.first.org/global/sigs/cti/curriculum/", "https://csrc.nist.gov/pubs/sp/800/150/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining intelligence requirements (PIRs) for an incident

Without requirements, threat-intel support during an incident becomes a pile of IOCs and actor profiles nobody asked for. PIRs tie intel work to decisions the incident commander and executives must make.

## From decisions to questions
| Decision owner | Decision | PIR |
|---|---|---|
| Incident commander | Is containment complete? | What other infrastructure and tooling does this actor use that we have not yet searched for? |
| CISO | Will they come back? | Does this actor re-target victims after remediation, and through which access vectors? |
| Legal / exec | Pay, notify, disclose? | Does this group exfiltrate before encryption and publish on a leak site? Are they sanctioned? |
| SOC | What to watch? | Which TTPs would indicate a second-stage operation in the next 30 days? |

Each PIR breaks into specific intelligence requirements and then collection tasks, e.g. "Pivot on the C2 IP's TLS certificate and JARM for sibling servers", "Review vendor reports on the ransomware affiliate for initial-access methods".

## Writing good PIRs
- Answerable and time-bound: "within 48 hours".
- One decision per PIR; avoid "tell us everything about APT-X".
- Ranked: the commander sets priority; collection effort follows the rank.
- State the confidence level needed and the sources allowed (internal telemetry, commercial feeds, sharing communities under TLP).

## Running it
1. Draft PIRs at the first intel sync after declaration; get the commander to approve them.
2. Track each PIR with status, current answer, confidence (estimative language) and sources.
3. Report against PIRs in every update; when a PIR is answered, close it and say so.
4. Revisit as the incident evolves; new decisions need new PIRs.

## Gotchas
- Attribution is rarely a decision driver; do not let actor naming consume analyst time unless a decision depends on it (sanctions checks do).
- Intelligence from sharing groups carries TLP; respect it when briefing.

## Verify
Every intel product in the case cites the PIR it answers, and each open PIR has an owner and due time.

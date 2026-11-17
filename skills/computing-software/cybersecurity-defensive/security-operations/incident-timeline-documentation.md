---
id: computing-software.cybersecurity-defensive.security-operations.incident-timeline-documentation
name: incident-timeline-documentation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-reporting, incident-timeline, timeline-analysis, utc, evidence-references, timesketch, attack-timeline, response-timeline]
level: practitioner
status: draft
description: "Keep two incident timelines (attacker activity and response actions) with UTC times, sources, confidence and evidence references, so reports and regulators get facts."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://timesketch.org/", "https://www.sans.org/white-papers/incident-handlers-handbook/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident timeline documentation

Every incident report, regulator notification and lessons-learned review is built from the
timeline. Start it in the first hour and keep it current.

## Two timelines
1. **Attacker (event) timeline**: what happened on systems.
2. **Response (decision) timeline**: when the incident was detected, declared, escalated, who
   decided what, containment actions, notifications sent. Regulators and lawyers ask about this one.

## Columns
| Time (UTC) | Host/account | Activity | Source artefact | Evidence ref | Confidence | Analyst | ATT&CK |
- Always UTC with timezone stated; convert local-time sources explicitly and note the offset used.
- Evidence ref points to the exhibit (image hash, log export file, ticket attachment) so every
  line can be re-verified.
- Confidence: confirmed (direct artefact), likely (strong inference), possible.
- Separate fact from interpretation: "4624 type 10 from 203.0.113.5 as svc_backup" (fact) vs
  "attacker used stolen svc_backup credentials" (assessment).

## Tools
- A shared spreadsheet works for small cases (lock edits to responders).
- **Timesketch** for large cases: import Plaso super-timelines, Hayabusa JSONL, CSV exports; tag and
  star events; saved views per question; stories for the narrative.
- Case management (TheHive, ServiceNow SIR) task logs for the response timeline.

## Practices
- Key milestones to always capture: initial access, first malicious execution, privilege
  escalation, lateral movement start, data access/exfil, impact, detection, containment,
  eradication, recovery.
- Dwell time = detection - initial access; time to contain = containment - detection.
- Mark gaps ("no logs for 2026-09-02 to 09-05 on FS01: log rollover") rather than leaving silence.
- Version the timeline; findings change as evidence arrives.

## Gotchas
- Clock skew between systems: check each host's time offset (NTP status, event times vs DC times)
  and record corrections.
- Copy-pasting times from UIs that show local time is the most common error.
- Over-detailed timelines bury the story; keep a summary timeline (20-40 lines) for reports.

## Verify
Peer review: pick five random entries and re-derive them from the referenced evidence; all should
match, including the UTC conversion.

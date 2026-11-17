---
id: computing-software.digital-forensics-incident-response.incident-response-process.maintaining-the-master-incident-timeline
name: maintaining-the-master-incident-timeline
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [incident-timeline, incident-documentation, timeline, attack-timeline, dfir]
level: practitioner
status: draft
description: "Maintain the master incident timeline that merges findings from every analyst: format, time normalisation, confidence, sourcing and how it feeds the report."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.sans.org/white-papers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maintaining the master incident timeline

**Goal:** one authoritative, sourced chronology of attacker and responder activity that every
analyst updates and the final report is built from. This is distinct from a super-timeline
(millions of raw events); the master timeline is curated, typically 50-500 rows.

## Columns
| Column | Example |
|---|---|
| Time (UTC) | 2026-09-02T03:14:07Z |
| Time precision / confidence | exact / approx (+/- 1h) / inferred |
| Host / account / asset | WKS-0142 / jdoe |
| Activity | rundll32 executed payload from Temp |
| ATT&CK technique | T1218.011 |
| Evidence source | Prefetch RUNDLL32.EXE-xxxx.pf; EDR process event |
| Evidence ID | EVID-007 |
| Analyst | CJ |
| Type | attacker / responder / business |

## Rules
- **Normalise to UTC** at entry. Record source time zone and known clock skew per host.
- Every row cites its evidence; no row without a source.
- Distinguish facts from inferences (confidence column). Inferred rows are coloured.
- Keep responder actions in the same timeline (isolation, password resets) so you can tell
  attacker activity from your own after containment.
- One owner (usually the scribe or tech lead) merges contributions; analysts submit rows.

## Tooling
A shared spreadsheet works; Timesketch or a case platform (IRIS, TheHive) for larger teams.
Export to CSV for the report and visualise (swimlane per host) for executives.

## Uses
- Defines dwell time (first attacker row) and scope (all hosts/accounts mentioned).
- Exposes gaps: long silent periods are either attacker dormancy or missing visibility.
- Feeds lessons learned: detection opportunities per stage.

## Verify
Sort by time and read it aloud as a story; each transition between rows should be
explainable. Unexplained jumps are your next investigative questions.

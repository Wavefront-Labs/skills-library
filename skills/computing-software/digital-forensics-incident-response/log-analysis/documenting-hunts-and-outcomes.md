---
id: computing-software.digital-forensics-incident-response.log-analysis.documenting-hunts-and-outcomes
name: documenting-hunts-and-outcomes
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [hunt-report, threat-hunting, hypothesis-driven-hunting, peak-framework, dfir]
level: practitioner
status: draft
description: "Document a threat hunt so it is repeatable and measurable: hypothesis, data and queries, results, findings, gaps, detections created and hunt metrics."
sources: ["https://www.splunk.com/en_us/blog/security/peak-threat-hunting-framework.html", "https://www.betaalvereniging.nl/en/safety/tahiti/", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Documenting hunts and outcomes

**Goal:** a hunt with no record cannot be repeated, audited or turned into detections. Use a
consistent hunt report (PEAK's Act/Knowledge phases emphasise documenting and preserving knowledge).

## Hunt record template
| Section | Content |
|---|---|
| ID, title, hunter(s), dates | HUNT-2026-031 "Rclone-style exfil from servers" |
| Type | Hypothesis-driven / baseline / model-assisted (PEAK) |
| Hypothesis | "Adversaries use renamed rclone on file servers to exfiltrate to cloud storage (T1567.002)" |
| Scope | Assets, time window, data sources and their coverage % |
| Data and queries | Exact queries (SPL/KQL/VQL) with links, versions, run times |
| Results | Counts, notable outliers, screenshots of key stacks |
| Findings | Malicious / suspicious-unresolved / benign explained; incidents opened (IDs) |
| Gaps | Missing telemetry, retention limits, parsing issues found |
| Outputs | Detections created/updated, playbook changes, logging changes requested |
| Next steps | Re-run cadence, follow-up hunts |

## Metrics to roll up
- Hunts completed, incidents found, detections created, telemetry gaps closed, time per hunt.
- Coverage: ATT&CK techniques hunted in the last 12 months (Navigator layer).

## Practice
- Write the hypothesis and scope before querying; record negative results - "not found with this data" is valuable.
- Store queries in version control; parameterise for re-runs.
- Link hunt outputs to the detection backlog and logging backlog tickets.

## Gotchas
- Reports that only list "nothing found" without coverage numbers give false comfort.
- Ad hoc query edits not saved back into the report break repeatability.

## Verify
Another analyst can re-run the hunt from the record alone and get comparable results.

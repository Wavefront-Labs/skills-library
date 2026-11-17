---
id: computing-software.digital-forensics-incident-response.incident-response-process.turning-incident-findings-into-control-improvements
name: turning-incident-findings-into-control-improvements
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [control-improvements, lessons-learned, detection-engineering, risk-register, continuous-improvement, dfir]
level: practitioner
status: draft
description: "Turn incident findings into tracked control and detection improvements: action items, ATT&CK-mapped detections, risk register entries and closure verification."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Turning incident findings into control improvements

**Goal:** every incident leaves the organisation measurably harder to attack the same way.
NIST SP 800-61r3 frames this as CSF ID.IM (improvement) feeding back into Govern and Protect.

## From finding to action
| Finding type | Typical action |
|---|---|
| Missing preventive control | Project to implement (MFA on VPN, application allowlisting) |
| Misconfigured control | Config change with verification test |
| Missed detection | New/tuned detection rule mapped to ATT&CK technique, tested |
| Log gap | Onboard source, extend retention |
| Process failure | Plan/playbook update, training, staffing change |
| Third-party weakness | Contract or access change |

## Action item format
ID, finding reference, action, owner (named person), due date, priority (risk-based),
verification method, status. Track in the risk register or GRC tool, not only in the report.

## Detection improvements
- For each attack stage in the timeline, write or tune a detection, test it with the
  incident's real artefacts or an Atomic Red Team test, and record the ATT&CK ID.
- Update the detection coverage map (e.g. ATT&CK Navigator layer) so gaps are visible.

## Governance
- Report open actions monthly to the security steering group; overdue high-priority items
  escalate to the risk owner.
- Risk acceptance must be explicit and signed when an action is declined.

## Verify
Close an action only when its verification passed (control test, detection fired, log
visible). At the next tabletop, replay the incident and check each improvement would have
changed the outcome.

---
id: computing-software.digital-forensics-incident-response.incident-response-process.turning-incident-ttps-into-detections
name: turning-incident-ttps-into-detections
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [incident-to-detection, lessons-learned, detection-engineering, sigma, dfir]
level: advanced
status: draft
description: "Convert each technique observed in an incident into tested detections: ATT&CK mapping, telemetry check, Sigma rule, replay test and deployment tracking."
sources: ["https://attack.mitre.org/", "https://github.com/SigmaHQ/sigma-specification", "https://github.com/redcanaryco/atomic-red-team"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Turning incident TTPs into detections

**Goal:** the best detection backlog is your own incident. For every attacker step, ask why it
was not detected sooner and fix that.

## Process
1. **Extract steps** from the master timeline: initial access, execution, persistence, privilege
   escalation, credential access, lateral movement, collection, exfiltration, impact.
2. **Map** each to ATT&CK technique and sub-technique (e.g. T1003.001 LSASS Memory, T1021.002 SMB/Admin Shares).
3. **Detection status per step:** detected (alerted, triaged in time), detected but missed in
   triage, logged but no rule, not logged.
4. **Telemetry gaps first:** "not logged" items become logging changes (Sysmon config, audit
   policy, cloud diagnostic settings) before rules can exist.
5. **Write rules** in Sigma using the real attacker command lines/artefacts as positive examples;
   generalise to the technique, not the exact string (e.g. `rundll32` calling `comsvcs.dll MiniDump`
   regardless of PID).
6. **Test** with recorded incident logs (replay into a dev SIEM) and an Atomic Red Team test for
   the technique; measure false positives on 30 days of production data.
7. **Deploy and track** in the detection backlog with an owner, linked to the incident ID.

## Output table
| Step | Technique | Status | Gap | New detection | Tested | Deployed |
|---|---|---|---|---|---|---|

## Gotchas
- Rules matching attacker-specific file names catch nothing next time.
- Detections deployed without triage runbooks get ignored.

## Verify
Each attacker step has either a deployed tested detection or a recorded accepted-risk reason.

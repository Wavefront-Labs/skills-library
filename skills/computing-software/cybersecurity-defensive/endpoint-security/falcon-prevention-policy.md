---
id: computing-software.cybersecurity-defensive.endpoint-security.falcon-prevention-policy
name: falcon-prevention-policy
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [falcon-prevention-policy, crowdstrike-falcon, edr-policy, sensor-update-policy, machine-learning-prevention, edr-operations]
level: practitioner
status: draft
description: "Configure CrowdStrike Falcon prevention policies: ML and behavioural prevention levels, host groups, sensor update and tamper protection, exclusions and staged rollout."
sources: ["https://www.crowdstrike.com/products/endpoint-security/falcon-prevent-next-gen-antivirus/", "https://falcon.crowdstrike.com/documentation", "https://github.com/CrowdStrike/falconpy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CrowdStrike Falcon prevention policies

(Falcon console docs require a customer login; settings names below are from the console.)

## Structure
- **Host groups** (dynamic by OS, hostname pattern, tags, OU) map to policies: workstations, servers, critical/fragile servers, VDI, pilot.
- **Prevention policy** per platform (Windows/macOS/Linux) and group, with precedence order.
- **Sensor update policy**: pin "N-1"/"N-2" builds for servers, "N" or auto for pilot; enable **uninstall and maintenance protection** (requires a maintenance token to uninstall).
- **Response policy** (Real Time Response permissions), **device control**, **firewall** policies separately.

## Prevention settings (Windows typical progression)
1. Start: Cloud ML and Sensor ML "Detection" at Moderate/Aggressive, "Prevention" at Moderate.
2. Enable behavioural prevention toggles: suspicious processes, suspicious registry operations, suspicious scripts and commands, intelligence-sourced threats, ransomware protections (volume shadow copy protection, backup deletion), credential dumping (LSASS), exploit mitigations, quarantine on write, script-based execution monitoring, interpreter-only (PowerShell/ .NET AMSI visibility).
3. Move Prevention to Aggressive after a quiet period on workstations; servers stay at Moderate unless validated.
4. "Extra aggressive" generally only for high-risk/kiosk groups.

## Exclusions
- ML exclusions (path-based, scoped to host groups) for false positives; IOA exclusions for specific behaviour patterns (process + command line regex); sensor visibility exclusions only when truly necessary (they blind the EDR).
- Document owner and ticket for each; review quarterly.

## Rollout
Pilot group (IT, security) -> 10% -> broad; watch detections dashboard for blocks of legitimate tools.

## Automation
FalconPy (`PreventionPolicies`, `HostGroup`) to export policies to Git and diff for drift.

## Gotchas
- Sensor visibility exclusions on broad paths (e.g. `<drive>\Tools\**`) are attacker gifts.
- A group with no policy assigned falls back to the default policy - check its settings too.

## Verify
- [ ] Every host in an intended group; no hosts on the default policy unexpectedly.
- [ ] Uninstall protection on; test that uninstall without token fails.
- [ ] Benign test (e.g. CrowdStrike test detection command from docs) triggers a prevention event.

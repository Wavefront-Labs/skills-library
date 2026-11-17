---
id: computing-software.cybersecurity-defensive.threat-intelligence.attack-for-ics
name: attack-for-ics
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [attack-for-ics, attack-mapping, ics-security, ot-security, mitre-attack, ot-detection]
level: advanced
status: docs-checked
description: "Apply MITRE ATT&CK for ICS: tactics unique to industrial environments (Impair Process Control, Inhibit Response Function), assets, and mapping OT incidents and detections."
sources: ["https://attack.mitre.org/matrices/ics/", "https://attack.mitre.org/assets/", "https://attack.mitre.org/techniques/ics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ATT&CK for ICS

A separate ATT&CK matrix for industrial control systems, covering adversary behaviour against OT.

## Tactics
The ICS matrix lists 12 tactics: Initial Access, Execution, Persistence, Privilege Escalation, Evasion,
Discovery, Lateral Movement, Collection, Command and Control, **Inhibit Response Function**,
**Impair Process Control**, **Impact**.

Example technique ids (ICS technique list): T0816 Device Restart/Shutdown, T0838 Modify Alarm Settings,
T0836 Modify Parameter, T0879 Damage to Property, T0880 Loss of Safety, T0827 Loss of Control,
T0843 Program Download, T0858 Change Operating Mode. Ids are renumbered and renamed over time:
always look the current id up on the site rather than copying from an old report.

## Assets
ATT&CK defines asset objects (e.g. Control Server, Data Gateway, Data Historian, Field I/O, Human-Machine
Interface, PLC, RTU, Safety Controller, Workstation, Jump Host, Firewall, VPN Server). Each carries a
mapping of techniques that may target that device, reflecting its capability and function.

## Uses
- **Incident analysis**: map known OT incidents to techniques to see the chain end-to-end.
- **Detection coverage**: map OT network detections and IT-OT boundary detections to techniques; find gaps with Navigator.
- **Tabletop design**: build scenarios from ICS technique chains relevant to your process.
- **Asset prioritisation**: use the asset-to-technique mappings to rank what to protect and monitor first.

## Gotchas
- Don't map OT-only; the Enterprise matrix covers the IT stages that usually precede OT impact.
- Detections need monitoring that understands your OT protocols; generic IT tooling sees little at the field level.

## Verify
OT detection coverage layer with data sources per technique, reviewed with operations engineers.

## Checked
2026-11-01. Confirmed on attack.mitre.org: the 12 ICS tactic names; technique names for T0816, T0838, T0836, T0879, T0880, T0827, T0843, T0858 (ICS technique list); the asset names and the asset-to-technique mapping statement (assets page). Removed: T0855 (not on the current ICS matrix), the Engineering Workstation and Safety Instrumented System asset names (the site lists Workstation and Safety Controller), named incidents, protocol names, tactic assignments of individual techniques, CISA ICS page claims.
Method: documentation only; no commands were run.

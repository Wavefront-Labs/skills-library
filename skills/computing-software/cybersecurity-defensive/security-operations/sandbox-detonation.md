---
id: computing-software.cybersecurity-defensive.security-operations.sandbox-detonation
name: sandbox-detonation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [malware-analysis, sandbox-detonation, dynamic-analysis, any-run, cape-sandbox, joe-sandbox, hybrid-analysis, behavioural-indicators, evasion]
level: practitioner
status: draft
description: "Detonate samples in a sandbox (CAPE, ANY.RUN, Joe Sandbox, Defender), read behavioural reports, defeat common evasion and extract IOCs safely."
sources: ["CySA+ CS0-003 objective 1.3 (sandboxing)", "CAPE Sandbox documentation", "D3FEND Dynamic Analysis (D3-DA)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sandbox detonation

**Goal:** observe what a sample does (processes, files, registry, network) quickly and safely,
and get behavioural indicators for detection and hunting.

## Choose the sandbox
| Option | When |
|---|---|
| Public interactive (ANY.RUN, Hybrid Analysis, Joe Sandbox Cloud free) | Commodity malware; sample contains no company data. Public tiers publish results. |
| Commercial private tenant | Sensitive samples, targeted attacks |
| Self-hosted CAPE (Cuckoo successor) | Full control, unlimited volume, custom VM images |
| EDR/AV built-in sandbox (e.g. Defender deep analysis) | Quick verdicts for files already in the EDR |

## Run well
1. Pick an OS image matching the target (Windows 10/11 with Office if it is a document).
2. Give it time: 3-5 minutes minimum; some samples sleep longer.
3. Interact if needed: enable macros, click through installers (interactive sandboxes).
4. Network: simulated internet (INetSim) is safe; a real egress through a VPN shows live C2
   but alerts the attacker and may contribute to harm: decide per case.
5. Provide arguments/parent files if the sample is a DLL (`rundll32 sample.dll,<export>`) or a stage-2 needing a loader.

## Read the report
- Process tree and command lines (LOLBins, PowerShell with encoded commands).
- Files dropped (hash each, they are new IOCs), registry Run keys, scheduled tasks, services.
- Network: DNS queries, HTTP requests, user agent, JA3/JA4, IPs; extracted malware configs (CAPE extracts many families' C2 lists).
- Signatures fired and ATT&CK mapping are hints, not proof.

## Evasion and empty reports
Samples check for VMs (MAC prefixes, low RAM/CPU, sandbox usernames, no user activity),
sleep, or require a specific locale or domain membership. Mitigate with realistic VM
specs (4 GB+ RAM, 2+ cores, documents and browser history), longer runtime, and different
locales. An empty report means "no verdict", not "benign".

## Gotchas
- Uploading to a public sandbox can tip off a targeted attacker who monitors it.
- Documents from your own company may contain sensitive data; use private analysis.
- Do not paste live C2 URLs into a browser outside the lab; defang them in notes.

## Verify
- [ ] Behavioural IOCs (hashes, domains, registry keys) added to the case and hunted across the estate.
- [ ] Detections exist for at least one behaviour observed, not just the file hash.

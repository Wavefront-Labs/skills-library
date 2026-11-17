---
id: computing-software.digital-forensics-incident-response.incident-response-process.prioritising-detections-with-the-pyramid-of-pain
name: prioritising-detections-with-the-pyramid-of-pain
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [pyramid-of-pain, threat-intelligence, iocs, ttps, detection-engineering, dfir]
level: practitioner
status: draft
description: "Use the Pyramid of Pain to prioritise incident indicators and detections: hashes and IPs versus artefacts, tools and TTPs, and how to climb the pyramid."
sources: ["https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prioritising detections with the Pyramid of Pain

**Goal:** spend detection effort where it costs the attacker most to adapt (David Bianco, 2013).

## Levels (bottom = trivial for attacker to change)
| Level | Example from an incident | Attacker cost to change |
|---|---|---|
| Hash values | sha256 of loader | Trivial (recompile, pad) |
| IP addresses | C2 VPS IP | Easy |
| Domain names | C2 domain | Simple (cheap registration) |
| Network/host artefacts | URI pattern `/api/v2/s?id=`, user agent, named pipe `\\.\pipe\msagent_*`, service name, registry path | Annoying |
| Tools | Cobalt Strike, Rclone, AdFind, Mimikatz | Challenging (retool) |
| TTPs | LSASS access by non-system process, DCSync from a non-DC, service creation over SMB then PsExec-like execution | Tough (change behaviour) |

## Applying it after an incident
1. Sort the IOC register by level. Hashes/IPs/domains still go to blocklists and sweeps
   (cheap, useful short-term), but expect them to age out in days.
2. For each attack stage, write at least one detection at **artefact, tool or TTP** level.
   Example: instead of the rclone hash, detect `rclone` command-line patterns (`copy`,
   `--config`, cloud remotes) regardless of binary name, plus large egress to storage APIs.
3. Prefer detections that survive tool swaps: behaviour of the technique (ATT&CK) rather
   than tool signature.
4. Track coverage per level in the detection inventory.

## Gotchas
- TTP detections are noisier; tune with environment baselines (admin tools used legitimately).
- Do not discard low-level IOCs; they are fast for retro-hunting and scoping.

## Verify
For each new detection, ask "if the attacker swapped binary and infrastructure tomorrow,
would this still fire?" If no, it sits low on the pyramid.

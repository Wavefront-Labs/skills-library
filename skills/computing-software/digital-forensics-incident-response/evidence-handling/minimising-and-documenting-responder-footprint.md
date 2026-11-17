---
id: computing-software.digital-forensics-incident-response.evidence-handling.minimising-and-documenting-responder-footprint
name: minimising-and-documenting-responder-footprint
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [responder-footprint, live-response, evidence-integrity, documentation, forensic-soundness, dfir]
level: practitioner
status: draft
description: "Minimise and document the changes a responder makes to a live system: tool choice, output locations, credential hygiene, and a footprint log for the report."
sources: ["https://csrc.nist.gov/pubs/sp/800/86/final", "https://www.rfc-editor.org/rfc/rfc3227"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Minimising and documenting responder footprint

**Goal:** every live action changes the system. Keep changes small, predictable and written
down, so analysts can tell your artefacts from the attacker's.

## Minimise
- Prefer remote collection (EDR live response, Velociraptor) over interactive logon; RDP
  creates profiles, logon events, and caches credentials on a possibly compromised host.
- Run tools from external media or memory; write outputs to an external drive or network
  share, never the evidence volume.
- Use known tools with documented artefacts (KAPE, WinPmem) instead of ad-hoc scripts.
- One collection pass with a planned tool set, not repeated exploratory logins.
- Do not install software on the host; portable versions only.

## Artefacts responders typically create
Prefetch files for tools (`WINPMEM*.pf`), Amcache/ShimCache entries, services for memory
drivers (`pmem`), new USB device entries, 4624/4672 logon events, 7045 service install,
PowerShell 4104 logs, shellbags of folders browsed, new user profile if first logon.

## Footprint log (keep alongside notes)
| UTC time | Host | Responder | Account | Method | Action / tool + hash | Expected artefacts |
|---|---|---|---|---|---|---|
| 2026-10-16T09:02Z | WKS-0142 | CJ | ir-collector | Velociraptor | Windows.KapeFiles.Targets | Velociraptor service activity, file reads |

## Credential hygiene
Use dedicated IR accounts with no domain-wide admin, restricted admin RDP or network logon
type 3, and rotate them after the incident.

## Verify
When building the timeline, filter out every footprint log entry; anything that remains in
the response window must be attacker or user activity.

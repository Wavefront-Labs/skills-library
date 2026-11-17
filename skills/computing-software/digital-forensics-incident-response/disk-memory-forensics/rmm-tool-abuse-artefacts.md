---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.rmm-tool-abuse-artefacts
name: rmm-tool-abuse-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [rmm-tools, lateral-movement, remote-access, persistence, dfir]
level: advanced
status: draft
description: "Investigate abuse of remote monitoring and management tools (AnyDesk, ScreenConnect, TeamViewer, Atera): install traces, logs, session records and IDs."
sources: ["https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-025a", "https://attack.mitre.org/techniques/T1219/", "https://support.anydesk.com/knowledge/trace-files"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RMM tool abuse artefacts

**Goal:** attackers install legitimate remote access software (ATT&CK T1219) for persistent,
interactive, often trusted access (CISA AA23-025A). Their logs are excellent evidence.

## AnyDesk
- Logs: `%ProgramData%\AnyDesk\ad_svc.trace` (service install), `%APPDATA%\AnyDesk\ad.trace`
  (user), `connection_trace.txt` (incoming sessions: time, remote AnyDesk ID, user/password or accepted).
- Config: `system.conf`, `service.conf` (`ad.anynet.id` = this machine's ID; unattended password hash).
- `file_transfer_trace.txt` lists files transferred during sessions.

## ConnectWise ScreenConnect
- Installed service `ScreenConnect Client (<instance-hash>)`; `%ProgramFiles(x86)%\ScreenConnect Client (<id>)\`
  `system.config` contains the relay host (attacker's instance domain if self-hosted or trial).
- Application event log: "ScreenConnect" events for session connect/disconnect, file transfers, commands.
- Files transferred land in the user's Documents\ConnectWiseControl\Files by default.

## TeamViewer
- `%ProgramFiles%\TeamViewer\Connections_incoming.txt` (remote TV ID, display name, start/end, user, session type),
  `TeamViewer<ver>_Logfile.log`; `%APPDATA%\TeamViewer\Connections.txt` for outgoing.

## Others
- Atera, Splashtop, NetSupport, Action1, MeshCentral, SimpleHelp: each installs a service and logs to
  ProgramData; check the vendor's documented log locations.

## Detection and scoping
- Hunt services/installed software across the fleet for RMM tools not on the approved list.
- Proxy/DNS for relay domains (`*.anydesk.com`, `relay.screenconnect.com`, `*.teamviewer.com`) from unexpected hosts.
- 7045 service installs and MSI installer events (1033/11707) for install times.

## Gotchas
- The organisation's own IT may use the same tool; attacker instances differ by account/instance ID or relay host.
- Portable versions run without install; look in prefetch/Amcache and user Downloads.

## Verify
Each RMM session is tied to a remote ID, time window and, where possible, actions (file transfers, commands).

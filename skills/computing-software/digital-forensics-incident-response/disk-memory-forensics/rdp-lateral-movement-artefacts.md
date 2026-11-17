---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.rdp-lateral-movement-artefacts
name: rdp-lateral-movement-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [rdp-forensics, lateral-movement, 4624, terminal-services, logon-types, dfir]
level: practitioner
status: draft
description: "Trace RDP lateral movement across source and destination: Security 4624 type 10, TerminalServices and RemoteConnectionManager logs, 4778/4779, and client artefacts."
sources: ["https://jpcertcc.github.io/ToolAnalysisResultSheet/", "https://www.sans.org/posters/hunt-evil/", "https://attack.mitre.org/techniques/T1021/001/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP lateral movement artefacts

**Goal:** reconstruct RDP hops: who connected from where to where, when, and how long the
session lasted.

## Destination host event logs
| Log | Event | Meaning |
|---|---|---|
| Security | 4624 **type 10** (RemoteInteractive) or type 7 (unlock/reconnect); with NLA a type 3 precedes | Successful logon; source IP in `IpAddress` |
| Security | 4625 | Failed logon (type 3 with NLA) |
| Security | 4778 / 4779 | Session reconnected / disconnected, with client name and IP |
| Security | 4634/4647 | Logoff |
| TerminalServices-RemoteConnectionManager/Operational | 1149 | "User authentication succeeded" with user, domain, source IP (despite the name, means network connection established) |
| TerminalServices-LocalSessionManager/Operational | 21 (logon), 22 (shell start), 24 (disconnect), 25 (reconnect), 39/40 | Session lifecycle with source IP |
| RdpCoreTS/Operational | 131 | Connection accepted, client IP:port |

## Destination file artefacts
New user profile created on first logon, `UsrClass.dat` shellbags, UserAssist for tools run,
`rdpclip.exe` and `tstheme.exe` Prefetch, clipboard misuse.

## Source host
Client artefacts (Terminal Server Client MRU, Default.rdp, bitmap cache, mstsc jump lists),
`TerminalServices-RDPClient/Operational` 1024/1102.

## Building the chain
Join destination logon source IPs to hosts (DHCP logs, DNS), then examine those as sources;
repeat until you reach the entry point (VPN pool, jump host, attacker IP). Sessions over
tunnels (ngrok, SSH -L, Chisel) show `127.0.0.1`/`::1` as source.

## Gotchas
- 4624 type 10 is absent when NLA fails over to other types or with RestrictedAdmin (type 3
  with no credentials stored); rely on TerminalServices logs too.
- Log rotation of Security.evtx on busy servers; the TS logs are smaller and often older.

## Verify
For each hop, 1149/21 on the destination and client evidence on the source share user and
time; the chain is consistent with network flow logs on TCP 3389.

---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.rdp-and-remote-access-protocols-on-the-wire
name: rdp-and-remote-access-protocols-on-the-wire
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [rdp-traffic, rdp, vnc, ssh, remote-access-tools, anydesk, lateral-movement, wireshark, dfir]
level: practitioner
status: draft
description: "Identify and characterise RDP, VNC, SSH and commercial remote-access tool traffic in captures and flows: handshakes, cookies, JA3/HASSH and session metadata."
sources: ["https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rdpbcgr/5073f4ed-1e93-45e1-b039-6e30c385867c", "https://wiki.wireshark.org/RDP", "https://github.com/salesforce/hassh"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP and remote access protocols on the wire

**Goal:** recognise interactive remote access in network data, identify the user or client
where possible, and spot abuse (lateral RDP, exposed RDP brute force, tunnelled RDP, rogue
remote-access tools).

## RDP (TCP 3389, also UDP 3389 for transport)
- First packet: X.224 Connection Request with **routing cookie** `Cookie: mstshash=<username>`
  (often the username typed by the client, truncated to 9 chars by mstsc; brute-force tools use
  fixed values like `hello` or `Administr`). Filter: `rdp.rt_cookie` or `tcp.port == 3389 && tpkt`.
- `rdp.negReq.requestedProtocols`: 0 standard RDP security, 1 TLS, 2 CredSSP (NLA), 8 RDSTLS.
  Standard RDP security in 2026 is unusual and weak.
- After that, TLS: extract SNI/certificate (self-signed cert CN = hostname of target), JA3/JA4
  of the client. Content is encrypted; you characterise sessions by size/duration.
- Brute force: many short sessions from one source, each ending after the CredSSP exchange.
- RDP over non-standard ports or tunnelled (ngrok, plink `-R`, Chisel): RDP handshake bytes
  (`03 00 00 13 0e e0`) on unexpected ports, or long-lived SSH/TLS sessions to rented VPS.
- Zeek `rdp.log` records cookie, security protocol, client name/build, keyboard layout and
  result: invaluable at scale.

## SSH (TCP 22)
- Cleartext banner (`SSH-2.0-OpenSSH_9.6`, `SSH-2.0-paramiko_...`, `SSH-2.0-Go`) and key
  exchange algorithms: **HASSH** fingerprints the client (tool identification).
- Session size and timing distinguish interactive shells (small packets, human cadence) from
  file transfer (bulk).

## VNC and commercial tools
- VNC/RFB: `RFB 003.008` banner on 5900+.
- AnyDesk (TCP 7070/443, `*.net.anydesk.com`), TeamViewer (5938, `*.teamviewer.com`),
  ScreenConnect/ConnectWise Control (8041, relay domains), Atera, Splashtop, RustDesk:
  identify by DNS/SNI and destination ranges; abuse by ransomware crews is common.

## Workflow
1. Statistics > Conversations, filter on remote access ports and SNI/domains.
2. For each session: source, destination, start, duration, bytes, client fingerprint, cookie.
3. Correlate with host logs: 4624 type 10 and RDP operational logs (1149, 21/24/25) on the
   target; tool logs (AnyDesk `ad.trace`, TeamViewer `Connections_incoming.txt`).

## Self-check
Every remote session you report has endpoints, duration, protocol and the client
identification method (cookie, fingerprint, tool domain) used.

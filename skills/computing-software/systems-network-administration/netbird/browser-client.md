---
id: computing-software.systems-network-administration.netbird.browser-client
name: browser-client
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, browser-client, webassembly, browser-ssh, browser-rdp]
level: practitioner
status: docs-checked
description: "Reach SSH and RDP targets from a web browser with the NetBird Browser Client: prerequisites, connect steps, temporary ACLs, security notes and limits."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/browser-client.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Browser Client runs a NetBird peer as WebAssembly in the browser, so you can open SSH or RDP sessions without installing anything.

Prerequisites: an admin account in the dashboard (the client creates temporary ACL rules); for SSH, NetBird SSH enabled on the target and in the dashboard; for RDP, the remote desktop server enabled on the target; a current Chrome, Firefox, Edge or Safari.

Connect: Peers > Servers > find the peer > Remote Access > SSH or RDP. Enter credentials (a DOMAIN\username prefix is allowed for RDP) and click Connect. RDP shows a certificate warning every time because the browser cannot check the native store; accepted certificates are remembered in browser storage.

Security: traffic is WireGuard-encrypted; a short-lived peer with browser-generated keys is created, with temporary ACLs allowing TCP 22 and TCP 3389, and removed at session end. Keys and credentials stay in browser memory. On shared machines use a private window and close the tab.

Limits: relay-only connections (possibly higher latency); no SFTP, sound or file shares; resolution change needs reconnect. Text clipboard works both ways for RDP.

Troubleshooting: "Failed to initialize WASM" - clear cache or try another browser; timeout - confirm the service runs on the target; RDP auth failure - include the domain in the username.

## Checked

2026-11-04: read the Browser Client page in full. Confirmed prerequisites, the connect steps, the RDP certificate behaviour, temporary peer and ACL ports, in-memory keys, private window advice, known limitations and troubleshooting entries. Nothing removed.

Method: documentation only; no commands were run.

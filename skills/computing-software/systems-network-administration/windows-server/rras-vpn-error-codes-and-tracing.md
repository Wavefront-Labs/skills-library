---
id: computing-software.systems-network-administration.windows-server.rras-vpn-error-codes-and-tracing
name: rras-vpn-error-codes-and-tracing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [remote-access, rras, vpn-error-809, rras-tracing, always-on-vpn]
level: practitioner
status: docs-checked
description: "Diagnose RRAS VPN failures: client errors 809, 812, 13801, 13806, 691 and 789, RRAS tracing with netsh ras, NPS 6273 events and certificate checks."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-always-on-vpn
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-remote-access-vpn-and-aovpn-guidance
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# RRAS VPN error codes and tracing

## Client errors to cause
| Error | Meaning | Usual fix |
|---|---|---|
| 809 | remote server does not respond | UDP 500 and 4500 blocked on the VPN server, firewall, NAT or routers between client and server |
| 812 | authentication method mismatch (RRAS event 20276) | NPS requires something the client cannot meet, for example PEAP with a certificate while the client uses EAP-MSCHAPv2; align client profile and NPS policy |
| 13801 | IKE authentication credentials unacceptable | server machine certificate lacks Server Authentication EKU or is expired, client lacks the root CA, or the VPN server name does not match the certificate subject |
| 13806 | IKE could not find a valid machine certificate | the VPN server lacks the required machine or root certificate; install valid certificates on client and server |

## Server-side tracing
Check the Application log on the RRAS server (event 20276 accompanies error 812) and the NPS accounting logs, which default to
`%SYSTEMROOT%\System32\Logfiles\` in files named `IN<date>.txt`. Verbose RAS tracing exists (`netsh ras set tracing`), but this skill does not
document its switches or log file names; follow the current Microsoft troubleshooting article before using it.

## Client side
- `Get-VpnConnection` shows the client profile.
- Event Viewer > Application: look for events labelled *RasClient*; every message ends with the error code. Event 20227 with error 720 is a separate case (WAN Miniport (IP) adapter not bound).
- UDP 500 and 4500 must not be blocked; if the tunnel type is known, set it explicitly on the client.

## Verify
- [ ] Error reproduced and resolved; tracing disabled again.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, windows-powershell-docs (winserver2025-ps RemoteAccess, NetNat, NetTCPIP), azure-docs vpn-gateway articles, SupportArticles-docs (troubleshoot-always-on-vpn, ms.date 2026-02-12).
Confirmed from SupportArticles-docs troubleshoot-always-on-vpn (ms.date 2026-02-12) and troubleshoot-remote-access-vpn-and-aovpn-guidance: causes and fixes for errors 809, 812 (event 20276), 13801 and 13806,
RasClient events, NPS accounting log location, UDP 500/4500 guidance, event 20227 with 720.
Removed error codes 13868, 691, 789 and 0x80092013 and their causes, the netsh tracing details, NPS events 6272/6273, RemoteAccess events 20255/20271, rasphone.pbk and the certutil command, which the pages do not confirm.
Method: documentation only; no commands were run.

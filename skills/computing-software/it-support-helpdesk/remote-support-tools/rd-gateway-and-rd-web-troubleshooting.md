---
id: computing-software.it-support-helpdesk.remote-support-tools.rd-gateway-and-rd-web-troubleshooting
name: rd-gateway-and-rd-web-troubleshooting
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rd-gateway-troubleshooting, rd-gateway, rd-web, rds, cap-rap, certificates]
level: practitioner
status: draft
description: "Fix RD Gateway and RD Web Access failures: certificate name and trust, CAP and RAP policy matches, FQDN vs NetBIOS targets, UDP 3391 fallback, and the gateway event log."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remote-desktop-gateway-role"
  - "https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-web-client-admin"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# rd-gateway-and-rd-web-troubleshooting

## How it fits
Client -> TLS 443 (and optionally UDP 3391) -> RD Gateway -> RDP 3389 -> target. The
gateway checks a **CAP** (who can connect: user/computer groups, auth method) and a **RAP**
(which targets they can reach: AD group or gateway-managed group of computers).

## Common failures
| Symptom | Likely cause |
|---|---|
| Certificate warning or "can't verify identity" | Gateway cert name does not match the public name, or chain/CRL not reachable from outside |
| "Your user account is not authorized to access the RD Gateway" | User not in a CAP group, or the CAP requires smart card/device redirection settings the client violates |
| "...not authorized to access the remote computer" | RAP group does not contain the target in the form the client used (FQDN vs short name vs IP) |
| Connects then drops in seconds, slow | UDP blocked; client falls back but some firewalls drop half the flow. Test with UDP off |
| RD Web shows no icons | User not assigned to the collection/RemoteApp, or the web feed URL is stale |

## Logs
Gateway server: Event Viewer > Applications and Services > Microsoft > Windows >
TerminalServices-Gateway > Operational. Event 200 = CAP passed, 302 = connected to resource,
303 = disconnected with bytes transferred; failure events next to them name the policy or
target that rejected the user.

## RD Web
- Classic: `https://<gateway>/RDWeb`; HTML5 client: `https://<gateway>/RDWeb/webclient`.
- The web client needs the gateway cert published to it (`Import-RDWebClientBrokerCert`)
  and a publicly trusted cert on the gateway.

## Gotchas
- Gateway managed computer groups list exact names; add both FQDN and short name, or use
  an AD group.
- NPS central policy store mode moves CAPs into NPS; look there if Gateway Manager shows
  none.
- Old `.rdp` files pin gateway settings; republish the feed after changes.

## Verify
The user connects from outside, gateway log shows 200 then 302 for that user and target,
and no certificate warning appears.

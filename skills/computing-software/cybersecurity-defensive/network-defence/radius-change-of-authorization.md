---
id: computing-software.cybersecurity-defensive.network-defence.radius-change-of-authorization
name: radius-change-of-authorization
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [change-of-authorization, radius-coa, rfc-5176, dynamic-authorization, session-reauthentication, port-bounce, network-access-control]
level: practitioner
status: docs-checked
description: "Use RADIUS Change of Authorization: enable dynamic authorization on NADs, CoA reauth vs port bounce vs disconnect, SOC-triggered quarantine and securing the CoA channel."
sources: ["https://datatracker.ietf.org/doc/html/rfc5176", "https://www.cisco.com/c/en/us/td/docs/security/ise/3-3/admin_guide/b_ise_admin_3_3/b_ISE_admin_33_asset_visibility.html", "https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_aaa/configuration/xe-16/sec-usr-aaa-xe-16-book/sec-rad-coa.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RADIUS Change of Authorization (CoA)

CoA (RFC 5176) lets the RADIUS server change an **existing** session - after posture changes, profiling
updates, or a SOC decision to quarantine a host - without waiting for re-authentication.

## NAD configuration (Cisco IOS-XE)
```
aaa server radius dynamic-author
 client <RADIUS_SERVER_1> server-key <secret>
 client <RADIUS_SERVER_2> server-key <secret>
 auth-type any
 port 1700        ! Cisco default; RFC default is UDP 3799
```

## Message types
| Type | Effect |
|---|---|
| CoA Reauth | Session re-authenticates; new authorisation (VLAN/dACL/SGT) applied |
| CoA Port Bounce | Link down/up - forces DHCP renewal (needed after VLAN change) |
| CoA Port Shutdown | Admin-disables the port |
| Disconnect-Request (Session terminate) | Ends the session (also for VPN/Wi-Fi) |

## SOC quarantine use case
EDR/SIEM -> NAC server integration -> NAC issues CoA for the endpoint's session -> the session gets a
quarantine authorisation. Release by reversing the quarantine policy on the NAC server.

## Security
- CoA packets are authenticated with the shared secret; restrict `client` entries to the RADIUS servers and filter UDP 1700/3799 to the management network. Unauthorised CoA = remote disconnect/re-segmentation of users.
- Apply the same Message-Authenticator and secret quality rules as for RADIUS (see radius-server-hardening).

## Gotchas
- Check which CoA types each NAD model supports before relying on them.

## Verify
- [ ] ISE live sessions -> "CoA" on a test endpoint changes its authorisation within seconds.
- [ ] The NAD log or debug shows the CoA was acknowledged.

## Checked

Date: 2026-10-28

- Confirmed (RFC 5176, Cisco IOS XE CoA page): UDP port 3799 is the RFC port, Cisco default is 1700 (3799 for ACS 5.1 interop); aaa server radius dynamic-author with client ... server-key; Disconnect Request ends a session; session reauthentication and bounce port requests exist.
- Removed (not found): placeholder server IPs, ANC command string and pxGrid detail, NAT, wireless limits and IP phone gotchas, show aaa servers verify.
Method: documentation only; no commands were run.

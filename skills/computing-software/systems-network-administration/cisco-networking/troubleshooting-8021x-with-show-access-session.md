---
id: computing-software.systems-network-administration.cisco-networking.troubleshooting-8021x-with-show-access-session
name: troubleshooting-8021x-with-show-access-session
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, 802-1x, dot1x-troubleshooting, access-session, mab, ise-live-logs, radius-debug, session-states]
level: practitioner
status: draft
description: "Troubleshoot 802.1X/MAB on Catalyst with show access-session details: method states, authorization results, dACL/VLAN applied, and the debugs that matter."
sources:
  - https://www.cisco.com/c/en/us/support/docs/security/identity-services-engine/215461-troubleshoot-dot1x-on-catalyst-9000-series.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ieee_802_1x_port_based_authentication.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Troubleshooting with show access-session

## First look
```
show access-session                          ! one line per session: Interface, MAC, Method, Domain, Status
show access-session interface Gi1/0/5 details
```
Key fields in details:
| Field | Meaning |
|---|---|
| Status | Authorized / Unauthorized / Running |
| Domain | DATA or VOICE |
| Oper host mode / control dir | multi-auth etc., Both/In |
| Server Policies | VLAN, dACL name, SGT, URL redirect returned by ISE |
| Method status list | `dot1x Authc Success`, `dot1x Stopped`, `mab Authc Failed`, `Running` |

## Reading method states
- `dot1x Running` forever, then MAB: no supplicant (printer/IoT) -> expected MAB fallback.
- `dot1x Authc Failed`: ISE rejected; check ISE Live Logs for the failure reason (bad cert, wrong identity store).
- `mab Authc Failed` + ISE shows nothing: switch not reaching ISE (source interface, key, NAD not defined).
- Authorized but no access: wrong VLAN, dACL download failed (`%EPM-4-POLICY_APP_FAILURE`), or
  URL redirect still applied.

## Supporting commands
```
show authentication sessions interface Gi1/0/5 details    ! older alias
show aaa servers
test aaa group ISE <user> <pw> new-code
show ip access-lists interface Gi1/0/5 in                  ! downloaded dACL entries (xACSACLx-IP-...)
show device-tracking database interface Gi1/0/5            ! IP learned for the session
show radius statistics
```

## Debugs (conditional, scoped)
```
debug condition mac-address 0050.5612.3456
debug access-session all
debug radius authentication
debug dot1x all
```
IOS XE 16.x+: also `monitor capture` on the uplink for RADIUS (UDP 1812/1813) or radioactive
trace (`show logging process smd internal`).

## Common root causes
- Port in `access-session closed` mode with no MAB: IoT never gets access.
- ISE CoA failing (UDP 1700 blocked or `aaa server radius dynamic-author` missing).
- IP device tracking not running: ISE sees no IP, posture/policies fail.
- Supplicant using wrong EAP method or untrusted server certificate.

## Verify
- [ ] Session Authorized with the expected Server Policies; ISE Live Log shows the same session ID.

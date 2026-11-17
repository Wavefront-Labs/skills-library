---
id: computing-software.systems-network-administration.cisco-networking.dot1x-monitor-low-impact-closed-modes
name: dot1x-monitor-low-impact-closed-modes
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, dot1x, monitor-mode-8021x, low-impact-mode, closed-mode, open-authentication, ise, nac-rollout, catalyst-9300]
level: practitioner
status: docs-checked
description: "Phase an 802.1X rollout on IOS-XE: open authentication with an ACL (monitor, low-impact style) versus closed mode, with Catalyst 9300 commands and what dACLs do."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ieee_802_1x_port_based_authentication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 802.1X deployment modes: open versus closed

Turning on closed-mode 802.1X on day one blocks any device without a supplicant (printers, cameras, PXE clients), so
roll out in phases. The Cisco guide defines the two authentication modes this relies on: 802.1X and MAB support
**open** and **closed**. The phase names "monitor" and "low-impact" are an industry convention for open mode with no
ACL and open mode with a restrictive port ACL; the Cisco page cited here does not use them.

## Building blocks (Catalyst 9300 17.9 guide)
- `authentication open`: a new host can pass traffic according to the ACL on the port before it authenticates; after
  authentication the RADIUS policies apply. Open authentication takes precedence over `authentication port-control`.
- `authentication host-mode {multi-auth | multi-domain | multi-host | single-host}`. Multi-auth allows one
  authentication on the voice VLAN and many on the data VLAN; multi-domain allows one per domain (voice, data).
- `authentication order {dot1x | mab} | webauth` and `authentication priority ...` set the method sequence;
  `mab [eap]` enables MAC authentication bypass, intended for devices such as printers.
- `authentication periodic` enables reauthentication (off by default; the default timer is 3600 s) and
  `authentication timer reauthenticate <seconds>` changes it, or use the server-supplied value.
- `authentication port-control {auto | force-authorized | force-unauthorized}`; `dot1x pae authenticator`.
- Line protocol stays up before authorisation in all host modes.

## Phase 1: open, no restrictions (monitor style)
```
interface GigabitEthernet1/0/10
 switchport mode access
 authentication host-mode multi-auth
 authentication open
 authentication order dot1x mab
 authentication priority dot1x mab
 authentication port-control auto
 authentication periodic
 mab
 dot1x pae authenticator
```
Everything is attempted and logged, and traffic is not blocked. Use RADIUS logs to find failing endpoints; fix them
with supplicant profiles or MAB entries.

## Phase 2: open with a restrictive port ACL (low-impact style)
Keep `authentication open` and apply a static ACL on the port permitting only what unauthenticated devices need.
After authentication the policy from the RADIUS server applies, including a downloadable ACL (dACL) and redirect
URLs. If no ACL is downloaded, the static default ACL on the port is applied to the host. Illustration only:
```
ip access-list extended PRE-AUTH
 permit udp any eq bootpc any eq bootps
 permit udp any any eq domain
 deny ip any any
interface GigabitEthernet1/0/10
 ip access-group PRE-AUTH in
```
Facts to design around: per-user ACLs are supported only in single-host mode; dACL limit with stacking is 64 ACEs
per dACL per port, without stacking it is the free TCAM entries; multiple dACLs of the same type (IPv4 or IPv6) are
not supported through ISE, so send unique dACLs. For hosts with no authorisation policy, a directive controls
behaviour: `open` allows all traffic, `default` (the default) applies the port's access; set it on AAA with
`authz-directive` or on the switch with `epm access-control open`.

## Phase 3: closed mode
Remove `authentication open`. Without a static ACL in closed mode, the first host's policy is applied without IP
address insertion; when a second host is detected, policies are refreshed and enforced with IP address insertion.
Remediation VLANs, guest and critical VLANs are separate features (see dot1x-critical-authentication).

## Readiness gates (judgement)
- Failed authentications near zero across a full business cycle; RADIUS-down behaviour tested; a helpdesk path for
  MAB exceptions.

## Verify
```
show authentication sessions
show authentication sessions interface GigabitEthernet1/0/10
```
Confirm status Authz Success for pilot endpoints before moving a switch to closed.

## Checked
Checked 2026-11-08 against the Cisco Catalyst 9300 17.9 802.1X chapter: open/closed modes, command syntax, host
modes, default reauthentication timer, dACL limits and directive behaviour, show commands. Removed: the IBNS 2.0
`access-session` line, `dot1x timeout tx-period`, the claim that closed mode passes only EAPoL/CDP/LLDP, and the two
rollout guides (404 and 403), which are the sources of the phase names.
Method: documentation only; no commands were run.

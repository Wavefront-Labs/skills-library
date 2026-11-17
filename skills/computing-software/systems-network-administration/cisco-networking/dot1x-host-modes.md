---
id: computing-software.systems-network-administration.cisco-networking.dot1x-host-modes
name: dot1x-host-modes
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9300, 802-1x, dot1x, host-mode, multi-auth, multi-domain, security-violation]
level: practitioner
status: docs-checked
description: "Choose the 802.1X host mode on a Catalyst 9300 (single-host, multi-host, multi-domain, multi-auth), set the violation action, and know which features need which mode."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ieee_802_1x_port_based_authentication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 802.1X host modes

Scope: Catalyst 9300 IOS XE 17.9 (Configuring IEEE 802.1x Port-Based Authentication).

## Modes
| Mode | Behaviour (from the guide) |
|---|---|
| `single-host` | only one client on the port; if it leaves or is replaced the link goes down and the port returns to unauthorized. With a voice VLAN, an unlimited number of Cisco IP phones can use it |
| `multi-host` | multiple hosts allowed after a single host has been authenticated; only the first host needs authentication |
| `multi-domain` | two authentications: one on the voice VLAN and one on the data VLAN; the voice VLAN must be configured for the phone |
| `multi-auth` | one authentication on the voice VLAN and multiple on the data VLAN |

```
interface gigabitethernet1/0/5
 authentication port-control auto
 authentication host-mode multi-domain
 authentication violation restrict
```
`authentication host-mode [multi-auth | multi-domain | multi-host | single-host]`; `authentication port-control`
must be `auto`. To authorize a voice device the AAA server must send the Cisco AV pair `device-traffic-class=voice`;
without it the switch treats the phone as a data device.

## Violations
`authentication violation {shutdown | restrict | protect | replace}`:
- `shutdown`: error-disable the port.
- `restrict`: generate a syslog error.
- `protect`: drop packets from any new device that sends traffic to the port.
- `replace`: remove the current session and authenticate the new host. In multi-domain mode the data host's MAC is
  replaced by the new MAC and authentication starts for it; if the new host is a voice host, the original voice
  host is removed. It does not apply to multi-auth (no violations are triggered) or multi-host (only the first host
  is authenticated).

Voice aware 802.1x security (`errdisable detect cause security-violation shutdown vlan`, global) disables only the
VLAN on which a violation occurs rather than the whole port, so a violation on the data VLAN leaves the phone's
voice VLAN running. Recovery uses `errdisable recovery cause security-violation` or shut/no shut.

## Feature support by mode (guide)
- Per-user ACLs: single-host only. In multi-domain and multi-auth the ACL policy of one host does not affect
  another host.
- Guest VLAN: single-host, multi-host, multi-auth and multi-domain. Restricted VLAN: single-host only.
- Multi-auth: RADIUS-supplied VLAN assignment is allowed under conditions listed in the guide; the guide says the
  number of hosts per multi-auth port is 8, though there can be more.
- Critical (inaccessible) bypass on multi-auth ports needs `authentication event server dead action reinitialize
  vlan vlan-id`.

## Check
`show authentication sessions interface interface-id` shows the sessions on the port.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Searched the Catalyst 9300 17.9 802.1x chapter for host-mode and
violation terms and read: Flexible Authentication host-mode list, the authentication host-mode step (keywords and
notes), authentication violation step and keyword meanings, MAC Replace, the voice VLAN `device-traffic-class=voice`
paragraph, voice aware 802.1x security, and the per-user ACL, guest/restricted VLAN, multi-auth and critical-VLAN lines
(read as individual paragraphs; the chapter was not read end to end). Corrected: the old text said `replace` is
"IOS XE" only and described `restrict` as "drops and logs" (the guide says generates a syslog error);
`multi-auth` described as "one voice + many data" now follows the guide; the single-host "one MAC" wording replaced.
Removed as unconfirmed: `access-session host-mode` (IBNS 2.0), the `%AUTHMGR-5-SECURITY_VIOLATION` message, a default
violation action, hot-desking/dock/VM and phone-tagging gotchas, the dACL placeholder note, `show logging | include
VIOLATION`. The MAB deployment guide cited earlier was not read and was dropped from sources.

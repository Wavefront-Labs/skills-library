---
id: computing-software.systems-network-administration.cisco-networking.mac-authentication-bypass-mab
name: mac-authentication-bypass-mab
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, aaa, mab, mac-authentication-bypass, 802-1x, radius, flexible-authentication]
level: practitioner
status: docs-checked
description: "Authenticate printers, cameras and other non-802.1X devices with MAB on Catalyst switches, ordering it with dot1x, and the guide's interaction rules."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ieee_802_1x_port_based_authentication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAC Authentication Bypass (MAB)

Catalyst 9300, IOS XE 17.9. MAB is disabled by default. When enabled on an 802.1x port, the
switch uses the client MAC address as its identity: it waits for an Ethernet packet from the
client, then sends the authentication server a RADIUS Access-Request with a username and password
based on that MAC. If authorization succeeds the client gets access; if it fails the port goes to
the guest VLAN, if one is configured. It does not work for clients that use an alternate MAC
address format unless you configure how MAB handles them.

## Enable (from the guide)
```
interface GigabitEthernet2/0/1
 authentication port-control auto     ! enables 802.1x on the port
 mab                                  ! mab eap makes the device use EAP for authorization
```
MAB can be enabled only if 802.1x authentication is enabled on the port. 802.1x also needs
`dot1x system-auth-control` globally and RADIUS configured.

## Ordering with dot1x
- By default 802.1x is tried first; if it times out waiting for an EAPOL response the switch
  falls back to MAB.
- If any EAPOL packet is seen during the link's life, the switch treats the device as an
  802.1x supplicant and uses 802.1x, not MAB. EAPOL history clears when the link goes down.
- To try MAB first (guide example):
```
interface GigabitEthernet1/0/1
 authentication order mab dot1x
 authentication priority mab dot1x
```
- A port already authorized by MAB is not unauthorized if a supplicant is later detected.

## Behaviour and limits
- Reauthentication works as for 802.1x; the port stays in its assigned VLAN, and on failure moves
  to the guest VLAN if configured. If reauthentication relies on Session-Timeout and a
  Termination-Action of Initialize (DEFAULT), the MAB session ends and connectivity is lost
  during reauthentication.
- Restricted VLAN is not supported for MAB-authenticated clients. MAB and NEAT are mutually
  exclusive.
- Disabling MAB on an already authorized port does not change the port state. An unauthorized port
  whose MAC is later added to the server database can be reauthorized by MAB.
- Inactivity timeout for MAB hosts: 1 to 65535 seconds.
- Reauthentication using SNMP MIB is not supported for 802.1x or MAB.
- Maximum dot1x or MAB client sessions: 2000.
- In multi-auth host mode, MAB can be the per-host fallback for non-802.1x devices on the same port.
- `mab request format attribute 32 vlan access-vlan` (global) enables VLAN-ID-based MAC
  authentication; `no mab logging verbose` filters MAB verbose messages.

## Verify
```
show authentication sessions interface Gi2/0/1
```
The guide's example output lists method `mab`, and logs `%MAB-5-SUCCESS` on success.
- [ ] A printer is authorized via MAB; a device with an unknown MAC lands in the guest VLAN or is denied per policy.

## Checked
2026-11-08. Confirmed against the Catalyst 9300 17.9 Security Configuration Guide chapter
"Configuring IEEE 802.1x Port-Based Authentication": MAB description, enabling procedure,
fallback and EAPOL behaviour, flexible authentication ordering, interaction list, guidelines,
session limit and show output. Removed unsupported content: the IBNS 2.0 policy-map and
convert-to-new-style notes, `mab request format attribute 1 groupsize` and the Calling-Station-Id
claim, the sample AAA/timer/PortFast configuration, the 3 x tx-period 30 s claim, and the ISE,
profiling, dACL and spoofing advice (not in the cited page). The cited MAB-specific page and the
ISE support article were dropped (404/not used).
Method: documentation only; no commands were run.

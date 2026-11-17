---
id: computing-software.cybersecurity-defensive.network-defence.wired-802-1x-authentication
name: wired-802-1x-authentication
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-access-control, 802-1x, eap-tls, peap, radius, cisco-ise, aruba-clearpass, microsoft-nps, dynamic-vlan, monitor-mode]
level: advanced
status: draft
description: "Roll out wired 802.1X: RADIUS/NAC policy, EAP-TLS with machine certificates, monitor-then-closed mode, dynamic VLANs and the switch config that makes it work."
sources: ["IEEE 802.1X-2020 Port-Based Network Access Control", "Cisco Identity-Based Networking Services: IEEE 802.1X deployment guide (monitor, low-impact, closed modes)", "CompTIA Security+ SY0-701 objective 3.2 (802.1X, EAP)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wired 802.1X authentication

**Goal:** only authenticated, managed devices get on the corporate network at the switch port;
everything else lands in a restricted VLAN or nowhere.

## Components
Supplicant (Windows/macOS/Linux client), authenticator (switch), authentication server
(RADIUS: Cisco ISE, Aruba ClearPass, Microsoft NPS, FreeRADIUS), identity source (AD, PKI).

## EAP method
**EAP-TLS** with machine certificates from your PKI (autoenrolled via GPO/Intune SCEP/PKCS) is
the strongest and avoids password prompts. PEAP-MSCHAPv2 is weaker (credential-based, relies on
the client validating the server certificate).

## Switch configuration (Cisco IOS-XE example)
```
aaa new-model
aaa authentication dot1x default group radius
aaa authorization network default group radius
aaa accounting dot1x default start-stop group radius
dot1x system-auth-control
radius server ISE1
 address ipv4 10.0.5.10 auth-port 1812 acct-port 1813
 key <shared secret>
interface GigabitEthernet1/0/10
 switchport mode access
 switchport access vlan 100
 authentication host-mode multi-auth
 authentication order dot1x mab
 authentication priority dot1x mab
 authentication port-control auto
 authentication open                 ! monitor mode: remove for enforcement
 dot1x pae authenticator
 mab
 spanning-tree portfast
```

## Phased rollout
1. **Monitor mode** (`authentication open`): everything still connects; RADIUS logs show who would fail. Fix supplicants and certificates.
2. **Low-impact mode**: pre-auth ACL allows DHCP/DNS/PXE; full access after auth.
3. **Closed mode**: unauthenticated ports get nothing (or a remediation/guest VLAN).

## Authorisation results
Dynamic VLAN assignment or downloadable ACLs / SGTs per device type (corporate laptop, printer, phone, IoT).

## Gotchas
- Printers, phones, cameras rarely support 802.1X: use MAB with profiling (see MAB skill).
- IP phones with PCs behind them need `multi-domain` host mode and voice VLAN.
- RADIUS server outage = nobody connects: configure critical authentication VLAN (`authentication event server dead action authorize vlan`).
- PXE boot and Wake-on-LAN before the supplicant starts need pre-auth access.

## Verify
- [ ] `show access-session interface Gi1/0/10 details` shows Authorized with method dot1x.
- [ ] Unknown laptop plugged in is denied or placed in guest VLAN.

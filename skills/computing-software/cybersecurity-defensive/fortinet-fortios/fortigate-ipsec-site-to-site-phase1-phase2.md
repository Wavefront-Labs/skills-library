---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ipsec-site-to-site-phase1-phase2
name: fortigate-ipsec-site-to-site-phase1-phase2
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [ipsec-phase1, fortios, ipsec, ikev2, phase2, site-to-site-vpn, route-based-vpn, dpd]
level: practitioner
status: draft
description: "Configure a FortiGate route-based site-to-site IPsec VPN with phase 1, phase 2, routes, policies and debug commands."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: a routed tunnel with strong proposals.

```
config vpn ipsec phase1-interface
    edit "to-branch"
        set interface "port1"
        set ike-version 2
        set remote-gw 203.0.113.50
        set proposal aes256-sha256
        set dhgrp 14
        set psksecret <PSK>
        set dpd on-idle
        set dpd-retrycount 3
        set dpd-retryinterval 5
    next
end
config vpn ipsec phase2-interface
    edit "to-branch"
        set phase1name "to-branch"
        set proposal aes256-sha256
        set src-subnet 10.1.0.0 255.255.0.0
        set dst-subnet 10.50.0.0 255.255.0.0
        set auto-negotiate enable
    next
end
config router static
    edit 100
        set dst 10.50.0.0 255.255.0.0
        set device "to-branch"
    next
end
```
Create policies in both directions between the LAN and the tunnel interface `to-branch`. Add a blackhole route (distance 254) for the remote subnet so traffic does not leak out the default route when the tunnel is down.

Gotchas
- Subnet selectors must mirror on both sides or phase 2 fails (a policy-based peer needs matching proxy IDs).
- A NAT device between peers requires NAT traversal (default enabled); open UDP 500/4500.
- PSK in config backups: protect backups.

## Verify
```
diagnose vpn ike gateway list
diagnose vpn tunnel list
get vpn ipsec tunnel summary
diagnose debug application ike -1
diagnose debug enable
```
Disable debug after: `diagnose debug disable` and `diagnose debug reset`.

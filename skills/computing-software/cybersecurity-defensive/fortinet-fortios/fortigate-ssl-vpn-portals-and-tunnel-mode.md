---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ssl-vpn-portals-and-tunnel-mode
name: fortigate-ssl-vpn-portals-and-tunnel-mode
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [ssl-vpn, fortios, sslvpn-portal, tunnel-mode, web-mode, forticlient, sslvpn-policy]
level: practitioner
status: draft
description: "Set up FortiGate SSL VPN tunnel and web mode with portals, address pool and policy, and check release deprecation caveats."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: remote user access with a portal, a tunnel IP pool and a policy.

```
config vpn ssl settings
    set servercert "corp-vpn-cert"
    set tunnel-ip-pools "SSLVPN_TUNNEL_ADDR1"
    set source-interface "port1"
    set source-address "all"
    set port 10443
    set default-portal "full-access"
end
config vpn ssl web portal
    edit "full-access"
        set tunnel-mode enable
        set web-mode disable
        set split-tunneling enable
        set split-tunneling-routing-address "LAN-NET"
    next
end
config firewall policy
    edit 30
        set name "sslvpn-to-lan"
        set srcintf "ssl.root"
        set dstintf "INTERNAL"
        set srcaddr "SSLVPN_TUNNEL_ADDR1"
        set dstaddr "LAN-NET"
        set groups "ENG"
        set action accept
        set service "ALL"
    next
end
```
Deprecation: Fortinet announced removing SSL VPN tunnel mode in newer releases (7.6.x on lower-end models) and recommends IPsec VPN; confirm the status for your version and plan a migration.

Gotchas
- Without `source-address` or geo filtering, the portal is exposed to all internet scanners; restrict it, add MFA, keep firmware current.
- Server certificate should be from a public CA.
- Overlapping tunnel pool and local LAN prevents routing.

## Verify
```
get vpn ssl monitor
diagnose debug application sslvpn -1
```
Connect a client; the monitor lists the user and tunnel IP. Turn debug off after the test.

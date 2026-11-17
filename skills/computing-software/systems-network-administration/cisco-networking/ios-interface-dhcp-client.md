---
id: computing-software.systems-network-administration.cisco-networking.ios-interface-dhcp-client
name: ios-interface-dhcp-client
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-dhcp, ip-address-dhcp, dhcp-client, isp-dhcp, client-id, dhcp-default-route, ip-dhcp-client-default-router-distance, renew-dhcp, release-dhcp, wan]
level: practitioner
status: draft
description: "Use an IOS interface as a DHCP client on ISP or management links: ip address dhcp, client-id and hostname options, default route distance, renew/release and common lease issues."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_dhcp/configuration/xe-16/dhcp-xe-16-book/config-dhcp-client.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IOS interface as a DHCP client

## Configure
```
interface GigabitEthernet0/0/0
 description ISP2-cable
 ip dhcp client client-id GigabitEthernet0/0/0       ! use the MAC as client ID (ISP binding)
 ip dhcp client hostname BR01-RTR
 ip dhcp client default-router distance 250          ! learned default becomes floating
 ip address dhcp
 ip nat outside
 no shutdown
```
The router installs a static default route via the offered gateway, with AD 254 by default
(`S* 0.0.0.0/0 [254/0]`). Set the distance explicitly when another default must win.

## Operate
```
show dhcp lease                               ! address, server, lease times, T1/T2
show ip interface brief | i Gi0/0/0
release dhcp GigabitEthernet0/0/0
renew dhcp GigabitEthernet0/0/0
debug dhcp detail                             ! client-side events
```

## Common issues
- **No address**: cable modem has bound to the previous router's MAC; power-cycle the modem
  or clone the MAC (`mac-address 0011.2233.4455` on the interface).
- **Client ID mismatch**: some ISPs key leases on the MAC; IOS by default sends a client-id
  string like `cisco-0011.2233.4455-Gi0/0/0`. Use the `client-id <interface>` form above to send
  the MAC.
- **Default route missing**: an ACL on the interface blocks UDP 67/68; or the interface is in a
  VRF and the route lands in that VRF table (`show ip route vrf X`).
- **Address changes after reboot** breaks IPsec peers / DNS: use dynamic DNS or IKEv2 with FQDN IDs.

## Tracking the DHCP default
To fail over when the ISP fails upstream, combine with IP SLA:
```
ip dhcp client route track 10        ! under the interface; route removed when track 10 down
```

## Verify
- [ ] `show dhcp lease` shows a bound lease with sensible lease time.
- [ ] Default route present with the intended AD.
- [ ] `renew dhcp` keeps the same address (stable binding).

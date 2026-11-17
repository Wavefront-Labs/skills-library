---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-virtual-ips-destination-nat
name: fortigate-virtual-ips-destination-nat
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [virtual-ip, fortios, vip, destination-nat, port-forwarding, mappedip, inbound-nat]
level: practitioner
status: draft
description: "Publish internal servers on a FortiGate with virtual IPs and a policy that references the VIP as destination."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: inbound access to an internal server on a public address.

```
config firewall vip
    edit "web-vip"
        set extintf "port1"
        set extip 203.0.113.10
        set mappedip "10.1.1.10"
        set portforward enable
        set protocol tcp
        set extport 443
        set mappedport 443
    next
end
config firewall policy
    edit 20
        set name "inbound-web"
        set srcintf "port1"
        set dstintf "DMZ"
        set srcaddr "all"
        set dstaddr "web-vip"
        set action accept
        set schedule "always"
        set service "HTTPS"
        set nat disable
        set logtraffic all
    next
end
```
The VIP object is used as the policy destination address. `nat disable` is the normal setting (the VIP supplies destination NAT); source NAT is used only for hairpin or when the server cannot route back.

Gotchas
- A VIP also installs a proxy ARP entry for the external IP on the interface, so the external IP must be reachable on that segment.
- Port-forwarding VIPs and full 1:1 VIPs behave differently; a 1:1 VIP maps every port and also changes outbound source addresses if `nat-source-vip enable` is set.
- Overlapping VIPs on the same external IP and port cause the first one to win.

## Verify
```
diagnose firewall iprope lookup 198.51.100.7 40000 203.0.113.10 443 tcp port1
diagnose sys session filter dst 203.0.113.10
diagnose sys session list
```

---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-dhcp-server-and-reservations
name: fortigate-dhcp-server-and-reservations
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [dhcp-server, fortios, dhcp-relay, reserved-address, lease-list, ip-range, dhcp-options]
level: practitioner
status: draft
description: "Run a DHCP server on a FortiGate interface with ranges, options and MAC reservations, and read lease tables."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: addressing for a local network without an external DHCP server.

```
config system dhcp server
    edit 1
        set interface "port2"
        set default-gateway 10.1.0.1
        set netmask 255.255.255.0
        set dns-service default
        set lease-time 86400
        set domain "example.internal"
        config ip-range
            edit 1
                set start-ip 10.1.0.100
                set end-ip 10.1.0.200
            next
        end
        config reserved-address
            edit 1
                set ip 10.1.0.20
                set mac 00:00:5e:00:53:01
                set description "printer"
            next
        end
    next
end
```
DHCP relay instead: `config system interface; edit port2; set dhcp-relay-service enable; set dhcp-relay-ip 192.0.2.30`.

Gotchas
- Two DHCP servers on the same segment cause random failures; stop the old one.
- `dns-service default` hands out the FortiGate's configured DNS; use `specify` for your internal resolver.
- Reserved IPs may be outside the range, but must be in the subnet.
- Option 43/66/150 for phones need `config options`.

## Verify
```
execute dhcp lease-list port2
```
A test client gets a lease from the range, and the reserved device receives its fixed address.

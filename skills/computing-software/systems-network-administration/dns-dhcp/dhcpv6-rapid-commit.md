---
id: computing-software.systems-network-administration.dns-dhcp.dhcpv6-rapid-commit
name: dhcpv6-rapid-commit
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcpv6, dhcpv6-rapid-commit, kea, two-message-exchange]
level: practitioner
status: verified
description: "Enable DHCPv6 rapid commit (two-message Solicit/Reply) in Kea, understand client and relay support, and avoid conflicts with multiple servers."
sources:
  - https://www.rfc-editor.org/rfc/rfc8415#section-18.2.1
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html#rapid-commit
  - https://www.rfc-editor.org/rfc/rfc9915
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html
  - https://manpages.debian.org/bookworm/isc-dhcp-common/dhcp-options.5.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 rapid commit

Normally DHCPv6 uses four messages (Solicit, Advertise, Request, Reply). With rapid commit, a client
includes the Rapid Commit option (14) in Solicit and a willing server answers directly with Reply,
committing the lease in two messages.

## Kea
Per subnet (disabled by default; the Kea ARM says it affects only the subnet it is set on):
```json
"subnet6": [{ "id": 1, "subnet": "2001:db8:1::/64", "rapid-commit": true,
  "pools": [ { "pool": "2001:db8:1::1000 - 2001:db8:1::ffff" } ] }]
```

## Clients
- systemd-networkd: `RapidCommit=` in `[DHCPv6]` defaults to true, so it asks for rapid commit
  (systemd.network(5)).
- ISC dhclient: `dhcp6.rapid-commit` is the zero-length option clients send to ask for it
  (dhcp-options(5)); set it with the `send` statement in dhclient.conf, `send dhcp6.rapid-commit;`.

## When not to use it
A server that answers a rapid-commit Solicit with Reply commits the lease without any confirmation.
If more than one server answers, all but one commit leases the client does not use, which can put
wrong data into DNS (if the servers update DNS) and into leasequery answers (RFC 9915). Use rapid
commit only when one server (or a coordinated HA pair with load balancing) answers each client.

## Wireshark
```
dhcpv6.msgtype == 1 && dhcpv6.option.type == 14     # Solicit with rapid commit
dhcpv6.msgtype == 7                                 # Reply
```
Two-message exchanges show Solicit followed directly by Reply containing option 14 (RFC 9915: a server
that accepts must include the Rapid Commit option in its Reply). A Solicit with option 14 built with
scapy matched the first filter above in tshark 4.4.1.

## Verify
- [ ] A rapid-commit client completes in Solicit/Reply and the server shows exactly one lease for it.

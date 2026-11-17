---
id: computing-software.networking-hardware-and-wireless.unbound.home-resolver-setup
name: home-resolver-setup
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, home-network, dhcp, resolver, access-control, dnssec]
level: intro
status: draft
description: "Stand up Unbound as a validating resolver for a home network: install, local test, expose to the LAN, test remotely and set the router's DHCP DNS."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/use-cases/home-resolver.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# home resolver setup
The guide's reasons: DNSSEC validation, no third-party resolver seeing queries, and a local cache.

1. Install (Ubuntu 22.04 example): `sudo apt install unbound -y`; `unbound -V` shows the version. By default it answers only the local host.
2. Test: `dig example.com @127.0.0.1` should show `SERVER: 127.0.0.1#53`.
3. Expose to the network: in the `server:` block set
   - `auto-trust-anchor-file: "/var/lib/unbound/root.key"`
   - `qname-minimisation: yes`
   - `interface: 0.0.0.0` (`::0` optional for IPv6)
   - `access-control: 192.168.0.0/16 allow` (adjust to your subnet)
   and add a `remote-control:` block with `control-enable: yes`.
4. Validate with `unbound-checkconf unbound.conf`, then restart with `unbound-control`.
5. From another machine: `dig example.com @<resolver address>`.
6. Router: find the gateway with `ip route`, then in the router's DHCP settings advertise the Unbound machine's IP as DNS. Devices that ignore the router's settings must be configured individually.

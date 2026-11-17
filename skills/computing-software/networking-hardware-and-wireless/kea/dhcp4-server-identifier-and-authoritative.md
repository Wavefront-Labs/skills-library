---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-server-identifier-and-authoritative
name: dhcp4-server-identifier-and-authoritative
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, server-identifier, authoritative, dhcpnak, echo-client-id]
level: advanced
status: docs-checked
description: "Override the DHCPv4 server identifier, enable authoritative DHCPNAK behaviour, and control client-id echoing in kea-dhcp4."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 server identifier, authoritative mode, client-id echo
Server identifier: by default the server uses the IPv4 address of the interface that received the message, so one instance uses several identifiers if it listens on several interfaces. Override with the `dhcp-server-identifier` option at subnet, shared-network, client-class or global level, never at host-reservation level. A class that sets it must not use `only-in-additional-list`, because such classes are evaluated after subnet selection.

```json
"option-data": [ { "name": "dhcp-server-identifier", "data": "10.2.5.76" } ]
```

Authoritative: for an INIT-REBOOT request from an unknown client on the wrong network, Kea by default stays silent like ISC dhcpd, and only sends DHCPNAK if it has a lease for that client with a different address. Set `authoritative` to true (default false) to always send DHCPNAK to INIT-REBOOT requests from unknown clients. It can be set at global, shared-network and subnet scope and is inherited; all subnets in a shared network must agree.

Client-id echo: since RFC 6842 Kea returns the client-id option when the client sent one. For older devices that refuse it, set `"echo-client-id": false`.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Server Identifier in DHCPv4, Authoritative DHCPv4 Server Behavior and Echoing Client-ID (RFC 6842) (partial read, those sections in full). Confirmed every claim. Nothing removed.

Method: documentation only; no commands were run.

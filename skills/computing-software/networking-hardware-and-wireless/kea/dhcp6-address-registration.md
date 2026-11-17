---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-address-registration
name: dhcp6-address-registration
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, address-registration, rfc-9686, allow-address-registration]
level: advanced
status: docs-checked
description: "Support RFC 9686 self-generated address registration in kea-dhcp6: allow-address-registration, option 148 and registered lease behaviour."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 address registration (RFC 9686)
Since Kea 2.7.7, a valid ADDR-REG-INFORM (36) message adds or updates a registered lease and gets an ADDR-REG-REPLY (37).

- From Kea 3.1.4, enable or disable globally with `allow-address-registration`; it is enabled by default.
- RFC 9686 servers return option 148 to clients that request it in the ORO. Like any standard option it must be in the server configuration to be sent, independent of `allow-address-registration`.
- Registered leases are independent of other states even in a shared lease database: if a lease in another state exists for an address, the address is in use and cannot be registered. A registered lease cannot change state; reclamation of expired registered leases removes them.
- Kea accepts the Option Request option in ADDR-REG-INFORM even though the RFC says the client must not include it.
- Kea accepts addresses "appropriate to the link" but not yet those "within a prefix delegated to the client".

## Checked

2026-11-08. Read dhcp6-srv.rst (Kea ARM source, master branch) sections Address Registration (RFC 9686 Support) in full. Confirmed Kea 2.7.7, Kea 3.1.4, default enabled, option 148, registered-lease notes and the link-appropriate address limit. Nothing removed.

Method: documentation only; no commands were run.

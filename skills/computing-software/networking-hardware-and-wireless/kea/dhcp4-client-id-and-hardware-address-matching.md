---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-client-id-and-hardware-address-matching
name: dhcp4-client-id-and-hardware-address-matching
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, match-client-id, chaddr, client-identifier, lease-lookup]
level: advanced
status: docs-checked
description: "How kea-dhcp4 finds a client's lease by client identifier or chaddr, and when to set match-client-id to false."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 client identifier versus hardware address
DHCPv4 clients may send chaddr (hardware address) and a client-identifier option. Per RFC 2131 the client identifier takes precedence, and Kea follows this by default when it searches, creates, updates or removes leases. Lookup order: by client identifier if present (even if chaddr differs, which covers a replaced network card); otherwise by chaddr; if neither finds a lease, a new one is created. RFC 4361 recommends a DUID as client identifier in dual-stack networks, and Kea supports DUIDs embedded in client identifiers since 2.1.2.

Problem clients: some generate a new client identifier on each connection, or change it during PXE multi-stage boot. Their MAC stays stable, so set `match-client-id` to false to identify them by chaddr.

`match-client-id` can be set globally or per subnet; the subnet value overrides the global one, and the default is true.

After changing the setting: a lease recorded under true is still found by chaddr when set to false, and renewal then records only chaddr. In the other direction, a lease with no recorded client id is assumed to belong to the client. If it holds a different client id, a new lease is allocated.

Since Kea 3.3.2 the setting is ignored when the hardware address is empty (hlen 0).

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Using Client Identifier and Hardware Address in full. Confirmed lookup order, match-client-id scope and default, behaviour after changing it, the Kea 2.1.2 DUID support and the Kea 3.3.2 hlen 0 rule. Nothing removed.

Method: documentation only; no commands were run.

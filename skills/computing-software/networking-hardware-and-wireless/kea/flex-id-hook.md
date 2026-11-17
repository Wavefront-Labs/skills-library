---
id: computing-software.networking-hardware-and-wireless.kea.flex-id-hook
name: flex-id-hook
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, hooks, libdhcp-flex-id, identifier-expression, replace-client-id]
level: advanced
status: docs-checked
description: "Identify clients for reservations with an expression using libdhcp_flex_id: identifier-expression, replace-client-id, ignore-iaid."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# flexible identifier hook
`libdhcp_flex_id.so` (DHCPv4 and DHCPv6, kea-dhcp4/6 only) evaluates an expression for each incoming packet and uses the resulting string as a client identifier, so host reservations can be tied to it. The syntax is the classification expression language, except the result is a string, not a boolean; an empty string is valid (for example when the client sends no specific option).

Parameters:
- `identifier-expression`: the expression.
- `replace-client-id`: default false, so the identifier is used only to search reservations, like hw-address or circuit-id. The drawback: replacing a client device makes the same identifier yield the same lease, and the new device's differing client identifier makes the server refuse the allocation until the old lease expires.
- `ignore-iaid` (v6 only).
- `cid-as-rfc4361-duid` (v4 only).

```json
{ "library": "libdhcp_flex_id.so", "parameters": {
  "identifier-expression": "expression",
  "replace-client-id": false, "cid-as-rfc4361-duid": true } }
```

Docs scenario: an IPv6 network with one interface per customer where client-ids are unreliable and a relay-inserted interface-id is unique per interface; the expression extracts the part of it to use as the identifier.

List this library before HA in `hooks-libraries` so the client ID exists before load balancing uses it.

## Checked

2026-11-08. Read the libdhcp_flex_id.so section of the Hook Libraries chapter (sections 16.9 and 16.9.1 and the parameter list; the rest of the 513 KB hooks page was searched, not read). Confirmed the four parameters, v4/v6 applicability, replace-client-id default false and its lease-conflict drawback, and the interface-id scenario. Description shortened. Nothing removed.

Method: documentation only; no commands were run.

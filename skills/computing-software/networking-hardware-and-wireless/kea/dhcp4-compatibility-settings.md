---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-compatibility-settings
name: dhcp4-compatibility-settings
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, compatibility, lenient-option-parsing, ignore-dhcp-server-identifier]
level: advanced
status: docs-checked
description: "Relax kea-dhcp4 strictness with the compatibility block: lenient-option-parsing, ignore-dhcp-server-identifier, ignore-rai-link-selection, exclude-first-last-24."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 compatibility parameters
All sit under `Dhcp4/compatibility`.

- `lenient-option-parsing`: by default tuple fields in custom options are parsed as length-value pairs and a length exceeding the rest of the buffer is an error. When true, the value becomes the rest of the buffer. From 2.5.8 it also silently ignores FQDN (81) options with some invalid domain names; from 3.1.9 it fixes invalid flags (when S and N are both 1, N is reset to 0, matching ISC DHCP).
- `ignore-dhcp-server-identifier`: when true, the server does not check whether the query was addressed to it.
- `ignore-rai-link-selection`: when true, the Relay Agent Information Link Selection sub-option is not used for subnet selection; not RFC-compliant, default false.
- `exclude-first-last-24`: when true, .0 and .255 are excluded from subnets with prefix length 24 or shorter.

```json
"Dhcp4": { "compatibility": { "lenient-option-parsing": true } }
```

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv4 chapter section Compatibility with Broken Clients and Relays (lenient-option-parsing with the 2.5.8 and 3.1.9 extensions, ignore-dhcp-server-identifier, ignore-rai-link-selection default false, exclude-first-last-24 for prefix length 24 or less). Nothing removed.

---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-custom-and-vendor-options
name: dhcp4-custom-and-vendor-options
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, option-def, option-data, vendor-options, option-space]
level: advanced
status: docs-checked
description: "Define non-standard DHCPv4 options with option-def, set values with option-data, and carry sub-options in the vendor-encapsulated space (option 43)."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# custom and vendor-specific DHCPv4 options
`option-def` only defines the format; `option-data` sets values.

Definition fields: `name`, `code`, `type` are required. Optional: `array` (default false), `record-types` (comma-separated field types, used when `type` is "record"; default empty), `space` (e.g. "dhcp4"), `encapsulate` (name of an option space it carries; default empty). Options with codes 224-254 are reserved for private use and, like code 43, may also be defined inside a client class; other option definitions in classes are not allowed.

Vendor-specific options live in the space `vendor-encapsulated-options-space`, empty by default and carried in Vendor-Specific Information (code 43):

```json
"option-def": [ { "name": "foo", "code": 1,
  "space": "vendor-encapsulated-options-space", "type": "record",
  "array": false, "record-types": "ipv4-address, uint16, string",
  "encapsulate": "" } ],
"option-data": [ { "name": "foo",
  "space": "vendor-encapsulated-options-space", "code": 1,
  "csv-format": true, "data": "192.0.2.3, 123, Hello World" } ]
```

Also include the Vendor-Specific Information option (43) itself in `option-data`; the docs say this is required, otherwise the option is not included in messages sent to the client.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv4 chapter sections Custom DHCPv4 Options, DHCPv4 Private Options and DHCPv4 Vendor-Specific Options (required fields, defaults, the foo example, option 43 requirement). Loosened the record-types wording to what the page states.

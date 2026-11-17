---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-server-id-duid-and-data-directory
name: dhcp6-server-id-duid-and-data-directory
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, server-id, duid, data-directory, kea-dhcp-data-dir]
level: advanced
status: docs-checked
description: "Select the kea-dhcp6 server DUID type and know where the DUID and memfile lease file are stored, including the data-directory deprecation."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 server identifier and data directory
The server identifier is a DUID. RFC 9915 defines four types: DUID-LLT, DUID-EN, DUID-LL and DUID-UUID. Kea generates one on first startup, stores it in a file and keeps it stable across restarts. DUID-LLT is the default, following the RFC.

Choose a type in the global `server-id` map; supported `type` values are "LLT", "EN" and "LL":

```json
"Dhcp6": { "server-id": { "type": "EN" } }
```

When a new type is selected, the server generates a value and replaces the DUID in the file.

The DUID file and the default memfile lease file live in the data directory, by default `[kea-install-dir]/var/lib/kea`. The `data-directory` parameter is deprecated as of Kea 2.7.9: duid and lease files may only be loaded from the compiled-in path, which can be overridden at startup with the environment variable `KEA_DHCP_DATA_DIR`. A different path in `data-directory` makes Kea refuse to start, or log an unrecoverable error if running.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv6 chapter sections Server Identifier in DHCPv6 (RFC 9915 types, LLT default, server-id type values LLT/EN/LL, regeneration on type change) and the data-directory note (2.7.9, KEA_DHCP_DATA_DIR). Nothing removed.

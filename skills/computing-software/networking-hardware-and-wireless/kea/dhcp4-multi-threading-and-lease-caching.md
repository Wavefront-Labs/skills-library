---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-multi-threading-and-lease-caching
name: dhcp4-multi-threading-and-lease-caching
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, multi-threading, thread-pool-size, cache-threshold, cache-max-age]
level: advanced
status: docs-checked
description: "Tune kea-dhcp4 throughput with multi-threading settings and lease caching (cache-threshold, cache-max-age)."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 multi-threading and lease caching
Multi-threading is configured under `multi-threading`:
- `enable-multi-threading`: default true.
- `thread-pool-size`: 0 auto-detects; a positive number sets the count. Default 0.
- `packet-queue-size`: 0 is unlimited; default 64.

```json
"multi-threading": { "enable-multi-threading": true,
  "thread-pool-size": 4, "packet-queue-size": 16 }
```

Lease caching avoids database writes for clients that renew repeatedly. The server reuses the lease unchanged except CLTT, which needs no disk operation. Parameters at global, shared-network or subnet level (subnet wins):
- `cache-threshold`: fraction of the valid lifetime allowed as lease age. Values at or below 0.0 or above 1.0 disable caching. Default 0.25 since Kea 3.0.0.
- `cache-max-age`: seconds; 0 disables caching. Unspecified by default.

A lease is not reusable after an important change such as DDNS parameters, hostname or a valid-lifetime reduction. Example: with a 2000 second lifetime and threshold .25, a lease committed under 500 seconds ago is reused. The `dhcp-lease-time` in replies is the reusable remaining lifetime.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (DHCPv4 server chapter (multi-threading, lease caching)). Removed: nothing.
Method: documentation only; no commands were run.

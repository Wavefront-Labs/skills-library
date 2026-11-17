---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-sanity-checks-and-extended-lease-info
name: dhcp4-sanity-checks-and-extended-lease-info
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, sanity-checks, lease-checks, store-extended-info, stash-agent-options]
level: advanced
status: docs-checked
description: "Set lease-checks sanity levels when loading leases, store extended lease info, and stash relay agent options in kea-dhcp4."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 sanity checks, extended lease info, stash agent options
`sanity-checks` / `lease-checks` governs what happens when a loaded lease's subnet-id no longer matches the configuration (for example a subnet was temporarily removed). Levels:
- `none`: accept as is.
- `warn`: warn but accept; the default.
- `fix`: try to correct, otherwise insert the data anyway.
- `fix-del`: try to correct, otherwise reject the lease.
- `del`: reject any inconsistent lease; strictest.

Currently implemented for the memfile backend, and applied to the in-memory lease database, not the file: inconsistent leases stay in the lease file.

```json
"sanity-checks": { "lease-checks": "fix-del" }
```

`store-extended-info` (default false; global, shared-network, subnet) adds DHCPREQUEST details to the lease user context under "ISC", including relay-agent-info (option 82) and remote-id and relay-id when present. It is needed for Leasequery and stash agent options. Values from the last DHCPREQUEST that contained them are kept. Extended info is also checked by `extended-info-checks` in `sanity-checks`: `none`, `fix` (default; also upgrades the old format), `strict` (fixes inconsistencies that affect the Leasequery hook) and `pedantic` (full conformance to Kea's own format). Like `lease-checks` it is implemented only for memfile and applies to the in-memory lease database.

`stash-agent-options` (global, default false, since 2.5.8): records the relay agent information options from the initial SELECTING-state DHCPREQUEST and acts as if they appear in later RENEWING requests, which are unicast and skip the relay.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv4 chapter sections Sanity Checks in DHCPv4, Storing Extended Lease Information and Stash Agent Options (levels, default warn, memfile-only, ISC user-context map, 2.5.8). Added the extended-info-checks levels from the same section.

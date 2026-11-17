---
id: computing-software.cybersecurity-defensive.suricata.eve-community-id-xff-multitenancy
name: eve-community-id-xff-multitenancy
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [community-id, xff, x-forwarded-for, tenant-id]
level: practitioner
status: docs-checked
description: "Enrich EVE with community_id for cross-tool correlation, X-Forwarded-For handling modes, and tenant_id."
sources: ["https://docs.suricata.io/en/latest/output/eve/eve-json-output.html", "https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# community-id, xff, tenants

## Community ID
`community-id: true` adds `community_id` so records line up with tools such as Zeek. `community-id-seed` (0 to 65535, default 0) must match across all tools.

## xff
Replaces or supplements IPs from the X-Forwarded-For header (disabled by default).
- `mode`: `extra-data` or `overwrite`.
- `deployment`: `reverse` (uses the last IP) or `forward` (the first IP).
- `header`: the header name, `X-Forwarded-For` by default.

## Tenants
With separate per-tenant detection configurations, EVE adds `tenant_id` to matching traffic.

Related: `flow` and `netflow` records; netflow is unidirectional so there are about twice as many as flow records.

## Checked

Method: docs-checked 2026-11-09 against https://docs.suricata.io/en/latest/output/eve/eve-json-output.html (read the eve-log config block, netflow, community flow ID and tenant sections); the suricata.yaml page was not needed for these claims.

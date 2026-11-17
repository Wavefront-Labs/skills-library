---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.hybrid-version-compat
name: hybrid-version-compat
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, version-compatibility, data-plane-version, clustering-data-planes, hybrid-mode, upgrade]
level: advanced
status: docs-checked
description: "Version rules between Kong control and data planes (same major, DP minor not newer, patch ignored), plugin version rules, and checking DP versions via the Admin API."
sources:
  - https://developer.konghq.com/gateway/hybrid-mode/
  - https://developer.konghq.com/gateway/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid version compatibility

Self-managed rules:
- A control plane only accepts data planes with the same major version.
- A DP with a newer minor version than the CP is rejected; a newer patch version is accepted.
- Plugins: major versions must match, a DP plugin's minor version cannot be newer than the CP's, and patch versions are ignored.
- Configuration is not pushed to incompatible DPs.

Konnect Dedicated Cloud Gateways require CP and DP versions to match exactly.

Check connected data planes with the Admin API endpoint `/clustering/data-planes` (on-prem). In Konnect use `/expected-config-hash`.

Upgrade order for hybrid deployments: upgrade control planes first (dual-cluster or in-place), then data planes with a rolling upgrade.
DB-less deployments use a rolling upgrade; traditional mode uses dual-cluster if spare hardware exists, otherwise in-place.

Back up configuration and read the breaking changes and changelog before starting.

## Checked

2026-11-04. Confirmed against the Hybrid mode page (version rules, plugin rules, no push to incompatible DPs, Dedicated Cloud Gateway exact match, the two endpoints) and the Upgrade page (strategy table, CP first, backup and changelog). Nothing removed.
Method: documentation only; no commands were run.

---
id: computing-software.networking-hardware-and-wireless.envoy.http-upgrades-and-websocket
name: http-upgrades-and-websocket
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, upgrade-configs, websocket, connect, http-upgrade, buffer-filter]
level: practitioner
status: docs-checked
description: "Enable or disable WebSocket and CONNECT upgrades per HCM and per route, and keep the buffer filter out of the upgrade filter chain."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/http/upgrades.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http upgrades and websocket
Envoy upgrade support targets WebSocket and CONNECT but works for arbitrary upgrades. Both the upgrade headers and the upgraded payload pass through an HTTP filter chain. Configure `upgrade_configs` on the HTTP connection manager:

```yaml
upgrade_configs:
- upgrade_type: websocket
  filters:
  - name: envoy.filters.http.router
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```
With only `upgrade_type`, headers and body go through the default HTTP filter chain. Setting `filters` gives that upgrade type its own chain, down to just the router, so HTTP-only filters never see the opaque payload. Custom chains can be set only on the HCM, not per route.

Per-route `upgrade_configs` can enable or disable an upgrade and override the HCM setting; the docs table shows the default is enabled, a route-level disable turns it off, and a route-level enable works even if the HCM disabled it.

Gotchas: buffering is generally incompatible with upgrades, so leave the buffer filter out of the upgrade `filters` list. All upgrade statistics are bundled (`downstream_cx_upgrades_total`, `downstream_cx_upgrades_active`), so WebSocket is not separated from other upgrades. Verify by opening a WebSocket and watching `downstream_cx_upgrades_active`.

## Checked
2026-11-03. Confirmed against upgrades.rst and the router filter reference. Removed or corrected: nothing.
Method: documentation only; no commands were run.

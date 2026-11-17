---
id: computing-software.systems-network-administration.headscale.derp-custom-map
name: derp-custom-map
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, derp-map, regions, derp-yaml, urls]
level: advanced
status: docs-checked
description: "Customise the DERP map in Headscale: disable default regions, add your own regions in derp.yaml, or serve only custom DERP servers."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/derp.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom DERP maps

Config keys: `derp.urls` (remote maps, default `https://controlplane.tailscale.com/derpmap/default`), `derp.paths` (local files), `derp.auto_update_enabled: true` and `derp.update_frequency: 3h`.

## Default map minus one region, plus a file

```yaml
derp:
  server:
    enabled: false
  urls:
    - https://controlplane.tailscale.com/derpmap/default
  paths:
    - /etc/headscale/derp.yaml
```

## Only custom servers

```yaml
derp:
  server:
    enabled: false
  urls: []
  paths:
    - /etc/headscale/derp.yaml
```

## derp.yaml

Extensions `.yaml`, `.yml`, `.json`, `.hujson` (JSON ones parse as HuJSON). Disable a region by setting it to null (region 1 is New York):

```yaml
regions:
  1: null
```

The docs add custom regions (e.g. ID 900, regioncode `custom-east`, nodes with `hostname`, `ipv4`, `ipv6`, `canport80: true`). See `derp-example.yaml` in the repository and the Go `DERPMap` types for fields.

## Ports for custom DERP servers

udp/3478 STUN, tcp/443 relay, tcp/80 captive-portal checks (`canport80: true`).

## Gotcha

Emptying `urls` removes Tailscale's DERP servers, so only your custom or embedded servers remain; check connectivity before relying on them. The embedded server, if enabled, is merged into the map automatically (`automatically_add_embedded_derp_region: true` by default).

## Checked

2026-11-04. Confirmed against the Headscale DERP reference and config-example.yaml: derp.urls default, paths, auto_update_enabled, update_frequency 3h, file extensions and HuJSON, null region removal (region 1 is New York), the custom region example with ID 900, and the ports. Replaced an unsourced gotcha.
Method: documentation only; no commands were run.

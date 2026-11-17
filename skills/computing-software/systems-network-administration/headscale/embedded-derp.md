---
id: computing-software.systems-network-administration.headscale.embedded-derp
name: embedded-derp
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, derp, embedded, stun, udp-3478]
level: practitioner
status: docs-checked
description: "Enable Headscale's embedded DERP relay: config keys, public IPs, STUN on udp/3478, region defaults, and its known limitations."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/derp.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedded DERP server

Disabled by default. Enable it explicitly:

```yaml
derp:
  server:
    enabled: true
    ipv4: 198.51.100.1
    ipv6: 2001:db8::1
```

Setting the public IPv4 and IPv6 addresses improves stability. Example-config defaults: `region_id: 999`, `region_code: "headscale"`, `region_name: "Headscale Embedded DERP"`, `stun_listen_addr: "0.0.0.0:3478"` (MUST be defined when enabled), and a private key at `/var/lib/headscale/derp_server_private.key` (generated if missing).

## Ports

- udp/3478 STUN, used to help clients discover their public IP and traverse NAT.
- Further ports are needed to run a DERP server: see "ports in use" in the Headscale requirements page.
- `server_url` must use https because DERP requires TLS (config example).

## Verify

```
tailscale debug derp-map
tailscale debug derp headscale
```

The second assumes the default region code.

## Limitations

- Cannot serve Tailscale's captive portal checks: no `/generate_204` over HTTP on tcp/80.
- No speed or throughput optimisations; it exists to help node connectivity.

## Gotcha

Removing Tailscale's default DERP servers makes the embedded one a single point of failure; test it first (derp-custom-map).

## Checked

2026-11-04. Confirmed against the Headscale DERP reference and config-example.yaml: disabled by default, ipv4 and ipv6 keys, region_id 999, region_code, region_name, stun_listen_addr, private_key_path, the debug commands and footnote, and both limitations. Replaced an unsourced tcp/443 port statement for the embedded server.
Method: documentation only; no commands were run.

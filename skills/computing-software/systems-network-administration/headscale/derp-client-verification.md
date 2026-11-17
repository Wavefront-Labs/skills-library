---
id: computing-software.systems-network-administration.headscale.derp-client-verification
name: derp-client-verification
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, verify-clients, derper, verify-client-url, fail-open]
level: advanced
status: docs-checked
description: "Restrict DERP relay use to your own clients: verify_clients on the embedded server, or derper's -verify-client-url against Headscale /verify."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/derp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DERP client verification

## Embedded server

```yaml
derp:
  server:
    verify_clients: true
```

True by default: relay access is denied to unknown clients ("only allow clients associated with this server").

## Third-party derper

Point a standalone `derper` at the Headscale verify endpoint:

- `-verify-client-url` set to `https://headscale.example.com/verify`
- `-verify-client-url-fail-open` controls what happens when Headscale is unreachable; access is allowed by default.

## Why it matters

Verification restricts DERP access to nodes that are members of your tailnet; relay access is denied for unknown clients. With `-verify-client-url-fail-open` at its default, the DERP server allows access when it cannot reach Headscale.

## Verify

```
tailscale debug derp headscale
```

from a registered client checks connectivity to the embedded DERP. DERP metrics and debug information are on the metrics and debug endpoint (debug-endpoint).

## Checked

2026-11-04. Confirmed against the Headscale DERP reference and config-example.yaml: verify_clients default, derper flags and /verify endpoint, fail-open default, and the connectivity check. Replaced an unsourced fail-closed recommendation.
Method: documentation only; no commands were run.

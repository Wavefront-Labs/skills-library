---
id: computing-software.messaging-and-integration.nats.server-tls-configuration
name: server-tls-configuration
category: computing-software
field: messaging-and-integration
product: nats
tags: [tls, cert-file, verify, pinned-certs, handshake-first, certificate-rotation]
level: practitioner
status: docs-checked
description: "Enable TLS in nats-server: tls map keys, min_version, timeout, verify, pinned_certs, rate limit, TLS-first handshake, reload for rotation."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/securing_nats/tls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt client, route and monitoring traffic and optionally require client certificates.

Minimal config:
```
tls: {
  cert_file: "./server-cert.pem"
  key_file: "./server-key.pem"
}
```
Equivalent flags: `nats-server --tls --tlscert=./server-cert.pem --tlskey=./server-key.pem`. Startup logs "TLS required for client connections".

Keys in the `tls` map: `cert_file`, `key_file`, `ca_file` (defaults to the system trust store), `cipher_suites` (must match the Go build's names), `curve_preferences`, `insecure` (outgoing only; not recommended), `min_version` (default "1.2"), `timeout` (handshake, default 2 seconds), `verify` (require and verify client certificates; not applied to monitoring), `verify_and_map` (also maps certificate values to a user), `verify_cert_and_check_known_urls` (cluster/gateway contexts), `pinned_certs` (hex SHA256 of DER public key fingerprints; connection closed if absent), `connection_rate_limit` (new TLS client connections per second; default 0 = off).

A root-level `tls` also covers the monitoring port when `https_port` is set; `cluster` and other sections take their own `tls` blocks. Debug logging (`-D`/`-DV`) shows TLS version and cipher per client.

TLS-first (2.10.4+): add `handshake_first: true` so no clear-text INFO is sent; only clients with an equivalent option can connect. `auto` or a duration such as `250ms` falls back to the old behavior.

Rotation: changed certificate files need a configuration reload; make `ca_file` include all CAs/intermediates across servers since they rarely rotate simultaneously.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.

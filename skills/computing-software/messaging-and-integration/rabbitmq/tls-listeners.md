---
id: computing-software.messaging-and-integration.rabbitmq.tls-listeners
name: tls-listeners
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, tls-listeners, rmq-tls]
level: advanced
status: docs-checked
description: "Enable TLS on AMQP listeners with a server certificate, key and CA chain and restrict to TLS 1.2 and 1.3."
sources:
  - https://www.rabbitmq.com/docs/ssl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS listeners

**Goal:** Encrypt client traffic.

## Steps
1. In `rabbitmq.conf`: `listeners.ssl.default = 5671`, `ssl_options.cacertfile`, `ssl_options.certfile`, `ssl_options.keyfile` (placeholders for paths).
2. To restrict versions, `ssl_options.versions.1 = tlsv1.3` accepts only TLSv1.3; `ssl_options.versions.1 = tlsv1.2` disables older versions. On Erlang 26 and 27 TLSv1.3 and TLSv1.2 are enabled by default. Clients with old runtimes may not connect if you restrict versions.
3. Rotate certificates by replacing the files on disk, then clear the cache: `rabbitmqctl eval -n <node> 'ssl:clear_pem_cache().'`. Without that, the new pair is picked up after the runtime purges its cache.
4. Disable plain listeners with `listeners.tcp = none`.

## Failure modes
- Expired certificates produce a "Certificate Expired" alert and cut handshakes.

## Verify
- `openssl s_client -connect host:5671` (add `-tls1_3` to check that version); `rabbitmq-diagnostics listeners` shows the TLS listener.

## Checked

Date: 2026-11-02. Confirmed on the TLS guide: listener and file keys, version settings and defaults, rotation with `ssl:clear_pem_cache()`, `listeners.tcp = none`, s_client and `listeners`. Fixed: the restart-based rotation step was replaced. Removed: `versions.2`, the chain-order failure mode.

Method: documentation only; no commands were run.

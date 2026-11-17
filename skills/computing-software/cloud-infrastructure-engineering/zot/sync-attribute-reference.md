---
id: computing-software.cloud-infrastructure-engineering.zot.sync-attribute-reference
name: sync-attribute-reference
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, sync-config, sync-retries, content-filter, platforms-filter, req-per-sec, only-signed]
level: advanced
status: docs-checked
description: "Reference of Zot sync registry and content attributes with defaults: retries, timeouts, TLS, concurrency, tag filters, destinations, platforms and signed-only."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/mirroring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Per registry entry in `extensions.sync.registries`:

- `urls`: tried in listed order if the main URL fails. `credentialsFile`: JSON mapping hosts to `username`/`password`.
- `tlsVerify` default `true`; `certDir` (since v2.1.23 all `.crt` files join the CA bundle).
- `maxRetries` (default none), `retryDelay` (required with `maxRetries`), `maxRetryDelay` (enables exponential backoff, must be at least `retryDelay`).
- `syncTimeout` default 3 hours, on-demand only.
- `manifestCheckInterval` default `0s`, on-demand only.
- `onlySigned`: true syncs only notation- or cosign-signed images.
- `syncLegacyCosignTags` default `true`.
- `reqConcurrent` default 3 and `reqPerSec` default unlimited, per upstream host.
- `disableHTTP2`: true uses HTTP/1.1. `maxIdleConnsPerHost`: Go default 2, equals `reqConcurrent` when HTTP/2 is disabled.
- `platforms`: periodic sync only; `os/arch[/variant]` or bare arch; default all; `""` keeps descriptors with no platform. The index keeps its upstream digest even when only some children are stored.

Under `content`: `prefix` (exact path or glob), `tags.regex`, `tags.semver`, `destination`, `stripPrefix`, and `platforms` overriding the registry value (on-demand ignores it).

`pollInterval` applies only when `content` is set; examples use strings like `"6h"`. `preserveDigest` is deprecated.

## Checked

2026-11-08. Read in full: docs/articles/mirroring.md and compared every claim above against it. Removed: the stated defaults for tags.semver and stripPrefix (the page describes both values but names no default).

Method: documentation only; no commands were run.

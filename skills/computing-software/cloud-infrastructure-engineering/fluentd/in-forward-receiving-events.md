---
id: computing-software.cloud-infrastructure-engineering.fluentd.in-forward-receiving-events
name: in-forward-receiving-events
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, in-forward, forward, aggregator, shared-key, security, tls]
level: practitioner
status: docs-checked
description: "Receive events from other Fluentd instances or fluent-cat with in_forward: port and bind, tag override and prefix, size limits, shared-key security and TLS transport."
sources:
  - https://docs.fluentd.org/input/forward
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in_forward
Listens on TCP for event streams and on UDP for heartbeats; the most efficient way to receive events from other Fluentd instances, `fluent-cat` or client libraries. For raw TCP payloads use `in_tcp`.
```
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>
```
- `port` (24224), `bind` (0.0.0.0), `backlog`.
- `tag` (1.5.0) replaces the incoming tag; `add_tag_prefix` (1.5.0) prepends, e.g. `prod.app.log`.
- `chunk_size_limit` drops larger chunks; `chunk_size_warn_limit` only warns.
- `decompression_size_limit` (1.19.3, 256MB): applies to compressed sends from `out_forward`; oversize chunks are not processed and the connection closes.
- `skip_invalid_event` (default true since 1.19.0).
- `source_address_key`, `source_hostname_key`: add client address or hostname to each record (extra time on large chunks).
- `deny_keepalive`, `send_keepalive_packet`, `resolve_hostname`.
- `<transport tls>` with `cert_path` enables TLS; without it raw TCP is used. `linger_timeout` moved into `<transport>` in 1.14.6.
- `<security>`: `self_hostname`, `shared_key` (both required), `user_auth` with `<user>` (`username`, `password`), `allow_anonymous_source` (default true; if disabled `<client>` sections with `host` or `network` are required).

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/input/forward and confirmed: port, tag and add_tag_prefix, size limits, skip_invalid_event default, security section parameters. Removed or reworded: nothing.

Method: documentation only; no commands were run.

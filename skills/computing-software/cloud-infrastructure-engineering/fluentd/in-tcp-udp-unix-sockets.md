---
id: computing-software.cloud-infrastructure-engineering.fluentd.in-tcp-udp-unix-sockets
name: in-tcp-udp-unix-sockets
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, in-tcp, in-udp, in-unix, delimiter, remove-newline, message-length-limit]
level: practitioner
status: docs-checked
description: "Receive raw payloads with in_tcp and in_udp (tag, parse, delimiter, remove_newline, message_length_limit) and forward-protocol events over a Unix socket with in_unix."
sources:
  - https://docs.fluentd.org/input/tcp
  - https://docs.fluentd.org/input/udp
  - https://docs.fluentd.org/input/unix
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in_tcp, in_udp and in_unix
```
<source>
  @type tcp
  tag tcp.events
  port 5170
  delimiter "\n"
  <parse>
    @type regexp
    expression /^(?<field1>\d+):(?<field2>\w+)$/
  </parse>
</source>
```
- **in_tcp** (not for Fluentd client libraries; use `in_forward`): `tag` required, `port` 5170, `bind`. `delimiter` is a plain string, can be several characters, and the delimiter itself is not passed on. With `message_length_limit` (1.16.1), overlong data is discarded until the next delimiter. `<transport tls>` enables TLS; `<security><client>` limits by `host` or `network`.
- **in_udp**: `tag` required, `port` 5160, `message_length_limit` default 4096 bytes, `remove_newline` default true (set `false` for binary payloads containing `0x0a`/`0x0d`). If `RcvbufErrors` in `netstat -su` grows, packets are dropped; try multiple workers.
- Both: `<parse>` required; `source_hostname_key`, `source_address_key` (1.4.2) add client info; tune kernel parameters for high volume.
- **in_unix**: same wire protocol as `in_forward` over a socket. `path` defaults to `/var/run/fluent/fluent.sock` (or `FLUENT_SOCKET`), `backlog`, `tag` (1.11.0).

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/input/tcp, https://docs.fluentd.org/input/udp, https://docs.fluentd.org/input/unix and confirmed: ports, delimiter behaviour, message_length_limit, remove_newline, RcvbufErrors advice, unix path default. Removed or reworded: nothing.

Method: documentation only; no commands were run.

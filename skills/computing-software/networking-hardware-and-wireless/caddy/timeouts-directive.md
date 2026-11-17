---
id: computing-software.networking-hardware-and-wireless.caddy.timeouts-directive
name: timeouts-directive
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [timeouts, read-timeout, write-timeout, min-rate, max-write-chunk, slowloris, caddyfile]
level: advanced
status: docs-checked
description: "Set per-request idle read and write timeouts, minimum transfer rates and write chunk size with the experimental timeouts directive, and why server defaults override it."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/timeouts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: abort stalled connections for specific routes without touching server-wide settings.

Experimental. Syntax: `timeouts [<matcher>] { read_timeout <duration> [<min_rate>]  write_timeout <duration> [<min_rate>]  max_write_chunk <size> }`. These are idle timeouts that reset after every successful read or write, so slow clients that keep progressing are unaffected.

`read_timeout`: how long a read of the request body may stall. No idle read timeout is applied by default. The optional `min_rate` is bytes per second averaged from the start of the body; the allowed time becomes the duration plus the time to send the bytes so far at that rate, which stops clients that send just enough to never stall.

`write_timeout`: how long a write to the client may stall; reset before each write. Its `min_rate` works similarly but is averaged from the response start, so pauses between writes count against it. Avoid it for long streaming responses like server-sent events.

`max_write_chunk`: largest size of one underlying write, so `write_timeout` applies per chunk of a big response rather than the whole write. Accepts go-humanize sizes; only matters when `write_timeout` is set; default `64KiB`.

Critical precedence: the server-wide `read_body_idle` and `write_idle` timeouts are on by default and are applied after this directive's on each read and write, so they win. To let `read_timeout` or `write_timeout` work, disable the matching global timeout, for example `read_body_idle -1s` in the `timeouts` global option.

Examples: `timeouts /upload* { read_timeout 10s 1024 }` aborts uploads stalling over 10 s or averaging under 1 KiB/s; `timeouts /files/* { write_timeout 30s  max_write_chunk 16KiB }` checks downloads between 16 KiB chunks.

## Checked

2026-11-03: read caddyfile/directives/timeouts against this skill. Confirmed: experimental status, read_timeout, write_timeout, min_rate semantics, max_write_chunk default 64KiB, precedence of read_body_idle and write_idle, both examples.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.

---
id: computing-software.database-administration.memcached.meta-pipelining-quiet-opaque-noop
name: meta-pipelining-quiet-opaque-noop
category: computing-software
field: database-administration
product: memcached
tags: [pipelining, quiet-mode, opaque, mn, meta-noop]
level: advanced
status: docs-checked
description: "Pipeline meta commands efficiently with q quiet mode, O opaque tokens (32 bytes max), k key, and an mn terminator."
sources:
  - https://docs.memcached.org/protocols/meta/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Metaget has no multi-key interface, so fetch many keys by pipelining: `mg foo v\r\nmg bar v\r\nmg baz v\r\n`. Metaget does not return the key by default; clients should look at response codes to count responses.

Tools:
- `q` hides nominal responses (the `EN` miss code for mg; the success code for ms and md). Errors and other codes such as `EX` for a failed CAS still come back, as do syntax errors (`CLIENT_ERROR`).
- Without `q` and the key you cannot match responses to requests. Use `k` (adds the key as a token, works for mg, ms and md; wasteful with long keys and small data) or `O<opaque>` (tokens reflected back as-is, up to 32 bytes; a simple approach is to count outstanding requests with short numbers).
- If all keys may be misses you cannot tell when processing finished. Either send the final mg without `q` (which adds an `EN`), or end the pipeline with `mn\r\n`, which responds with a bare `MN\r\n`.

Example:
```
mg foo v q O1\r\nmg bar v q O2\r\nmn\r\n
VA 2 O1\r\nhi\r\nMN\r\n
```
(foo hits and bar misses silently.) The same approach works for pipelined sets: `ms foo 2 q` hides the success code.

## Checked

2026-11-04. Confirmed against the Meta page (Pipelining Quiet mode with Opaque or Key, Quiet mode semantics) and protocol.txt (O token limit, mn). Removed: nothing factual; wording aligned to the page.

Method: documentation only; no commands were run.

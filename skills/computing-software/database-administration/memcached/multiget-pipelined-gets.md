---
id: computing-software.database-administration.memcached.multiget-pipelined-gets
name: multiget-pipelined-gets
category: computing-software
field: database-administration
product: memcached
tags: [multiget, get, gets, pipelining, round-trip]
level: practitioner
status: docs-checked
description: "Fetch many keys in one get request instead of a loop of single gets, and understand the multiget hole at larger cluster sizes."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/userguide/faq/
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`get key1 key2 key3` returns a `VALUE <key> <flags> <bytes>` line plus data block per item found and finishes with `END`; keys not found are simply absent. `gets` works the same way (adding the CAS value), and `gat <exptime> <key>*` fetches and updates the expiration time.

Anti-pattern from the FAQ: a loop that calls `get` for each id. Fetching a single item still requires a network roundtrip and a little processing, so use pipelined gets instead: the more you fetch at once the better.

The multiget hole (Performance page): as you add servers, multigets are more spread out. A multiget for 10 keys against 2 servers turns into two syscalls, one per server; with 10 servers it ends up one syscall per server. The servers do more syscalls on smaller incoming requests and their capacity drops. It is not insurmountable: with many clients you can group related keys (for example all keys for one user's profile) on the same instance, so a multiget hits a single server with far fewer syscalls in total.

The meta protocol has no multi-key `mg`; pipeline several `mg` commands (see the meta-pipelining-quiet-opaque-noop skill).

## Checked

2026-11-04. Confirmed against protocol.txt (retrieval commands, gat), the FAQ ("Can using memcached make my application slower?") and the Performance page (The Multiget Hole). Removed: the closing `-vv` verification tip, which no page states.

Method: documentation only; no commands were run.

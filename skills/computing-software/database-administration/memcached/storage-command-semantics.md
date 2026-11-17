---
id: computing-software.database-administration.memcached.storage-command-semantics
name: storage-command-semantics
category: computing-software
field: database-administration
product: memcached
tags: [set, add, replace, append, prepend]
level: practitioner
status: docs-checked
description: "Choose between set, add, replace, append, prepend and cas, the exact wire syntax, and their reply codes."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Wire format:
```
<cmd> <key> <flags> <exptime> <bytes> [noreply]

<data block>

cas <key> <flags> <exptime> <bytes> <cas unique> [noreply]

```
- set: store always. add: only if the key is absent. replace: only if present.
- append / prepend: add data after / before existing data; they ignore flags and exptime and apply only to an existing key.
- cas: store only if nobody changed it since your `gets`.
- flags: opaque 16-bit client value (may be 32-bit from 1.2.1). bytes may be 0.

Replies: `STORED`, `NOT_STORED` (add/replace condition unmet, not an error), `EXISTS` (cas lost), `NOT_FOUND` (cas on a missing key).

Check: `printf 'set k 0 60 2
hi
' | nc localhost 11211` returns `STORED`.

Meta equivalents: `ms` with `MA`, `MP`, `ME`, `MR` modes (see meta-set skill).

## Checked

Confirmed 2026-11-09: command line syntax for set, add, replace, append, prepend and cas; semantics of each; append and prepend ignore flags and exptime; flags width; bytes may be zero; replies STORED, NOT_STORED, EXISTS and NOT_FOUND; meta mode letters E, A, P, R, S (protocol.txt storage commands and metaset). Reworded the append/prepend failure statement to the documented wording.

Method: docs-checked 2026-11-09 against memcached doc/protocol.txt

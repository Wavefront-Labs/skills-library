---
id: computing-software.database-administration.memcached.key-rules-and-item-size
name: key-rules-and-item-size
category: computing-software
field: database-administration
product: memcached
tags: [key-length, item-size, i-flag, store-too-large, 250-characters]
level: practitioner
status: docs-checked
description: "Key and value limits in memcached: keys up to 250 characters without whitespace or control chars, 1 MB default item size (-I)."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/userguide/usecases/
  - https://docs.memcached.org/serverguide/configuring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Keys: at most 250 characters, no control characters or whitespace. The usecases guide says this may be raised to 65k in the future.

Binary or odd keys: with the meta protocol, send base64 and add the `b` flag (see binary-keys-base64 skill).

Item size: default `item_size_max 1048576` (1 MB) in `stats settings`. `-I` raises it (for example `-I 2m`). The Loki guide pairs `-I 2m` with 1.5 MB chunks.

Failure behaviour: a failed `set` against an existing key also removes the old item (see set-failure skill).

A `set` rejected as too large counts as a failed set: see the set-failure skill.

## Checked

2026-11-04. Confirmed against protocol.txt (250-character key limit, no whitespace or control characters), the use-cases guide (65k note), the Configuring page (item_size_max 1048576) and the Performance page (failed set removes old item). Removed: the store_too_large claim, the unsourced list-splitting advice and the closing Verify tip.

Method: documentation only; no commands were run.

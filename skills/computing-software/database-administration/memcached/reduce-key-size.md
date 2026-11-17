---
id: computing-software.database-administration.memcached.reduce-key-size
name: reduce-key-size
category: computing-software
field: database-administration
product: memcached
tags: [key-size, memory-savings, key-compression, base64, slab-class]
level: intro
status: docs-checked
description: "Save memory by shortening keys, base64-encoding numbers and using binary keys, but only when memory is genuinely scarce."
sources:
  - https://docs.memcached.org/userguide/usecases/
  - https://docs.memcached.org/protocols/meta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Smaller keys mean less memory per item, and for small items can move them to a more efficient slab class. Keys are effectively limited to 250 characters.

Tactics:
- Boil long names down (for example a function id you can grep for).
- Base64 encode long numbers.
- Meta protocol: base64 plus the `b` flag allows packed binary keys (see binary-keys-base64).
- The binary protocol can set arbitrary keys directly.

Gains: roughly 5-20% of memory, but often buying a few gigabytes of RAM is cheaper than the engineering time, so do it only if really hurting.

Verify the effect on slab classes with `stats slabs` (`chunk_size`, `used_chunks`) and `stats items` (`mem_requested`), and memory per item from the ./sizes utility.

## Checked

Confirmed 2026-11-09: 250-character key limit, shortening keys, base64 for long numbers, arbitrary binary keys in the binary protocol, the 5-20% figure and the buy-RAM-instead caveat (Use Cases page, Reducing key size); the `b` base64 key flag (protocol.txt and Meta page); `chunk_size` and `used_chunks` in stats slabs, `mem_requested` in stats items, and the ./sizes utility (protocol.txt, Performance page). Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Use Cases, Meta protocol and Performance pages and memcached doc/protocol.txt

---
id: computing-software.database-administration.memcached.binary-keys-base64
name: binary-keys-base64
category: computing-software
field: database-administration
product: memcached
tags: [base64, binary-keys, b-flag, utf8, key-size]
level: advanced
status: docs-checked
description: "Store binary or UTF-8 keys through the meta protocol with the b flag and base64, and why that can save RAM."
sources:
  - https://docs.memcached.org/protocols/meta/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

With the meta protocol you can store and retrieve non-ASCII keys (UTF-8 strings too): base64-encode the key and send the `b` flag.

```
ms 44OG44K544OI 2 b\r\nhi
mg 44OG44K544OI b v k    -> VA 2 k44OG44K544OI b
```
If you request `k`, the returned key is base64 and the `b` flag in the response tells the client the key is base64-encoded binary. `me` (meta debug) takes `b` too, and `ma` and `md` accept `b`. `lru_crawler mgdump` prints `mg <base64encodedkey> b` for keys in binary format.

Why: if keys are very long but data very short, a string identifier can be encoded into a small number, and IDs can be 32-bit or 64-bit integers, saving RAM on the servers.

Trade-off: base64 adds some overhead on the network portion, but is typically extremely fast to encode or decode on modern hardware. The protocol limits keys to 250 characters.

## Checked

2026-11-04. Confirmed against the Meta Text Protocol page ("Binary Encoded Keys") and protocol.txt (key limit, b flag on mg/ms/md/ma/me, mgdump). Removed: the closing `mg <key> b s` check line (not on the page) and the claim that the 250 limit applies to the base64 text as sent (the page does not say).

Method: documentation only; no commands were run.

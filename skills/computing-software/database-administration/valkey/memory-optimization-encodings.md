---
id: computing-software.database-administration.valkey.memory-optimization-encodings
name: memory-optimization-encodings
category: computing-software
field: database-administration
product: valkey
tags: [memory-optimization, listpack, intset, hash-max-listpack-entries, fragmentation, rss, bucketing]
level: practitioner
status: docs-checked
description: "Reduce Valkey memory: listpack and intset encodings with their max-entries settings, hash bucketing for key-value stores, and allocator fragmentation caveats."
sources:
  - https://valkey.io/topics/memory-optimization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Small encodings: hashes, lists, integer-only sets and sorted sets below size limits use compact encodings, up to 10 times less memory (about 5 times on average), transparently. Tune with these `valkey.conf` directives (defaults shown for 7.2):
```
hash-max-listpack-entries 512
hash-max-listpack-value 64
zset-max-listpack-entries 128
zset-max-listpack-value 64
set-max-intset-entries 512
set-max-listpack-entries 128
set-max-listpack-value 64
```
Values that overflow convert to normal encoding (fast when small); benchmark conversion time before raising limits a lot.

Other levers: a 32-bit build (`make 32bit`) uses less memory per key but caps at 4 GB, and RDB/AOF files are compatible with 64-bit. Bitmaps or `GETRANGE`/`SETRANGE` store a flag per user; 100 million users take about 12 MB. Prefer one hash per object over separate keys.

Bucketing trick: store small string-to-string data in hashes, splitting `object:1234` into key `object:12` and field `34`, giving about 100 fields per hash; short ids like `object:2` use key `object:` with field `2`. Small hashes are linear arrays (cache friendly) yet amortised O(1). Limits: no per-field TTL on this pattern (fields hold strings only), and once a hash exceeds the limits the saving is lost.

Allocator: Valkey often does not return freed memory to the OS, so RSS stays near peak (5 GB filled, 2 GB deleted leaves RSS near 5 GB). Provision for peak usage; freed chunks are reused, and the fragmentation ratio (RSS divided by used memory) misleads after a high peak. Without `maxmemory` Valkey can consume all RAM; consider `maxmemory-policy noeviction` so writes error instead.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/memory-optimization/ (page text read in full): Up to 10 times (5 average) saving, the seven 7.2 default directives, overflow conversion, make 32bit and 4 GB cap, RDB/AOF compatibility, 100 million users in 12 MB, hash advice, object:12 / field 34 bucketing with 100 fields, linear-array cache locality, no field TTL and strings only, RSS and fragmentation behaviour, maxmemory and noeviction advice.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.

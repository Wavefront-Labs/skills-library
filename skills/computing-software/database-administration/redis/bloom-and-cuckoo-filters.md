---
id: computing-software.database-administration.redis.bloom-and-cuckoo-filters
name: bloom-and-cuckoo-filters
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, bloom-filter, cuckoo-filter, probabilistic-data-structures, redis-bloom, redis-data-types]
level: practitioner
status: docs-checked
description: "Use Redis Bloom and cuckoo filters (BF.RESERVE/BF.ADD/BF.EXISTS, CF.*) for memory-cheap membership checks with a chosen false-positive rate, and size them correctly."
sources:
  - https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/
  - https://redis.io/docs/latest/develop/data-types/probabilistic/cuckoo-filter/
  - https://redis.io/docs/latest/commands/bf.reserve/
  - https://redis.io/docs/latest/commands/bf.add/
  - https://redis.io/docs/latest/commands/cf.reserve/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bloom and cuckoo filters

**Goal:** answer "have we seen this?" (username taken, URL crawled, coupon used) with a few bits per item; false positives possible, false negatives not. Built into Redis 8; RedisBloom module on older versions.

## Bloom filter
```text
BF.RESERVE seen:urls 0.001 10000000              # error rate 0.1%, capacity 10M
BF.ADD seen:urls https://example.com/a           # 1 if newly added
BF.EXISTS seen:urls https://example.com/a        # 1 = probably, 0 = definitely not
BF.MADD / BF.MEXISTS ...                          # batches
BF.INFO seen:urls                                 # filter details
```
- Sizing: bits per item = -ln(error) / ln(2)^2: about 9.6 bits at 1%, 14.4 at 0.1%, 19.2 at 0.01%; 10M items at 0.1% ≈ 18 MB.
- Exceeding capacity adds sub-filters (`EXPANSION`, default 2; use 2 or more when the item count is unknown). `NONSCALING` uses slightly less memory and errors when full instead. Reserve for the real expected count.
- No deletion in a Bloom filter (cuckoo filters support it).

## Cuckoo filter
```text
CF.RESERVE seen:coupons 1000000
CF.ADD seen:coupons C-123
CF.EXISTS seen:coupons C-123
CF.DEL seen:coupons C-123                          # deletion supported
```
Choose cuckoo when deletes are needed or lookups dominate; Bloom when inserts dominate. Adding the same item twice to a cuckoo filter creates two entries and fills the filter.

## Pattern: avoid DB lookups
Check the filter first: `0` means skip the database query entirely (e.g. "username available" path); `1` means confirm against the database.

## Persistence and backups
Check the Bloom filter documentation for how to copy a filter between servers.

## Gotchas
- `BF.ADD` on a missing key auto-creates a filter with default error rate, capacity and expansion (see BF.RESERVE for the values in your version): always `BF.RESERVE` first with the real capacity and error rate.

## Verify
Load a test set, then query N items known absent and measure the false-positive fraction against the configured rate.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed: BF.RESERVE syntax (`error_rate capacity [EXPANSION] [NONSCALING]`), EXPANSION default 2, NONSCALING behaviour; BF.ADD returns 1 or 0 and auto-creates with default settings; the bits-per-item formula and the 14.378 bits at 0.1% figure; cuckoo versus Bloom trade-offs and CF.RESERVE syntax; all previously modular functionality is built into Redis Open Source 8. Removed unconfirmed: default capacity and error values, BF.INFO field list, BF.SCANDUMP/LOADCHUNK persistence, deletion-of-absent-item warning, error-rate compounding.
Method: documentation only; no commands were run.

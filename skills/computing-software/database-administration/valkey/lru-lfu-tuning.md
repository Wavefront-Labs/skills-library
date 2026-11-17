---
id: computing-software.database-administration.valkey.lru-lfu-tuning
name: lru-lfu-tuning
category: computing-software
field: database-administration
product: valkey
tags: [lru, lfu, maxmemory-samples, lfu-log-factor, lfu-decay-time, morris-counter, eviction-tuning]
level: advanced
status: docs-checked
description: "Tune Valkey approximated LRU (maxmemory-samples 5 vs 10) and LFU (lfu-log-factor 10, lfu-decay-time 1) eviction with Morris counter behaviour."
sources:
  - https://valkey.io/topics/lru-cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
LRU approximation: Valkey does not find the true least-recently-used key, since exact LRU costs more memory. It samples a few keys per eviction, evicts the oldest-accessed among them, and keeps a pool of good candidates. Precision is tuned by `maxmemory-samples` (default 5). Five samples already does a reasonable job; 10 is very close to true LRU, at some extra CPU. Under power-law access the difference from true LRU was minimal in simulations. Try values live with `CONFIG SET maxmemory-samples <count>` and compare cache miss rate.

LFU mode: `allkeys-lfu` and `volatile-lfu` evict rarely used keys, which can give a better hit ratio. Frequency is estimated with a probabilistic Morris counter in a few bits per object (range 0-255), sampled like LRU, plus decay so old popularity fades. Defaults saturate near one million requests and decay every minute.
```
lfu-log-factor 10
lfu-decay-time 1
```
`lfu-decay-time` is minutes before a sampled counter decays; 0 never decays. `lfu-log-factor` sets hits needed to saturate: higher means more accesses to reach 255, lower gives better resolution at low counts. Counter values from the page table:
- factor 0: 104 after 100 hits, 255 after 1000.
- factor 1: 18 / 49 / 255 at 100 / 1000 / 100K hits.
- factor 10: 10 / 18 / 142 / 255 at 100 / 1000 / 100K / 1M hits.
- factor 100: 8 / 11 / 49 / 143 / 255 at 100 / 1000 / 100K / 1M / 10M hits.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/lru-cache/ (page text read in full): Approximated LRU sampling and candidate pool, maxmemory-samples 5 versus 10, CONFIG SET, LFU Morris counter, allkeys-lfu/volatile-lfu, defaults (~1 million, 1 minute), lfu-log-factor 10, lfu-decay-time 1, 0 means no decay, counter range 0-255, the counter table.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.

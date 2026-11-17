---
id: computing-software.database-administration.memcached.extstore-enable
name: extstore-enable
category: computing-software
field: database-administration
product: memcached
tags: [extstore, flash-storage, ext-path, ssd, 1-6-0]
level: practitioner
status: docs-checked
description: "Add flash storage with -o ext_path=/path/to/file:5G on memcached 1.6.0+, and decide whether extstore fits your workload."
sources:
  - https://docs.memcached.org/features/flashstorage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Extstore leaves the hash table and keys in memory and moves values to external storage (usually flash). It requires memcached 1.6.0 or newer and flash storage; it will not work with rotational media. With only one or two instances you probably do not need it. It fits if stored values are much larger than keys and your hit rate would improve by keeping data longer; it can save cost if you have spare network capacity.

Enable: your normal startup options (-m, -c, etc.) plus
```
-o ext_path=/path/to/a/datafile:5G
```
This initializes extstore with up to 5 gigabytes of storage, split internally into pages of 64 megabytes by default.

Signal to try it: in `stats` and `stats slabs`, slab classes with large `chunk_size` also have a relatively high `total_pages`, and you see evictions.

Cautions:
- The key and item structure plus 12 bytes for the flash location stay in RAM, so if your values are only 60 bytes you will not save much RAM, if any.
- Writing too much to memcached means writing too much to flash, which can burn out the drive or cause too much latency; most server-quality flash is rated to be overwritten only 1-5+ times per day.
- All data is tracked in memory, so a restart of memcached effectively empties flash.
- UDP is not supported for objects flushed to disk, and many features (incr/decr/append/prepend) are disabled for items sent to disk.
- You will not be able to store the full 5 gigabytes because of fragmentation; the page says to expect 80-90% best case.

Unless your servers are very busy, no further tuning is needed; monitor `stats` (including the `extstore_` stats) and how much is written to disk. Evictions can mean you are out of RAM or writing faster than extstore can keep up.

## Checked

2026-11-04. Confirmed against the Flash Storage page (quick start, when to use, tuning guide, rough notes). Removed: the unstated claim that extstore is incompatible with warm restart.

Method: documentation only; no commands were run.

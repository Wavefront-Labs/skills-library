---
id: computing-software.devops-ci-cd.forgejo.cache-adapter-recommendation
name: cache-adapter-recommendation
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [cache-adapter, twoqueue, redis-cache, valkey]
level: practitioner
status: docs-checked
description: "Pick the [cache] ADAPTER for your load: default, twoqueue for light use, redis or memcache for busy instances."
sources:
  - https://forgejo.org/docs/latest/admin/setup/recommendations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default cache is basic: entries expire after a fixed time-to-live regardless of use, with no eviction under memory pressure and no LRU. Forgejo caches things like commit counts for repositories or branches, file and commit history lookups, user settings and avatar hashes.

Recommendations by load:

- Low activity: set `[cache].ADAPTER = twoqueue`, a size-limited LRU cache that keeps frequently used items. The guide also suggests changing `[cache].HOST` to a value such as `{"size":100, "recent_ratio":0.25, "ghost_ratio":0.5}`, because the default keeps up to 50,000 items for 16 hours, which is not memory efficient.
- High activity: use `redis` or `memcache` so caching is outsourced to dedicated software, and adjust `[cache].HOST` to point at it.

The redis adapter supports software that implements a limited subset of the Redis Go client API. Forgejo runs integration tests against Redis v7.2 (higher versions are not officially supported because of licensing concerns), Redict (an LGPL fork of v7.2), Valkey (a fork of v7.2 stewarded by the Linux Foundation) and Garnet (an independent RESP implementation).

## Checked

2026-11-04. Confirmed against the Forgejo Recommended Settings and Tips page ([cache].ADAPTER section): basic adapter behaviour, the four caching examples, twoqueue and its HOST value, the 50,000 item and 16 hour defaults, redis or memcache for busy instances, and the tested Redis-compatible software. Nothing removed.

Method: documentation only; no commands were run.

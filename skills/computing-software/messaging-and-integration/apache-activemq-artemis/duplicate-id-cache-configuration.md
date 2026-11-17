---
id: computing-software.messaging-and-integration.apache-activemq-artemis.duplicate-id-cache-configuration
name: duplicate-id-cache-configuration
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,id-cache-size,persist-id-cache,duplicate-id-cache,use-duplicate-detection,activemq-artemis]
level: advanced
status: docs-checked
description: "Size and persist the duplicate ID cache with id-cache-size globally or per address and persist-id-cache; bridges and cluster connections add IDs automatically."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/duplicate-detection.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duplicate ID cache configuration

**Goal:** make the duplicate-detection cache big enough and durable enough for your resend window, without wasting heap.

## Size
Global, in `<core>` of `broker.xml`:
```xml
<id-cache-size>5000</id-cache-size>
```
Default `20000`; `0` disables caching. Per address, an `id-cache-size` in an `address-setting` takes precedence over the global value (default also `20000`, `0` disables). The cache is circular, so choose a size large enough that, when you resend, all previously sent IDs are still in the cache and not overwritten.

## Persistence
`persist-id-cache` (global only, not per address, default `true`) persists each ID as it is received so duplicates are still detected after a broker restart; the cost is performance. Setting it to `false` is in `<core>`:
```xml
<persist-id-cache>false</persist-id-cache>
```

## Bridges and cluster connections
Core bridges add a unique duplicate ID if the message has none when `use-duplicate-detection` is `true` (default `true`), so a resend after a crash or interruption is ignored by the target if already received. Cluster connections use core bridges internally and have the same `use-duplicate-detection` setting, default `true`.

## Performance
If you do not need duplicate detection at all, set the global `id-cache-size` to `0` so the server does not pre-allocate cache objects and heap remains available.

## Checked

Method: docs-checked 2026-11-09 against duplicate-detection.adoc (read in full). Removed the Verify step.

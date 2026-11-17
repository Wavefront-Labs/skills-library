---
id: computing-software.search-and-information-retrieval.apache-solr.cache-configuration-warming
name: cache-configuration-warming
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [caches-warming, caches, filtercache, autowarm, query-warming, caffeinecache]
level: advanced
status: docs-checked
description: "Size and warm Solr caches in solrconfig.xml: filterCache, queryResultCache, documentCache, CaffeineCache, autowarmCount, and warming listeners."
sources:
  - https://solr.apache.org/guide/solr/latest/configuration-guide/caches-warming.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache-configuration-warming

Caches belong to one Index Searcher and are cleared on commit; a new searcher auto-warms from the old one's cache while the old keeps serving.

`CaffeineCache` (W-TinyLFU eviction) is the modern implementation. Attributes: `size`, `initialSize`, `autowarmCount` (integer or percentage), `maxIdleTime` (seconds, 0 = never evict), `maxRamMB`, `async`, `enabled`.
- `maxRamMB` takes precedence over `size`. Do not use it on `documentCache`.
- `async` defaults on; it is required if queries include child documents or joins, and suits `filterCache`.

Caches:
- `filterCache`: bitsets for each `fq`, `filter()` and `facet.method=fc`.
- `queryResultCache`: ordered doc ids for a query, sort and range. Related elements: `queryResultWindowSize`, `queryResultMaxDocsCached`.
- `documentCache`: stored fields; size it above max results times max concurrent queries.

Other elements: `useColdSearcher`, `maxWarmingSearchers`.

Warming: `<listener event="firstSearcher">` fires at startup with no current searcher; `newSearcher` fires after commits, both with `solr.QuerySenderListener`. Replace the sample queries before production; the `firstSearcher` sample is active by default. Cache stats appear in the Admin UI Plugins & Stats screen.

## Checked

Checked 2026-11-09 against the full Caches and Query Warming page of the Solr Reference Guide: cache parameters, CaffeineCache, filterCache, queryResultCache, documentCache, useColdSearcher, maxWarmingSearchers and the listener events. Every claim matched.

Method: docs-checked 2026-11-09 against the Caches and Query Warming page (raw ref-guide source); no commands were run.

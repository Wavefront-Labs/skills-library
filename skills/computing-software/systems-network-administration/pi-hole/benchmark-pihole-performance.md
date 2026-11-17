---
id: computing-software.systems-network-administration.pi-hole.benchmark-pihole-performance
name: benchmark-pihole-performance
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-benchmark, dig-mass-query, cache-size-benchmark]
level: advanced
status: docs-checked
description: "Benchmark Pi-hole with your real query history: extract domains, disable logging, enlarge the cache and time dig -f."
sources: ["https://docs.pi-hole.net/guides/misc/benchmark/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Realistic benchmarking

Use your own long-term database for domains so the test reflects real usage.

**1. Extract domains**

```bash
sqlite3 /etc/pihole/pihole-FTL.db "SELECT domain FROM queries LIMIT 100000;" > domains.list
```

Start with a small number to get results in reasonable time. The list will contain frequent domains and some blocked ad domains.

**2. Prepare Pi-hole**

- Disable logging and the long-term database so the log and database do not grow by hundreds of megabytes and distort results:

```bash
pihole-FTL --config dns.queryLogging false
pihole-FTL --config database.maxDBdays 0
```

- Increase the cache, because the artificial rate gives domains no time to expire naturally. The guide suggests about 25,000, roughly one-eighth to one-fourth of the extracted domains:

```bash
pihole-FTL --config dns.cache.size 25000
```

**3. Run**

```bash
time dig -f domains.list +noall +answer > /dev/null
```

The elapsed time for the number of domains gives your throughput.

**4. Restore** the original `queryLogging`, `maxDBdays` and `cache.size` values afterwards. Note that the default cache size in the config reference is 10000.

**Checklist**

1. Record current settings first.
2. Benchmark.
3. Restore settings (the config reference gives `database.maxDBdays` default 91).

## Checked

2026-11-03. Read the Realistic benchmarking guide (sqlite3 extraction command and 100,000 limit, logging and database settings, the 25,000 cache suggestion and its one-eighth to one-fourth guess, the `time dig -f` command) and the FTL configuration reference (`dns.cache.size` default 10000, `database.maxDBdays` 0 disables, default 91).

Method: documentation only; no commands were run.

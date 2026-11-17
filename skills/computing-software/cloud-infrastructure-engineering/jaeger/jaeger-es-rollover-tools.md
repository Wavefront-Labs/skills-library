---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-es-rollover-tools
name: jaeger-es-rollover-tools
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, jaeger-es-rollover, jaeger-es-index-cleaner, rollover-conditions, lookback]
level: advanced
status: docs-checked
description: "Run jaeger-es-rollover init, rollover and lookback plus jaeger-es-index-cleaner to manage Elasticsearch indices manually."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: operate rollover without ILM.

Initialize (add `-e ARCHIVE=true` for archive storage):
`docker run -it --rm --net=host jaegertracing/jaeger-es-rollover:latest init http://localhost:9200`
For spans, services and dependencies it creates index templates, the first index (jaeger-span-000001) and read/write aliases (jaeger-span-read, jaeger-span-write). Then deploy Jaeger with `use_aliases: true`.

Roll over periodically (cron):
`docker run -it --rm --net=host -e CONDITIONS='{"max_age": "2d"}' jaegertracing/jaeger-es-rollover:latest rollover http://localhost:9200`
This rolls the write alias to a new index when the current one is older than 2 days and adds the new index to the read alias.

Optionally remove old indices from the read alias, mimicking `max_span_age` of daily indices:
`docker run -it --rm --net=host -e UNIT=days -e UNIT_COUNT=7 jaegertracing/jaeger-es-rollover:latest lookback http://localhost:9200`

Delete old data with the cleaner, also used for daily indices:
`docker run -it --rm --net=host -e ROLLOVER=true jaegertracing/jaeger-es-index-cleaner:latest 14 http://localhost:9200`
This removes indices older than 14 days. The tools are also available as standalone binaries on the Jaeger GitHub releases page.

## Checked

2026-11-03. Confirmed against the Elasticsearch page, Index Rollover section: init (templates, first index, read and write aliases, ARCHIVE=true), rollover with CONDITIONS, lookback with UNIT and UNIT_COUNT, index cleaner with ROLLOVER=true and a day count, and the standalone binaries note. Nothing removed.
Method: documentation only; no commands were run.

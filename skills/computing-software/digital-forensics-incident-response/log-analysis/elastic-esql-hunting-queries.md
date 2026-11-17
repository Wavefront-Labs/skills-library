---
id: computing-software.digital-forensics-incident-response.log-analysis.elastic-esql-hunting-queries
name: elastic-esql-hunting-queries
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [esql, elastic-security, threat-hunting, ecs, siem-query, dfir]
level: practitioner
status: gated
description: "Hunt in Elastic with ES|QL: piped FROM/WHERE/STATS/EVAL syntax over ECS fields, stacking and rarity queries, ENRICH lookups, time bucketing and limits versus KQL/EQL."
sources: ["https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html", "https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-commands.html", "https://www.elastic.co/guide/en/security/current/rules-ui-create.html", "https://www.elastic.co/guide/en/ecs/current/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic ES|QL hunting queries

ES|QL (Elasticsearch Query Language, GA in 8.14) is a piped language that aggregates and transforms at query time, which suits hunting (stacking, rarity, ratios) better than KQL filters. Elastic Security also supports ES|QL detection rules.

## Shape
```esql
FROM logs-endpoint.events.process-*
| WHERE @timestamp > NOW() - 7 days AND event.type == "start"
| WHERE process.parent.name IN ("winword.exe", "excel.exe", "outlook.exe")
| STATS hosts = COUNT_DISTINCT(host.name), runs = COUNT(*) BY process.name, process.parent.name
| SORT runs DESC
| LIMIT 50
```
Commands: `FROM`, `WHERE`, `EVAL` (computed fields), `STATS ... BY`, `KEEP`/`DROP`, `RENAME`, `SORT`, `LIMIT`, `DISSECT`/`GROK` (parse strings), `ENRICH` (lookup policy), `MV_EXPAND`, `LOOKUP JOIN` (newer versions).

## Hunting recipes
Rare processes by host count (stacking):
```esql
FROM logs-endpoint.events.process-*
| WHERE event.type == "start" AND @timestamp > NOW() - 30 days
| STATS host_count = COUNT_DISTINCT(host.name) BY process.executable
| WHERE host_count <= 2
| SORT host_count ASC
```
Beacon-like regularity per destination:
```esql
FROM logs-network_traffic.*
| WHERE source.ip == "10.1.2.3"
| EVAL bucket = DATE_TRUNC(1 minute, @timestamp)
| STATS conns = COUNT(*) BY destination.ip, bucket
| STATS minutes_active = COUNT(*), avg_per_min = AVG(conns) BY destination.ip
| SORT minutes_active DESC
```
Parsing a command line:
```esql
FROM logs-*
| WHERE process.name == "powershell.exe"
| EVAL cmd_len = LENGTH(process.command_line)
| WHERE cmd_len > 1000 OR process.command_line LIKE "*-enc*"
| KEEP @timestamp, host.name, user.name, process.command_line
```

## When to use what
- **ES|QL**: aggregation, rarity, computed fields, ad-hoc pivots.
- **EQL**: sequences (`sequence by host.id [process where ...] [network where ...]`), ideal for ordered behaviours.
- **KQL/Lucene**: quick filters in Discover and dashboards.

## Gotchas
- Default result limit (1,000 rows unless `LIMIT` changed, with a server maximum) silently truncates; always set `LIMIT` and know the cap.
- Field types must match: keyword vs text; use `.keyword` or ECS keyword fields for exact matching and grouping.
- Large time ranges over many indices are expensive; narrow `FROM` index patterns and filter time first.

## Verify
A hunt result is reproduced by an independent query (EQL or Discover filter) for at least one hit, and the query is saved with its time range in the hunt record.

## Checked

- Date: 2026-11-02.
- Confirmed against: only the existence of ES|QL and Elastic Security rules; the Elastic reference pages were stubs.
- Not confirmed: all ES|QL command names and syntax (LOOKUP JOIN, MV_EXPAND, GROK, COUNT_DISTINCT, DATE_TRUNC) and ECS field names (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.

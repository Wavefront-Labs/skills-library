---
id: computing-software.messaging-and-integration.temporal.custom-search-attributes
name: custom-search-attributes
category: computing-software
field: messaging-and-integration
product: temporal
tags: [search-attributes, custom-search-attribute, keyword, keywordlist, text, limits, visibility]
level: practitioner
status: docs-checked
description: "Temporal custom Search Attributes: supported types, Keyword versus KeywordList versus Text, per-store limits, size limits, and why no PII belongs in them."
sources:
  - https://docs.temporal.io/search-attribute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Search Attribute is an indexed key-value field in a workflow's Visibility info, used in List Filters. Never put secrets or PII in names or values: values are stored unencrypted, are not passed through a Payload Codec (the Server must read them to filter), and names show in Namespace config, queries and the UI.

Keys carry over on Continue-As-New and Cron runs. Values live only as long as the workflow. For business logic, expose state via a Query or an external datastore written by Activities rather than Search Attributes.

Custom attributes require advanced Visibility: Elasticsearch, or with Server v1.20+ MySQL 8.0.17+, PostgreSQL 12+, SQLite 3.31.0+ (not Cassandra). On Elasticsearch they are global across Namespaces; on SQL they are per Namespace.

Types: Bool, Datetime, Double (`scaled_float`, 4 decimal digits), Int (64-bit), Keyword, KeywordList, Text. Since v1.20 Keyword holds one value; use KeywordList for lists. Storing lists in other types is deprecated; Cloud Namespaces must migrate before Sep. 30, 2026.

String choice: Keyword for exact structured values (supports `=`, `!=`, `IN`, `STARTS_WITH`, `BETWEEN`, `ORDER BY`), the default; KeywordList for tags (`=`, `!=`, `IN`); Text only for prose with word-level OR matching, and not in ORDER BY.

Per-Namespace limits (MySQL, PostgreSQL, SQLite / Cloud): Bool, Datetime, Double, Int 3 / 20 each; Keyword 10 / 40; KeywordList 3 / 5; Text 3 / 5. Elasticsearch has no Temporal limit, only its mapping limit. Value size 2 KB, total size 40 KB, at most 255 characters per value.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: search-attribute (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.

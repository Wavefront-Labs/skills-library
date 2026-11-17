---
id: computing-software.messaging-and-integration.temporal.list-filter-syntax
name: list-filter-syntax
category: computing-software
field: messaging-and-integration
product: temporal
tags: [list-filter, visibility-query, starts-with, keyword, text-search, search-attribute-alias, count-workflow]
level: practitioner
status: docs-checked
description: "Temporal List Filter syntax: operators, Text versus Keyword matching, STARTS_WITH and BETWEEN prefix tricks, ordering, pagination, and search attribute aliasing."
sources:
  - https://docs.temporal.io/list-filter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A List Filter is an SQL-like string for the Visibility List API, scoped to one Namespace. Attribute names are case sensitive. Time ranges resolve to 1 ns on Elasticsearch and 1 microsecond on SQL stores.

Operators: `=, !=, >, >=, <, <=`, `AND, OR, ( )`, `BETWEEN ... AND`, `IN (a, b)`, `STARTS_WITH` (Keyword only), `IS NULL`, `IS NOT NULL`. Literals: quoted strings, numbers, booleans. Wrap names with characters outside `[a-zA-Z0-9]` in backticks. `ORDER BY` is not supported on Cloud (default order `ClosedTime DESC NULL FIRST`, `StartTime DESC`), and not for Text attributes.

Text attributes use the Elasticsearch standard analyzer: lowercased tokens split at most punctuation (`order-processing-v2` gives `order`, `processing`, `v2`); underscores, dots, colons and apostrophes between two letters or two digits do not split. `=` matches if any query token matches any indexed token (OR), so `Description = 'foobar'` matches `my-business-id-foobar`, but `'foo'` does not. For exact identifiers use Keyword.

Keyword prefixes: `WorkflowId STARTS_WITH "order-"`, or `WorkflowId BETWEEN "order-" AND "order-~"` (misses values with `~` right after the prefix).

Example: `WorkflowType = "main.YourWorkflowDefinition" and ExecutionStatus != "Running" and (StartTime > "2021-06-07T16:46:34.236-08:00" or CloseTime > "2021-06-07T16:46:34-08:00")`.

Over 10,000 results is slow: use Count (v1.20+) or paginate with the page token until it is null. Standalone Activities use the same syntax via `ListActivities`, `temporal activity list` and `temporal activity count`.

Aliasing (Server 1.30+): default attributes carry a `Temporal` prefix; the unprefixed alias works too, but a custom attribute with that name wins, and the prefixed name still reaches the default.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: list-filter (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.

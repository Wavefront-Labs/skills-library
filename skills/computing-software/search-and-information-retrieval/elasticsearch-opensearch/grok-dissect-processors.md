---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.grok-dissect-processors
name: grok-dissect-processors
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, grok-dissect-processors]
level: advanced
status: docs-checked
description: "Extract fields from log lines using the grok and dissect processors and choose between them by speed and flexibility."
sources:
  - https://www.elastic.co/docs/reference/enrich-processor/grok-processor
  - https://www.elastic.co/docs/reference/enrich-processor/dissect-processor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parse text with grok and dissect

**Goal:** structured fields from unstructured messages.
- Dissect: `{"dissect":{"field":"message","pattern":"%{ts} %{level} %{msg}"}}` no regex, can be faster than grok in some cases; matching is strict (every pattern character must match, every key needs a value).
- Grok: `{"grok":{"field":"message","patterns":["%{IP:client} %{WORD:verb} %{URIPATHPARAM:path}"]}}` regex based; `patterns` is an ordered list and the first match wins.
- Both take `ignore_missing` (default false), `ignore_failure` and `on_failure`; use `on_failure` to tag unparsable lines.
- Dissect extra whitespace breaks a match unless the right padding modifier `->` is used; `%{}` and `%{?name}` skip text; `+` appends (joined by `append_separator`); all values are strings, so use the convert processor for types.
- Grok extras: `pattern_definitions` for custom patterns, `trace_match` stores the matching pattern index in `_ingest._grok_match_index`, `ecs_compatibility: v1` for ECS names.
- A dissect pattern with a key lacking a value throws an exception, handled by `on_failure` or suppressed by `ignore_failure`.
- Grok has a watchdog that interrupts slow evaluations and fails the processor; the limit is `ingest.grok.watchdog.max_execution_time` (default 1s).
- Test with the simulate API (processor wrapped in a `pipeline` object, samples in `docs`) using real log lines, including a non-matching one.
- Failure mode: greedy or ambiguous grok patterns run slowly; prefer dissect when the format is stable.

## Verify
- [ ] Simulate returns all expected fields for 3 representative lines.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch grok and dissect processor pages in full; OpenSearch was not checked.

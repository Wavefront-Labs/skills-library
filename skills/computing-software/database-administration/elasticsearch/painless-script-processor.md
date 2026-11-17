---
id: computing-software.database-administration.elasticsearch.painless-script-processor
name: painless-script-processor
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, painless-script, script-processor, ingest-pipelines, painless, elasticsearch-ingest]
level: practitioner
status: verified
description: "Transform documents at ingest with the Elasticsearch script processor in Painless, using stored scripts and params, with null safety, performance and debugging tips."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/script-processor.html
  - https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-ingest-processor-context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Painless script processor

**Goal:** logic the built-in processors cannot express (conditional field maths, list manipulation), without an external ETL step.

## Inline
```json
PUT _ingest/pipeline/orders
{ "processors": [ { "script": { "tag": "compute-totals", "lang": "painless",
  "source": """
    def items = ctx.items;
    if (items == null) { return; }
    double total = 0;
    for (def it : items) { total += (it.qty ?: 0) * (it.price ?: 0.0); }
    ctx.order_total = Math.round(total * 100) / 100.0;
    ctx.item_count = items.size();
  """ } } ] }
```
`ctx` is the document source (plus `ctx._index`, `ctx._id`, both read back correctly in `_simulate`). The triple-quoted `"""` form above is console notation; in a raw JSON body put the script on one line or escape newlines as `\n`.

## Stored script + params
```json
PUT _scripts/mask-email
{ "script": { "lang": "painless",
  "source": "if (ctx.user?.email != null) { def e = ctx.user.email; int at = e.indexOf('@'); ctx.user.email = e.substring(0, 1) + params.mask + e.substring(at); }" } }

{ "script": { "id": "mask-email", "params": { "mask": "***" } } }
```
Params keep the script text constant so it compiles once (compiles are cached and rate limited).

## Rules
- Null-safe access (`?.`, `?:`) everywhere; a null pointer fails the document.
- Prefer built-in processors (`set`, `rename`, `convert`, `split`, `foreach`, `dissect`) for simple cases: faster and declarative.
- Regex in Painless is controlled by `script.painless.regex.enabled`, default `limited` (a `=~` match worked at the default, bounded by `script.painless.regex.limit-factor`, default 6); `true` removes the limit, `false` disables regex. Prefer `grok`/`dissect` processors.
- No access to other documents or external lookups; use `enrich` for that.

## Debug
`_simulate?verbose=true` with sample docs; `Debug.explain(ctx.items)` throws an exception showing the object type and value.

## Verify
Ingest stats for the pipeline show the script processor's `time_in_millis` per document is reasonable (sub-millisecond typical); no `failed` count growth.

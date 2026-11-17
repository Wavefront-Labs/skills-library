---
id: computing-software.search-and-information-retrieval.typesense.natural-language-search-troubleshooting
name: natural-language-search-troubleshooting
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [nl-query-debug, prompt-cache, nl-fallback, typesense]
level: advanced
status: docs-checked
description: "Debug Typesense natural language search with nl_query_debug, the LLM failure fallback, and nl_query_prompt_cache_ttl and first-request latency."
sources: ["https://typesense.org/docs/30.2/api/natural-language-search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting natural language search

## Failure fallback

If LLM processing fails (API error, timeout), Typesense (1) uses the original natural language text as `q` when no `q` was given, (2) still applies explicit parameters such as `filter_by` and `sort_by`, and (3) adds an `error` field to the response.

## Debug mode

Add `nl_query_debug=true` in development. `parsed_nl_query` then includes `llm_response` with the raw `content`, the `extraction_method` (such as `regex`) and the `model`, alongside `generated_params` and `augmented_params`.

Tune behaviour with custom `system_prompt` text on the model, to give domain terminology or per-collection hints.

## Schema prompt cache

Typesense caches the prompt built from your collection schema. Control it per request with `nl_query_prompt_cache_ttl` (seconds); default 86400 (24 hours); `0` disables the cache temporarily. For large datasets the first request is slow, potentially several seconds, because building the prompt runs a series of `facet_by` queries; later requests reuse the cache.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Natural Language Search (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.

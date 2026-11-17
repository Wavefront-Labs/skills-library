---
id: computing-software.search-and-information-retrieval.typesense.natural-language-search-queries
name: natural-language-search-queries
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [nl-query, parsed-nl-query, nl-model-id, typesense]
level: advanced
status: docs-checked
description: "Run Typesense natural language searches with nl_query and nl_model_id, how LLM filters merge with filter_by via AND, and parsed_nl_query."
sources: ["https://typesense.org/docs/30.2/api/natural-language-search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Natural language search queries

## Single search

`GET /collections/products/documents/search` with `q=show me red shirts under 50`, `nl_query=true`, `query_by=name,description,color,category`, `nl_model_id=gemini-model` (use `--data-urlencode` with curl `-G`).

An explicit `filter_by=in_stock:true` is combined with the generated `color:red && category:shirt && price:<50` using AND, giving `in_stock:true && color:red && category:shirt && price:<50`.

## Multi search

Each search in `/multi_search` can carry its own `q`, `nl_query: true`, `query_by` and `nl_model_id`.

## Response

Besides hits there is `parsed_nl_query`: `parse_time_ms`, `generated_params` (only what the LLM produced: `q`, `filter_by`, `sort_by`) and `augmented_params` (final parameters after merging explicit ones). `request_params` echoes the input. Hide it with `exclude_fields=parsed_nl_query`.

## Examples of generated parameters

"Find red shirts under $30" gives `filter_by: color:Red && category:Apparel && price:<30`. "Show me available footwear sorted by price" gives `category:Footwear && in_stock:true` with `sort_by: price:asc`. "highest rated apparel" gives `category:Apparel` and `rating:desc`.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Natural Language Search (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.

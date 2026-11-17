---
id: computing-software.search-and-information-retrieval.meilisearch.custom-ranking-rules
name: custom-ranking-rules
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [custom-ranking-rules, asc-desc, business-ranking, meilisearch]
level: practitioner
status: docs-checked
description: "Add attribute:asc or attribute:desc custom ranking rules in Meilisearch, place them after built-in rules, and contrast them with sort."
sources:
  - https://www.meilisearch.com/docs/capabilities/full_text_search/relevancy/custom_ranking_rules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom ranking rules

A custom ranking rule is written as `attribute_name:asc` or `attribute_name:desc` and appended to the `rankingRules` list through the update-settings or update-rankingrules endpoint.

## Requirements

- The attribute must hold a numeric or string value in every document. If some documents lack it, the outcome is undefined and results may be ordered unexpectedly.
- Ordering is lexicographical: in a descending sort `Elena` ranks above `Ryu` and below `11`.

## Placement

Custom rules ignore relevancy, so they normally belong after the built-in rules; they then only break ties among equally relevant documents. A high position makes users see alphanumeric order instead of relevance.

Example list with custom rules at the bottom: words, typo, proximity, attributeRank, sort, wordPosition, exactness, `release_date:asc`, `movie_ranking:desc`. `release_date:asc` puts a 1999 film ahead of a 2020 one; `movie_ranking:desc` puts higher-ranked movies first.

## Custom rules versus sort

`sort` is for letting users choose an order, such as price ascending or descending in a shop. Custom rules are always active, suiting promotion, for example keeping discounted products near the top. Meilisearch has no native pinning or boosting of specific documents in this feature.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged except the shortened description.

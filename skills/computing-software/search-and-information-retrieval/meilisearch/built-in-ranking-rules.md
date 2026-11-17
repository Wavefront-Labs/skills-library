---
id: computing-software.search-and-information-retrieval.meilisearch.built-in-ranking-rules
name: built-in-ranking-rules
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [ranking-rules, bucket-sort, attribute-rank, meilisearch]
level: advanced
status: docs-checked
description: "Understand Meilisearch built-in ranking rules (words, typo, proximity, attributeRank, sort, wordPosition, exactness) and their order."
sources:
  - https://www.meilisearch.com/docs/capabilities/full_text_search/relevancy/ranking_rules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in ranking rules

The default order has seven rules: `words`, `typo`, `proximity`, `attributeRank`, `sort`, `wordPosition`, `exactness`. Change it with the update-settings or update-rankingrules endpoint.

## What each rule does

- `words`: more matched query terms first. Meilisearch always behaves as if `words` were present at higher priority than the attribute, exactness, typo and proximity rules, even if removed. It works from right to left, so term order in the query matters.
- `typo`: fewer typos first.
- `proximity`: matched terms closer together and in query order first. Its precision can be lowered through the proximityPrecision setting, which may significantly improve indexing speed at a possible cost to multi-term relevancy.
- `attributeRank`: matches in more important attributes first (per the attribute ranking order).
- `sort`: ordering from the query-time `sort` parameter; ignored when the request has no valid `sort`.
- `wordPosition`: matches nearer the start of an attribute first.
- `exactness`: terms identical to the query first.

An older `attribute` rule equals `attributeRank` plus `wordPosition`; it cannot be combined with either, or Meilisearch errors. Prefer the two separate rules.

## Ordering advice

Rules apply as a bucket sort: once a rule separates two documents, later rules cannot reorder them. Keep broad rules (words, typo, proximity) first, then fine-tuning rules (attributeRank, wordPosition, exactness). Place `sort` after the broad group and before the fine-tuning group; if sorting seems to have no effect, move it up one position at a time. Put custom rules last as tiebreakers. Recommended order: words, typo, proximity, sort, attributeRank, wordPosition, exactness, popularity:desc.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged except the shortened description.

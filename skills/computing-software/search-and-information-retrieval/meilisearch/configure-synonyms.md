---
id: computing-software.search-and-information-retrieval.meilisearch.configure-synonyms
name: configure-synonyms
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [synonyms, one-way-synonyms, multi-word-synonyms, meilisearch]
level: practitioner
status: docs-checked
description: "Define Meilisearch one-way or mutual synonyms; normalization, exact-match precedence, the 1-3 word term limit and 50 synonym cap."
sources:
  - https://www.meilisearch.com/docs/capabilities/full_text_search/relevancy/synonyms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure synonyms

Synonyms are set through the update-synonyms settings endpoint as an object mapping a term to an array of equivalents.

## One-way and mutual

- One-way: `{"phone": ["iphone"]}` treats documents with `iphone` as matching `phone`. Searching `iphone` also finds `phone` documents, but ranked lower due to the typo rule.
- Mutual: list every word against all the others, for example shoe, boot, slipper and sneakers each mapping to the other three. Any one of them then finds all.

## Rules

- Normalization: synonyms are processed with the index settings (stop words, separator and non-separator tokens). Do not let a synonym be a separator token such as `&`, or it is ignored. Case and accents are ignored, so `CV` and `Résumé` match `resume`.
- The exact query always wins over its synonyms because the `exactness` rule prefers exact words. With `ghost` as a synonym of `spirit`, searching `spirit` ranks the document containing "Spirit" first.
- Multi-word synonyms behave as phrases: `san francisco` and `sf` as a mutual pair.
- Synonyms are only fetched for search terms of 1 to 3 words. Setting "lord of the rings" as synonym of "lotr" works when searching `lotr`, but not when searching the four-word phrase.
- Up to 50 synonyms per term; extras are silently ignored. Multi-word synonyms of one term may total at most 100 words, again silently truncated.

Result counts can change by more than the pair itself because of typos and query splitting.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged except the shortened description.

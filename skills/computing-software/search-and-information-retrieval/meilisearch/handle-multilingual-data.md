---
id: computing-software.search-and-information-retrieval.meilisearch.handle-multilingual-data
name: handle-multilingual-data
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [multilingual, localized-attributes, query-locales, meilisearch]
level: advanced
status: docs-checked
description: "Index multilingual data in Meilisearch: per-language indexes versus one index, localizedAttributes for documents, locales on queries, and language detection."
sources: ["https://www.meilisearch.com/docs/capabilities/indexing/how_to/handle_multilingual_data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling multilingual datasets

## Index layout

Recommended: one index per language. It shards data naturally, allows per-language settings (stop words, separators), and eases languages needing specialized tokenizers such as Chinese or Japanese. To search several languages at once, use multi-search or federated search across the indexes.

A single index is acceptable for proofs of concept or under roughly 1M documents, when languages are space-separated and tokenize alike (English, French, Italian, Spanish, Portuguese). Languages with compounds (German), meaning-changing diacritics (Swedish) or no spaces (Chinese, Japanese) are better isolated. Do not mix Chinese and Japanese in one field; separate fields such as `title_zh` and `title_ja` are okay.

For the single-index approach, use language-suffixed or prefixed fields (`title_fr`, `title_en`) and declare them in the `localizedAttributes` setting so each gets the right tokenizer.

## Detection and alignment

Meilisearch detects language automatically, reliably for long texts but weakly for short snippets and type-as-you-search queries. Declaring `localizedAttributes` for documents and `locales` for queries restricts detection to the languages you name, making it more consistent. Queries and documents must be tokenized the same way, otherwise valid terms fail to match.

Query example: `client.index('INDEX_NAME').search('schiff', { locales: ['deu'] })`. If `locales` and `localizedAttributes` disagree, the query's `locales` wins for that request, so a wrong value overrides your index tuning.

## Checked

Method: docs-checked 2026-11-09 against the Handling multilingual datasets page (raw mdx of github.com/meilisearch/documentation, read in full). All claims confirmed.

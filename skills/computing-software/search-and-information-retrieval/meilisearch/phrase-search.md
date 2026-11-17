---
id: computing-software.search-and-information-retrieval.meilisearch.phrase-search
name: phrase-search
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [phrase-search, double-quotes, exact-phrase, meilisearch]
level: intro
status: docs-checked
description: "Wrap words in double quotes so Meilisearch requires them adjacent and in order, and know how phrases interact with matchingStrategy."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/getting_started/phrase_search"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phrase search in Meilisearch

Putting part or all of the `q` value in double quotes makes Meilisearch treat the quoted words as one unit: they must appear consecutively and in the given order. The query `"african american" horror` has one phrase plus one ordinary term, so a document must hold "african american" side by side and also contain "horror". A document with the two words apart does not satisfy the phrase.

In JSON the quotes must be escaped, for example `"q": "\"star wars\" \"empire strikes\""`. Several phrases can appear in one query, and each must match as an exact sequence.

## Interaction with matchingStrategy

A quoted phrase is always required. The strategy only affects the unquoted terms. For `"science fiction" adventure comedy`:

- `last` (the default): the phrase is required, while "adventure" and "comedy" follow normal behaviour where the least important terms may be dropped.
- `all`: the phrase and both extra terms must be present.

## When to use it

Known titles or names such as "The Lord of the Rings", technical terms such as "machine learning", and quoted expressions where adjacency matters.

## Checked

Method: docs-checked 2026-11-09 against the Meilisearch documentation source for Phrase search (capabilities/full_text_search/getting_started/phrase_search.mdx), read in full. Removed the unconfirmed stop-words note, which comes from a page not read.

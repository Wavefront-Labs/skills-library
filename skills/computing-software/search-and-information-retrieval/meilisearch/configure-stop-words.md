---
id: computing-software.search-and-information-retrieval.meilisearch.configure-stop-words
name: configure-stop-words
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [stop-words, common-terms, language-indexes, meilisearch]
level: practitioner
status: docs-checked
description: "Configure Meilisearch stopWords per index: case sensitivity, reindexing, per-language indexes and the effect on phrase search."
sources:
  - https://www.meilisearch.com/docs/capabilities/full_text_search/how_to/configure_stop_words
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure stop words

Stop words are very common terms ("the", "is", "at", "of") that Meilisearch ignores while indexing and searching. Removing them keeps them from diluting relevancy for words like "lord" and "rings" in `the lord of the rings`, and reduces comparisons per query.

## Settings operations

The default is an empty array, meaning none. You get, update or reset the stop words list through the index settings endpoints; a reset returns to treating all words as meaningful. The docs offer a starting English list: a, an, and, are, as, at, be, but, by, for, if, in, into, is, it, no, not, of, on, or, such, that, the, their, then, there, these, they, this, to, was, will, with.

## Rules to remember

- Stop words are per index.
- They are case-sensitive: "the" is not "The".
- They are removed from the index, so changing them re-indexes all documents asynchronously (follow the task).
- For multilingual data use one index per language with its own list, since "die" is a stop word in German but a real English word.
- They are ignored inside phrase searches, so `"the great gatsby"` matches like `"great gatsby"`.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged except the shortened description.

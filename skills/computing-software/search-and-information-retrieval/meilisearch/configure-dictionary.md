---
id: computing-software.search-and-information-retrieval.meilisearch.configure-dictionary
name: configure-dictionary
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [dictionary, custom-tokens, tokenizer, meilisearch]
level: practitioner
status: docs-checked
description: "Use the Meilisearch dictionary setting to keep terms like J. R. R. as single tokens, and tell it apart from synonyms and stop words."
sources:
  - https://www.meilisearch.com/docs/capabilities/full_text_search/how_to/configure_dictionary
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure a custom dictionary

The `dictionary` setting lists user-defined terms that Meilisearch treats as indivisible tokens during indexing and search, overriding the default tokenizer.

## When

- Domain words, or languages without whitespace such as Japanese, where uninterrupted sequences should not be fragmented.
- Names or abbreviations with dots and spaces, such as `J. R. R. Tolkien` or `W. E. B. Du Bois`, which the default tokenizer splits into letters and periods.

## Operations

Get the current value (empty array `[]` by default), update it (adding `J. R. R.` and `W. E. B.` makes a query for `J. R. R. Tolkien` match the exact spelling), or reset to restore default tokenization.

Updating triggers reindexing of all documents. This is asynchronous, so watch the task API.

## Versus other settings

- `synonyms` map different words to one concept (NYC to New York City).
- `stopWords` ignore common terms that add no signal.
- `dictionary` preserves sequences the tokenizer would split.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged except the shortened description.

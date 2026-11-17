---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.highlight-unified-fragments
name: highlight-unified-fragments
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, highlight-unified-fragments, es-highlighting]
level: practitioner
status: docs-checked
description: "Return snippets with highlight, pre_tags, fragment_size, number_of_fragments and require_field_match."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/highlighting
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/highlighting-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Highlighting with the unified highlighter

**Goal:** show matched terms in context.
```
{"query":{"match":{"body":"fox"}},"highlight":{"fields":{"body":{"fragment_size":150,"number_of_fragments":2}},"pre_tags":["<em>"],"post_tags":["</em>"]}}
```
- `type` defaults to `unified` (others `plain`, `fvh`). Unified splits text into sentences, scores them with BM25, and handles phrase and multi-term queries.
- Defaults: `fragment_size` 100 characters, `number_of_fragments` 5 (0 returns the whole field and ignores `fragment_size`), `pre_tags`/`post_tags` `<em>`/`</em>`, `require_field_match` true (false highlights all fields), `order` none (`score` puts best fragments first).
- Unified uses stored offsets when `index_options` is `offsets` (postings) or `term_vector` is `with_positions_offsets`; term vectors are faster for large fields (over 1 MB) and multi-term queries. Otherwise it re-analyzes text, which can be costly.
- Plain highlighting analyzes at most 1,000,000 characters by default (`index.highlight.max_analyzed_offset`).
- Set `encoder: html` to escape the snippet text before the tags are added; still treat snippets as untrusted before rendering in a page.
- If the field is not stored, Elasticsearch extracts it from `_source`.
- Highlighters do not follow boolean logic, so with nested booleans or `minimum_should_match` some highlighted text may not correspond to real matches.

## Verify
- [ ] Snippets contain the matched term inside the tags and no raw HTML from content.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch highlighting and highlighting settings pages in full; OpenSearch was not checked.

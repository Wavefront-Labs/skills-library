---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.text-vs-keyword-fields
name: text-vs-keyword-fields
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, text-vs-keyword-fields]
level: practitioner
status: docs-checked
description: "Decide between text, keyword, wildcard and constant_keyword fields in Elasticsearch for full-text search, exact match, sorting and aggregations."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/text
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/keyword
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/ignore-above
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose text versus keyword (Elasticsearch)

**Goal:** pick the type that matches how the field is queried.
- `text`: analyzed into terms for full-text search; human-readable content such as an email body or product description. Not used for sorting, seldom for aggregations. Default analyzer is `standard`.
- `keyword`: structured content (IDs, emails, hostnames, status codes, zip codes, tags). Used for sorting, aggregations and term-level queries like `term`. The keyword page advises against keyword fields for full-text search.
- Need both: a multi-field, for example `"my_field":{"type":"text","fields":{"keyword":{"type":"keyword"}}}`; search `my_field`, aggregate and sort on `my_field.keyword`.
- Numeric identifiers (ISBN, product ID) never range-queried: consider `keyword`, since `term` on keyword is often faster than on numeric. A multi-field can map both.
- `ignore_above` (character count): longer strings are not indexed, but stay in `_source`. Standard indices default to 2147483647, and a keyword over 32766 UTF-8 bytes rejects the document. logsdb defaults to 8191. For safety with non-ASCII text set 8191 or less. Dynamic mapping makes text with a `.keyword` sub-field at `ignore_above` 256, so longer values have no `.keyword` value and cannot be matched exactly.
- `wildcard`: machine-generated content searched grep-style with wildcard or regexp queries. Page criteria: over a million unique values with leading-wildcard patterns, or values over 32KB with any wildcard pattern. Otherwise keyword is faster, indexes faster and costs less. No phrase queries; scoring is constant.
- `constant_keyword`: every document in the index has the same value. With no `value` in the mapping, the first document sets it; one bad document can then cause the others to be rejected. The value cannot change once set.
- Failure mode: sorting, aggregating or scripting on `text` throws an exception because fielddata is off by default. `fielddata: true` loads tokens into heap and can cause latency spikes and cluster performance problems; the page says it usually makes no sense, so use the keyword multi-field.
- Failure mode (not stated on these pages; a judgment): a `term` query on a text field misses because the stored tokens are analyzed.
- OpenSearch: not checked; its text and keyword pages were unreadable.

## Verify
- [ ] `POST my-index/_analyze` with the field shows the tokens your `term` queries must use.

## Checked
Checked 2026-11-08 against the Elasticsearch text, keyword (family) and ignore_above pages. Only Elasticsearch was checked. Removed: the `fielddata` circuit-breaker claim (pages mention heap and latency, not the breaker).
Method: documentation only; no commands were run.

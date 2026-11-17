---
id: computing-software.search-and-information-retrieval.typesense.curation-tags
name: curation-tags
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [curation-tags, rule-tags, stop-processing, typesense]
level: practitioner
status: docs-checked
description: "Trigger Typesense curation items by name with rule.tags and the curation_tags search parameter, including how tagged and untagged items are ordered and processed."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tagging curation items

Add `tags` to a rule: `"rule": {"query": "iphone pro", "match": "exact", "tags": ["apple", "iphone"]}`, plus `includes` and `excludes` as usual. Then trigger the matching rules directly from a search with `"curation_tags": "apple,iphone"`.

## Selection logic

Suppose `item1` is tagged `tagA,tagB`, `item2` is tagged `tagA`, and `item3` has no tags.

1. `curation_tags=tagA`: only items containing `tagA` are considered (`item1`, `item2`), in alphabetic order of item name; both are processed when stop processing is false.
2. `curation_tags=tagA,tagB`: items with both tags are evaluated first, then items with either tag, never the untagged ones. Within each group the order is alphabetic by name, and several rules run if `stop_processing` is `false`.
3. No `curation_tags` in the search: only untagged rules are considered.

## stop_processing

Default `true`: processing stops at the first matching rule. Set `false` to let multiple actions fire in sequence. Rules run in lexical order of their `id`.

A tag-only rule with no query or filter is how diversity overrides are triggered (see the diversity skill).

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.

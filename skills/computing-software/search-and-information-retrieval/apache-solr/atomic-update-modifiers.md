---
id: computing-software.search-and-information-retrieval.apache-solr.atomic-update-modifiers
name: atomic-update-modifiers
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [partial-updates, atomic-updates, in-place-updates, set-add-inc, partial-update, require-in-place]
level: practitioner
status: docs-checked
description: "Update part of a Solr document with atomic and in-place updates: set, add, add-distinct, remove, removeregex, inc, storage requirements, and update.partial.requireInPlace."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/partial-document-updates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# atomic-update-modifiers

Wrap a field value in a modifier object together with the document `id`:
- `set`: replace values; null or empty list removes them.
- `add`: append to a multiValued field.
- `add-distinct`: append only if not already present.
- `remove`: remove all occurrences of the value(s).
- `removeregex`: remove values matching a regex.
- `inc`: add a positive or negative number to a numeric field.

Storage requirements: every field must be `stored="true"` or `docValues="true"`, except copyField destinations, which must be `stored="false"` and `docValues="false"`; their data must come only from copy sources. Derived fields from spatial types and CurrencyFieldType must be unstored too.

In-place updates are the cheaper subset. An atomic update runs in place only when the updated fields are non-indexed, non-stored, single-valued numeric docValues fields, `_version_` is also docValues-only, and any copy targets meet the same conditions. Pass `update.partial.requireInPlace=true` to fail the request instead of silently falling back to a full atomic update.

Child documents can be updated too, but need `_root_` and routing by root id in SolrCloud.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Partial Document Updates page: every modifier, the Field Storage rules and copyField destinations, derived spatial and CurrencyFieldType fields, the in-place update conditions, `update.partial.requireInPlace`, and the child document `_root_` and routing note. Nothing removed.

Method: documentation only; no commands were run.

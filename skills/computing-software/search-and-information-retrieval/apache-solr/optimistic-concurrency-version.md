---
id: computing-software.search-and-information-retrieval.apache-solr.optimistic-concurrency-version
name: optimistic-concurrency-version
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [optimistic-concurrency, version-field, http-409, conditional-update]
level: practitioner
status: docs-checked
description: "Use Solr optimistic concurrency with the _version_ field: conflicting writes return HTTP 409, and version values above 1, 1, 0 and negative mean different match rules."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/partial-document-updates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# optimistic-concurrency-version

Each document has a `_version_` value maintained by Solr (the default schema defines the field). Send it back with an update to make the write conditional.

Rules for the `_version_` you send:
- Greater than 1: must equal the version in the index.
- Exactly 1: the document must simply exist.
- Below 0 (for example -1): the document must not exist.
- 0: no check; version and existence do not matter.

On a mismatch Solr returns HTTP 409. The client should re-read the document, reapply its change and resubmit.

You can pass `_version_` as a request parameter or embed it in each document, which suits batches where each document has its own version. Add `versions=true` to the update request to get the new `_version_` back without a separate `/get` call.

If a document without `_version_` is sent and atomic updates are not in use, normal rules apply, usually replacing the previous document. Optimistic concurrency can be combined with atomic updates.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Partial Document Updates page (Optimistic Concurrency section): default `_version_` field, the four version rules, HTTP 409 and restart workflow, request-parameter or embedded `_version_`, `versions=true`, and the missing-`_version_` rule. Nothing removed.

Method: documentation only; no commands were run.

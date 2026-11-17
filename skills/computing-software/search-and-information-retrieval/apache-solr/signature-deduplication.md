---
id: computing-software.search-and-information-retrieval.apache-solr.signature-deduplication
name: signature-deduplication
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [deduplication, signature-processor, lookup3signature, near-duplicates, overwritedupes]
level: advanced
status: docs-checked
description: "Detect duplicate and near-duplicate Solr documents with SignatureUpdateProcessorFactory: Lookup3, MD5 or TextProfile signatures, overwriteDupes, and the SolrCloud restrictions."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/de-duplication.html
  - https://solr.apache.org/guide/solr/latest/configuration-guide/update-request-processors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# signature-deduplication

Register `solr.processor.SignatureUpdateProcessorFactory` in an `updateRequestProcessorChain` before `RunUpdateProcessorFactory`.

Signature classes:
- `Lookup3Signature` (default): 64-bit hash, exact duplicates, faster and smaller than MD5.
- `MD5Signature`: 128-bit hash, exact duplicates.
- `TextProfileSignature`: fuzzy Nutch hash for near duplicates, best on longer text.

Properties: `signatureClass`, `fields` (comma list, default all fields), `signatureField` (must be defined in the schema), `enabled` (default true), `overwriteDupes` (default true; then `signatureField` must be indexed).

SolrCloud restrictions:
- `overwriteDupes=true` only works when the signature field is the uniqueKey field, because of how updates are forwarded to replicas.
- In that case the processor must run before `DistributedUpdateProcessor` so the generated key routes to the correct shard leader.
- Using another signature field with `overwriteDupes=false` (just tagging) has no limits.

## Checked

2026-11-04. Confirmed against the De-Duplication page: signature classes, processor properties and defaults, SolrCloud restrictions. Nothing removed.

Method: documentation only; no commands were run.

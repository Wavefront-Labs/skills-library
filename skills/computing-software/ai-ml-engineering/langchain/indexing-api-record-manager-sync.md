---
id: computing-software.ai-ml-engineering.langchain.indexing-api-record-manager-sync
name: indexing-api-record-manager-sync
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, vector-store, langchain-indexing-api, record-manager, incremental-indexing, sqlrecordmanager]
level: practitioner
status: docs-checked
description: "Keep a vector store in sync with sources using LangChain's index() and a RecordManager: cleanup modes, source ids, hashing, and avoiding duplicates."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/indexing.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/master/libs/core/langchain_core/indexing/api.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indexing API with RecordManager

**Goal:** re-run ingestion without re-embedding unchanged chunks, without duplicates, and with changed source content cleaned up.

## Setup
```python
from langchain.indexes import SQLRecordManager, index
record_manager = SQLRecordManager("pgvector/handbook", db_url="sqlite:///record_manager_cache.sql")
record_manager.create_schema()          # required before first use
result = index(chunks, record_manager, vectorstore, cleanup="incremental",
               source_id_key="source", key_encoder="sha256")
print(result)   # {'num_added': 2, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 0}
```
The record manager stores, per document, a hash of page content and metadata, the write time and the source id. Unchanged documents are skipped, which also skips the embedding call. `index` accepts an iterable of documents or a loader.

## Cleanup modes
| Mode | Cleans deleted source docs | Cleans changed docs | When cleanup runs | Parallelizable |
|---|---|---|---|---|
| `None` | no | no | never (still de-duplicates) | yes |
| `"incremental"` | no | yes | continuously, as it writes | yes |
| `"full"` | yes | yes | after all batches | no |
| `"scoped_full"` | no | yes | after all batches | yes |

- `incremental`: deletes stale documents whose source ids were seen in this run. Needs `source_id_key`; if chunks of one source span several batches there is redundant work, so use as large a batch as possible.
- `full`: deletes everything in the store not returned by the loader this run. The loader must return the entire dataset, otherwise it deletes content it should not. (`index([], ..., cleanup="full")` clears a store.)
- `scoped_full`: like full but only deletes stale documents for source ids seen this run; suited to when a good batch size is hard to pick or the loader cannot return everything at once. It tracks source ids in memory.
- While content is being mutated both old and new versions can be returned until cleanup finishes; incremental shortens that window.

## Requirements and gotchas
- Do not use with a store pre-populated outside the indexing API: the record manager does not know those records exist.
- The vector store must support `add_documents` with `ids` and `delete` with `ids`.
- `source_id_key` should point at the ultimate source of a chunk (all chunks of a parent file share it). Only omit it if you never use incremental mode.
- Namespace suggestion from the docs: include the vector store and collection, for example `redis/my_docs`.
- Hashing defaults to SHA-1, which warns; pass `key_encoder` as `"sha256"`, `"sha512"`, `"blake2b"` or a callable.
- The hash covers metadata as well as content, so a metadata field that changes each run makes the record look changed.
- Cleanup is time-based: two back-to-back runs finishing within the same clock tick may fail to clean up (the docs call this unlikely).
- `force_update=True` re-writes documents even if present in the record manager (useful after changing embeddings).

## Verify
- [ ] Second run over unchanged input reports `num_added == 0` and `num_skipped == total`.
- [ ] Editing one document updates only its chunks; removing one source is only purged by a `"full"` run.

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 indexing how-to notebook and langchain_core indexing/api.py: result keys, cleanup-mode table and descriptions, full-mode warning, scoped_full rationale, requirements (ids on add/delete, no pre-populated stores), namespace suggestion, source guidance, time-based caution, key_encoder values and SHA-1 default warning, force_update.
- Removed as unconfirmed: the langchain_classic import path, Postgres connection example, the claim that a namespace reused across collections corrupts bookkeeping, the claim that changing the encoder forces a full re-embed, the non-transactional/orphans note, example numbers (4310 skipped).
Method: documentation only; no commands were run.

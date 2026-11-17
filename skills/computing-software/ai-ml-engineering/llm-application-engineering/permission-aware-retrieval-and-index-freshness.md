---
id: computing-software.ai-ml-engineering.llm-application-engineering.permission-aware-retrieval-and-index-freshness
name: permission-aware-retrieval-and-index-freshness
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, acl-aware-retrieval, rag, document-permissions, index-freshness, multi-tenant]
level: practitioner
status: draft
description: "Keep RAG from leaking documents: ACL metadata on chunks, query-time pre-filtering by user and groups, tenant isolation, permission sync, deletes and freshness SLOs."
sources:
  - https://qdrant.tech/documentation/concepts/filtering/
  - https://www.postgresql.org/docs/current/ddl-rowsecurity.html
  - https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/
  - https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Permission-aware retrieval and index freshness

**Goal:** a user's RAG answers only ever use documents that user can open right now, and the index reflects edits and deletions within an agreed delay.

## Why it is hard
The LLM summarises whatever is retrieved. If retrieval ignores permissions, the assistant becomes a way to read HR files or another customer's data (OWASP LLM08 vector and embedding weaknesses). Prompt instructions cannot fix this.

## Store ACLs with every chunk
```json
{"doc_id": "drive:1Abc", "tenant_id": "acme", "allowed_principals": ["u:123", "g:finance", "g:all-staff"],
 "source_updated_at": "2026-10-17T09:12:00Z", "indexed_at": "2026-10-17T09:14:03Z"}
```
Copy permissions from the source system (SharePoint, Drive, Confluence, DB rows) at ingest; flatten nested groups or store group ids and expand the user side at query time.

## Filter before ranking
Resolve the caller's principals from the identity provider per request (user id + all groups), then apply a pre-filter inside the vector search:
```python
from qdrant_client import models
flt = models.Filter(must=[
    models.FieldCondition(key="tenant_id", match=models.MatchValue(value=user.tenant)),
    models.FieldCondition(key="allowed_principals", match=models.MatchAny(any=user.principals)),
])
hits = qdrant.query_points("chunks", query=qvec, query_filter=flt, limit=20)
```
pgvector: `WHERE tenant_id = $1 AND allowed_principals && $2` (index the array with GIN) or Postgres row-level security. Index the filter fields (Qdrant payload index) or filtered HNSW search degrades.
Do not retrieve top-k unfiltered and drop forbidden results afterwards: it leaks via counts and timing, and collapses recall when most results are forbidden.

## Tenant isolation
Strongest: separate collection/index per tenant. Shared index: tenant filter enforced in a single data-access layer that every query passes through, plus tests.

## Freshness and deletion
- Incremental sync from source change feeds (webhooks, delta APIs) for content and permission changes; a permission revocation must propagate as fast as a deletion.
- Deletes: tombstone and remove chunks by `doc_id`; verify in a reconciliation job comparing source ids to index ids.
- Record `source_updated_at` and `indexed_at`; monitor lag (p95) against an SLO such as 15 minutes for permissions, 24 hours for content.
- Caches of retrieved results or generated answers must key on the user's principals, or they leak across users.

## Verify
- [ ] Test users with different groups get different results for the same query; forbidden documents never appear.
- [ ] Revoking access removes the document from that user's results within the SLO.
- [ ] Reconciliation finds no index entries for deleted source documents.

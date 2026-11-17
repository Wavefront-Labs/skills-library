---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.search-store-selection
name: search-store-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, search-store-selection, opensearch, elasticsearch, vector-search, azure-ai-search]
level: practitioner
status: draft
description: "Select a search and analytics store: OpenSearch/Elasticsearch, Azure AI Search, vector options, database-native search; relevance needs, indexing pipeline, sizing and cost."
sources: ["https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html", "https://learn.microsoft.com/azure/search/search-what-is-azure-search", "https://www.elastic.co/guide/en/elasticsearch/reference/current/size-your-shards.html", "https://www.postgresql.org/docs/current/textsearch.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Search and analytics store selection

## Steps
1. **Clarify the need**: full-text relevance (ranking, stemming, synonyms, facets), log and
   observability analytics, vector/semantic search, or simple filtering.
2. **Options**:
   - Database-native: Postgres full-text search and pgvector, MongoDB Atlas Search; no extra
     system, fine for moderate scale.
   - Managed OpenSearch/Elasticsearch (OpenSearch Service, Elastic Cloud): rich full-text and
     log analytics; serverless collections exist for spiky use.
   - Azure AI Search / Vertex AI Search: managed with semantic ranking and connectors.
   - Dedicated vector databases only when vector scale or features exceed the above.
3. **Indexing pipeline**: CDC or events from the system of record into the index; search
   store is never the source of truth; rebuild procedure from source.
4. **Sizing** (Elasticsearch/OpenSearch): shard sizes roughly 10-50 GB, replicas for HA and
   read throughput, hot-warm-cold tiers for logs, index lifecycle policies.
5. **Relevance testing**: judgement lists and offline metrics before go-live.
6. **Cost**: memory-heavy nodes; logs often cheaper in object-store-backed tiers.

## Gotchas
- Too many small shards exhaust cluster heap; oversharding is the usual OpenSearch failure.
- Using the search index as the primary store loses data on reindex mistakes.

## Verify
- [ ] Full rebuild from source tested and timed.
- [ ] Shard sizing and lifecycle policies applied.

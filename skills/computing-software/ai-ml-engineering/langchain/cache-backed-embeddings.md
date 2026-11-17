---
id: computing-software.ai-ml-engineering.langchain.cache-backed-embeddings
name: cache-backed-embeddings
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, cachebackedembeddings, embeddings-cache, localfilestore, re-embedding, cost-control]
level: practitioner
status: verified
description: "Avoid re-embedding unchanged text with CacheBackedEmbeddings: byte stores (local, Redis), namespace by model, query embedding caching and key hashing choices."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CacheBackedEmbeddings

**Why:** re-indexing a corpus after a chunking tweak or pipeline rerun re-embeds identical chunks, costing time and money. A cache keyed by text hash returns stored vectors.

## Setup
```python
# langchain 1.x: these two moved to the langchain-classic package (the old `langchain.embeddings` / `langchain.storage` imports fail)
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

base = OpenAIEmbeddings(model="text-embedding-3-large")
store = LocalFileStore("./emb_cache")                   # or RedisStore / any ByteStore
emb = CacheBackedEmbeddings.from_bytes_store(
    base, store,
    namespace=base.model,                # default is "" (not enforced); set it so caches are separate per model
    query_embedding_cache=True,          # also cache embed_query results (off by default)
    key_encoder="sha256")                # default "sha1" emits a warning (run); also accepts blake2b, sha512, or a callable
vs = FAISS.from_documents(chunks, emb)   # first run computes, later runs hit the cache
```

## Behaviour
- `embed_documents` checks the cache per text, computes misses in batches, writes them back.
- Without a namespace, switching models returns vectors from the wrong model (silent quality collapse).
- Keys hash the raw text: any change (whitespace, metadata injected into text) is a miss. Normalize text before embedding if you want hits across trivial changes.

## Stores
- `LocalFileStore`: one file per vector; fine for small/medium corpora on one machine.
- `RedisStore` / `UpstashRedisByteStore`: shared across workers; set TTLs if storage is limited.
- `InMemoryByteStore`: tests and notebooks.

## Alternatives
The LangChain Indexing API with a RecordManager avoids re-adding unchanged documents to the vector store at all; the embedding cache complements it when rebuilding from scratch.

## Verify
- [ ] Second indexing run issues zero embedding API calls (check provider usage or count cache misses by wrapping the base embeddings).

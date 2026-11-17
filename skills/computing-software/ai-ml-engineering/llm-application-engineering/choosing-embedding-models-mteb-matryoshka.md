---
id: computing-software.ai-ml-engineering.llm-application-engineering.choosing-embedding-models-mteb-matryoshka
name: choosing-embedding-models-mteb-matryoshka
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, embeddings, vector-search, embedding-model-selection, matryoshka-embeddings, mteb, retrieval-evaluation]
level: practitioner
status: draft
description: "Choose an embedding model for retrieval: MTEB as a shortlist, evaluating on your own queries, dimensions and Matryoshka truncation, query/document input types, cost and hosting."
sources:
  - https://huggingface.co/spaces/mteb/leaderboard
  - https://platform.openai.com/docs/guides/embeddings
  - https://docs.voyageai.com/docs/embeddings
  - https://sbert.net/examples/sentence_transformer/training/matryoshka/README.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing embedding models

## Shortlist
- **MTEB leaderboard** (Retrieval task tab, your language) for candidates; check model size, max input tokens, licence, and whether results are self-reported. Leaderboard rank does not transfer reliably to your domain.
- Hosted APIs: Voyage AI (Anthropic does not offer its own embedding model and points to Voyage), OpenAI `text-embedding-3-small/-large`, Cohere, Google. Open models: BGE, E5, GTE, Nomic, Jina families via sentence-transformers or TEI.
- Domain-specific variants (code, legal, finance, multilingual) often beat general leaders in-domain.

## Evaluate on your data (the step that matters)
1. Build 100-500 real queries with labelled relevant chunks (from logs, or LLM-generated questions per chunk reviewed by humans).
2. Embed the corpus with each candidate, same chunking.
3. Measure recall@k (k = what you pass to the LLM or reranker) and nDCG@10; also latency and cost per million tokens.
```python
from sentence_transformers import SentenceTransformer
m = SentenceTransformer("BAAI/bge-base-en-v1.5")
q = m.encode(queries, normalize_embeddings=True, prompt_name=None)
d = m.encode(chunks, normalize_embeddings=True, batch_size=64)
hits = (q @ d.T).argsort(axis=1)[:, ::-1][:, :10]
```

## Asymmetric inputs
Many models expect different handling for queries and documents: Voyage `input_type="query" | "document"`, E5 prefixes `"query: "` / `"passage: "`, BGE query instruction, sentence-transformers `prompt_name="query"`. Getting this wrong costs several recall points silently.

## Dimensions and Matryoshka
- Storage and ANN memory scale with dimensions x vectors x bytes. 10M x 3072 float32 = ~123 GB before index overhead.
- Matryoshka-trained models (OpenAI text-embedding-3, Voyage, Nomic, many newer open models) keep most quality when truncated: request `dimensions=512` (OpenAI) / `output_dimension` (Voyage), or slice the vector and **re-normalise** before cosine/dot.
- Quantisation (int8, binary) cuts memory 4-32x; rescore top candidates with full precision.
- Evaluate the truncated/quantised variant, not just the full one.

## Lock-in
Changing models requires re-embedding everything (vectors from different models are incomparable). Store `embedding_model` and `dim` with each vector/collection and plan migrations.

## Verify
- [ ] Comparison table: recall@k, nDCG, p95 latency, cost, memory for each candidate and dimension.
- [ ] Query/document input types set as each model's docs specify.

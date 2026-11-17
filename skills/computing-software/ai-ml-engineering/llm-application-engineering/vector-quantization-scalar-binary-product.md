---
id: computing-software.ai-ml-engineering.llm-application-engineering.vector-quantization-scalar-binary-product
name: vector-quantization-scalar-binary-product
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, vector-quantization, product-quantization, binary-quantization, faiss, qdrant]
level: practitioner
status: gated
description: "Shrink vector indexes with scalar int8, binary and product quantization in Qdrant, FAISS and pgvector, using oversampling and rescoring, measured against exact search."
sources:
  - https://qdrant.tech/documentation/guides/quantization/
  - https://github.com/facebookresearch/faiss/wiki/Faiss-indexes
  - https://github.com/pgvector/pgvector#binary-quantization
  - https://huggingface.co/blog/embedding-quantization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vector quantization (scalar, binary, product)

**Goal:** cut vector memory and cost by 4-32x while keeping recall@k within an agreed tolerance of full-precision search.

## Options
| Method | Compression vs float32 | Recall impact | Notes |
|---|---|---|---|
| float16 / halfvec | 2x | negligible | easy first step |
| Scalar int8 | 4x | small | per-dimension range, quantile clipping |
| Binary (1 bit/dim) | 32x (128 bytes for 1024 dims, computed) | large alone, small with rescoring | works best for high-dimensional, centred vectors: Qdrant's docs say 1-bit loses a lot below about a thousand dimensions and cite 1536-d ada-002 at 0.98 recall@100 with 4x oversampling and 4096-d Cohere v2 at 0.98 recall@50 with 2x |
| Product quantization (PQ) | up to 64x (FAISS `PQ64` on 1024 dims = 64 bytes vs 4096, ran) | moderate | splits vector into m sub-vectors, 1 byte each (8 bits); `d` must be a multiple of `m` (`index_factory(100, "PQ64")` fails) |
Combine with Matryoshka truncation (fewer dimensions) where the model supports it.

## Qdrant
```python
from qdrant_client import models
client.create_collection("chunks",
    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE, on_disk=True),
    quantization_config=models.ScalarQuantization(
        scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8, quantile=0.99, always_ram=True)))
client.query_points("chunks", query=q, limit=10,
    search_params=models.SearchParams(quantization=models.QuantizationSearchParams(rescore=True, oversampling=2.0)))
```
Quantized vectors in RAM for the candidate search, full vectors on disk for rescoring the top `limit x oversampling`. `BinaryQuantization` uses the same pattern with higher oversampling. Ran against a qdrant 1.19.2 server (qdrant-client 1.19.1) on 3,000 random 128-d vectors with `on_disk=True`: INT8 with `quantile=0.99` held recall@10 = 1.0 for every setting; binary on this low-dimensional data gave recall@10 0.187 with `rescore=False`, 0.46 with the default and with `oversampling=1.0`, 0.627 at 2.0 and 0.753 at 4.0, which illustrates the low-dimension warning above (random Gaussian data is a hard case, not a model of real embeddings). `get_collection` echoed both configs. Qdrant's docs now list four methods (scalar, binary, product, and TurboQuant) with up to 4x, 32x, 64x and 32x compression.

## FAISS
```python
import faiss
index = faiss.index_factory(1024, "IVF4096,PQ64", faiss.METRIC_INNER_PRODUCT)   # 64 bytes per vector (built OK: IndexIVFPQ)
index.train(train_vecs)       # representative sample: FAISS wants at least 39 x nlist points (min_points_per_centroid = 39), and PQ's 256 codes per sub-quantizer need 9,984
index.add(all_vecs); index.nprobe = 32
```
`OPQ64,IVF4096,PQ64` adds a learned rotation for better accuracy (builds as `IndexPreTransform`). Refine with an `IndexRefineFlat` wrapper (or the `,RFlat` factory suffix) to rerank with exact distances; wrap the still-empty base index, because `IndexRefineFlat(base)` on an index that already holds vectors fails the `ntotal` equality check; set `k_factor` for the shortlist size. On 20,000 random 64-d unit vectors (IVF128,PQ16, nprobe 8) recall@10 vs exact was 0.344 plain, 0.355 with OPQ and 0.42 with refine at `k_factor=4`: random data is a worst case, so measure on your own vectors. Training on 30 x nlist points (3,840 for nlist 128) printed "please provide at least 4,992 training points" (39 x 128).

## pgvector
`halfvec` columns for 2x (pgvector README: `halfvec` indexes up to 4,000 dimensions); binary: index `(binary_quantize(embedding)::bit(1024)) bit_hamming_ops`, query with the Hamming operator `<~>`, select a shortlist (the README example takes 20 to return 5), then re-order by exact cosine on the full vector in an outer query. Operators and index shapes copied from the pgvector README (fetched); no Postgres with pgvector was run here, so the SQL itself is unexecuted (gated: unconfirmed, source is paywalled or blocked).

## Measure
Compute ground truth with exact search on a sample of real queries; report recall@10 and end-task metrics (RAG answer quality) for each configuration, plus latency and memory. Pick the cheapest setting within tolerance (e.g. recall@10 >= 0.95 of exact).

## Gotchas
- PQ/IVF need training on data like production; retrain after major corpus or model changes.
- Rescoring requires keeping full vectors somewhere (disk is fine).
- Quantization interacts with filters: heavy filtering plus low oversampling hurts recall more.

## Verify
- [ ] Recall@k vs exact measured on real queries for the chosen config.
- [ ] Memory per million vectors documented.

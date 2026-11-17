---
id: computing-software.search-and-information-retrieval.qdrant.product-turbo-quantization
name: product-turbo-quantization
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [product-quantization, turboquant, bits4, rescore, quant-turbo]
level: advanced
status: docs-checked
description: "Product quantization for up to 64x compression and TurboQuant with bits1 to bits8, its defaults and rescoring."
sources:
  - "https://qdrant.tech/documentation/manage-data/quantization/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Two more quantization methods cover other trade-offs.

Product quantization (v1.2.0) splits vectors into chunks and replaces each with a centroid index (256 centroids, one byte each), giving compression up to 64x. Its distance calculations are not SIMD-friendly, so it is slower than scalar quantization, and it loses accuracy, so the docs recommend it only for high-dimensional vectors when memory is the top priority.

TurboQuant (v1.18.0; `bits8` from v1.20.0) is configured by bit depth:

```json
{ "quantization_config": { "turbo": { "bits": "bits4" } } }
```

Options: `bits1`, `bits1_5`, `bits2`, `bits4` (the default) and `bits8`, covering roughly 4x (`bits8`) to 32x (`bits1`) compression.

Behaviour from the docs:

- Search is asymmetric by default, with the query at higher precision.
- `bits2`, `bits1_5` and `bits1` are rescored by default, `bits4` and `bits8` are not; the `rescore` search parameter overrides that.
- Cosine, Dot and Euclidean get SIMD-accelerated scoring; L1 (Manhattan) is supported but significantly slower, so the docs point to scalar quantization there.

Mapping in the guidance table: 4x with bits8, 8x with bits4, 16x with bits2, about 21x with bits1_5, 32x with bits1 or binary, up to 64x with product quantization.

## Checked

2026-11-03. Confirmed on the Qdrant quantization page: product quantization up to 64x, 256 centroids, not SIMD-friendly; TurboQuant bit depths and compression ratios, `bits4` default, v1.18.0 and v1.20.0 gates, asymmetric by default, rescoring defaults, L1 note. Fixed the REST key (`turbo`, not `turboquant`) and the garbled version note. Removed the generic closing tip and the unconfirmed 'slower to build' claim.

Method: documentation only; no commands were run.

---
id: computing-software.search-and-information-retrieval.qdrant.scalar-quantization
name: scalar-quantization
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [scalar-quantization, int8, quantile, always-ram, quant-scalar]
level: practitioner
status: docs-checked
description: "Compress float32 vectors to int8 with scalar quantization, a 4x reduction, with quantile and memory options."
sources:
  - "https://qdrant.tech/documentation/manage-data/quantization/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Scalar quantization converts each float32 component to an 8-bit integer, cutting vector memory 4x and speeding up scoring with SIMD instructions.

```http
PUT /collections/{collection_name}
{
  "vectors": { "size": 768, "distance": "Cosine" },
  "quantization_config": {
    "scalar": { "type": "int8", "quantile": 0.99, "memory": "pinned" }
  }
}
```

Options:

- `type`: `int8`, the only value currently supported.
- `quantile`: the share of values kept when computing the range; `0.99` excludes the extreme 1 percent so outliers do not stretch the scale.
- `memory`: `pinned` always keeps the quantized vectors in RAM; by default placement follows the original vectors. The `memory` parameter is from v1.19; older versions use `always_ram`.

Search can then rescore the top candidates against the original vectors:

```json
{ "params": { "quantization": { "rescore": true, "oversampling": 2.0 } } }
```

The quantization guidance table recommends scalar quantization for 4x compression when you use the Manhattan metric, where TurboQuant is slow, and TurboQuant bits8 otherwise.

The docs report an error below 1% in their experiments, usually less significant for high-dimensional vectors. Scalar quantization is available from v1.1.0. Rescoring is off by default for scalar quantization.

## Checked

2026-11-03. Confirmed on the Qdrant quantization page: float32 to 8-bit, 4x reduction, `type: int8` only, `quantile` excluding extreme values, `memory: pinned`, rescoring off by default for scalar, the Manhattan guidance. Replaced `always_ram` with `memory`. Removed the generic recall tip and the size arithmetic paragraph.

Method: documentation only; no commands were run.

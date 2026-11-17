---
id: computing-software.search-and-information-retrieval.qdrant.binary-quantization
name: binary-quantization
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [binary-quantization, one-bit, asymmetric, oversampling, quant-binary]
level: advanced
status: docs-checked
description: "Binary quantization gives 32x compression with 1-bit, plus 1.5-bit and 2-bit encodings, asymmetric search and rescoring."
sources:
  - "https://qdrant.tech/documentation/manage-data/quantization/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Binary quantization stores each component as bits, a 32x reduction at 1 bit per dimension, with large speedups: the docs cite up to 40x.

```http
PUT /collections/{collection_name}
{
  "vectors": { "size": 1536, "distance": "Cosine" },
  "quantization_config": { "binary": { "memory": "pinned" } }
}
```

The `encoding` parameter selects more bits: `one_and_half_bits` (1.5-bit) and `two_bits` (2-bit) trade some compression for accuracy. Both are available from v1.15. Asymmetric quantization scores binary stored vectors against a differently encoded query: set `query_encoding` to `scalar8bits` or `scalar4bits` (`default` and `binary` use a binary query). `memory: pinned` keeps the quantized vectors in RAM (the `memory` parameter is from v1.19; older versions use `always_ram`).

Guidance:

- It suits high-dimensional vectors with a centered distribution; one-bit storage loses precision below about a thousand dimensions, where the 1.5-bit and 2-bit encodings help.
- The docs recommend rescoring against the original vectors, and oversampling of 3 as a starting point:

```json
{ "params": { "quantization": { "rescore": true, "oversampling": 3.0 } } }
```

- The docs table suggests binary or TurboQuant bits1 for 32x compression (binary is faster, TurboQuant gives better recall), and 2-bit for 16x.
- If the originals are stored on disk, rescoring can slow search significantly.

## Checked

2026-11-03. Confirmed on the Qdrant quantization page: 32x at one bit, up to 40x speedup, `one_and_half_bits` and `two_bits` encodings, `query_encoding` values, v1.15 and v1.19 version gates, rescoring and oversampling guidance. Replaced the unconfirmed `always_ram` example with `memory: pinned`. Removed the generic recall tip and padded closing paragraph.

Method: documentation only; no commands were run.

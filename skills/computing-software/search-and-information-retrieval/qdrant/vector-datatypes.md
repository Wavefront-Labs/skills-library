---
id: computing-software.search-and-information-retrieval.qdrant.vector-datatypes
name: vector-datatypes
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [datatype, float16, uint8, turbo, storage, vec-datatype]
level: advanced
status: docs-checked
description: "Select a storage datatype for vectors: float32 by default, or float16, uint8 and the turbo types."
sources:
  - "https://qdrant.tech/documentation/manage-data/collections/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Vector storage precision is a per-vector option set in the collection configuration through `datatype`.

```json
{ "vectors": { "size": 768, "distance": "Cosine", "datatype": "float16" } }
```

Supported datatypes listed in the docs:

- `float32` is the default (each dimension stored as a 32-bit float).
- `float16` is half-precision.
- `uint8` is for vectors that are already lower precision (unsigned 8-bit integers).
- `turbo4`, `turbo8` and `turbo16` are the TurboQuant datatypes, storing 4, 8 and 16 bits per dimension.

Guidance:

- This differs from quantization: the datatype changes how the stored vectors are represented, while `quantization_config` adds a compressed copy used for fast scoring and optional rescoring from the originals.
- Both can be combined.

The docs warn that `turbo4` on the original vectors shrinks the footprint further but can reduce recall and search quality.

## Checked

2026-11-03. Confirmed on the Qdrant collections page: the `datatype` option, `float32` default, `float16`, `uint8`, `turbo4`/`turbo8`/`turbo16` and their bit widths; on the quantization page: turbo4 can reduce recall, and the datatype can be combined with `quantization_config`. Removed the unconfirmed 'small accuracy cost', the disk-read claim and the generic testing tip.

Method: documentation only; no commands were run.

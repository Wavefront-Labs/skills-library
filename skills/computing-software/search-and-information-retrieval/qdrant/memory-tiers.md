---
id: computing-software.search-and-information-retrieval.qdrant.memory-tiers
name: memory-tiers
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [memory-tiers, pinned, cached, cold]
level: advanced
status: docs-checked
description: "Control where vectors, indexes and payloads live with the pinned, cached and cold memory tiers (v1.19)."
sources:
  - "https://qdrant.tech/documentation/ops-configuration/memory-tiers/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Memory tiers say how much of each data structure is kept in RAM. They apply from v1.19.

- `pinned`: loaded onto the heap and never evicted; the structure must always fit in RAM. Qdrant rejects it for dense vectors and payloads.
- `cached`: memory-mapped and pre-loaded into the disk cache at startup; the operating system can evict it under memory pressure.
- `cold`: memory-mapped but not pre-loaded; the first access to a page needs a disk read.

Structures that can be given a tier:

- dense vectors
- the HNSW graph
- quantized vectors
- the sparse index
- payloads
- payload indexes
- the ID tracker

```json
{ "vectors": { "size": 768, "distance": "Cosine", "memory": "cold" },
  "quantization_config": { "scalar": { "type": "int8" } } }
```

The older `on_disk` flags are deprecated in favour of `memory`.

Defaults from the docs: dense vectors and the HNSW index `cached`, payloads `cold`, the sparse index, payload indexes and ID tracker `pinned`. Quantized vectors follow the original vectors: `pinned` if the originals are cached, `cold` if they are cold.

## Checked

2026-11-03. Confirmed on the Qdrant memory tiers page: the three tiers and their behaviour, `pinned` rejected for dense vectors and payloads, the list of structures, the defaults, the deprecated `on_disk` flags. Removed the unconfirmed 'typical pattern' advice and the monitoring tip.

Method: documentation only; no commands were run.

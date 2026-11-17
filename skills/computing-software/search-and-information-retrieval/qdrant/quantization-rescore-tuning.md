---
id: computing-software.search-and-information-retrieval.qdrant.quantization-rescore-tuning
name: quantization-rescore-tuning
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [rescore, oversampling, recall, on-disk, quant-rescore]
level: advanced
status: docs-checked
description: "Pin the quantized copy in RAM, keep originals cold on disk, and use rescore and oversampling at query time."
sources:
  - "https://qdrant.tech/documentation/search-tuning/when-your-collection-outgrows-ram/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When a collection outgrows RAM, the tuning guide's approach is:

1. Quantize the vectors.
2. Pin the quantized copy in memory (`memory: pinned`; older versions use `always_ram`).
3. Leave the original vectors on disk (cold).
4. Search the quantized copy for candidates, then rescore the best ones from the originals.

```json
{ "query": [0.1, 0.2], "limit": 10,
  "params": { "quantization": { "rescore": true, "oversampling": 3.0 } } }
```

`oversampling` defines how many extra vectors are pre-selected from the quantized index and then rescored with the original vectors: with oversampling 2.4 and limit 100, 240 are pre-selected and the top 100 returned. Rescoring can slow search when the originals are on disk.

Strict mode can cap client-requested oversampling with `search_max_oversampling`.

## Checked

2026-11-03. Confirmed on the Qdrant quantization and search-tuning pages: pinned quantized vectors with cold originals, rescore and oversampling semantics with the 2.4 and 100 example, `memory` replacing `always_ram` from v1.19, `search_max_oversampling` in strict mode. Removed the unconfirmed tuning process and storage advice.

Method: documentation only; no commands were run.

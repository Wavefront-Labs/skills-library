---
id: computing-software.search-and-information-retrieval.qdrant.gpu-indexing
name: gpu-indexing
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [gpu, vulkan, indexing, docker-image]
level: advanced
status: docs-checked
description: "Speed up HNSW index building with GPU support: dedicated images, Vulkan 1.3 and gpu.indexing."
sources:
  - "https://qdrant.tech/documentation/ops-configuration/running-with-gpu/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

GPU acceleration is available from v1.13.0 and is used for indexing (`gpu.indexing`).

Requirements and setup from the docs:

- Use the dedicated GPU Docker images (NVIDIA, AMD); GPU support is not in the default binary.
- The device must support Vulkan API v1.3.
- Turn it on in the configuration:

```yaml
gpu:
  indexing: true
```

```bash
docker run --gpus all -p 6333:6333 \
  -e QDRANT__GPU__INDEXING=1 \
  qdrant/qdrant:gpu-nvidia-latest
```

Other `gpu` options on the page: `force_half_precision`, `groups_count`, `device_filter`, `devices`, `parallel_indexes` and `allow_integrated`. The page advises against changing the low-level ones unless you know the Qdrant internals and the Vulkan API.

## Checked

2026-11-03. Confirmed on the Qdrant running-with-GPU page: v1.13.0, dedicated NVIDIA and AMD images, Vulkan API v1.3, `gpu.indexing: true`, the other `gpu` options. Removed the unconfirmed claims about search speed, graph equivalence and bulk-import pairing, and the generic testing tip.

Method: documentation only; no commands were run.

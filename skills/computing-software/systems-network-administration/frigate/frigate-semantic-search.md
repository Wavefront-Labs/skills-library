---
id: computing-software.systems-network-administration.frigate.frigate-semantic-search
name: frigate-semantic-search
category: computing-software
field: systems-network-administration
product: frigate
tags: [semantic-search, jina-clip, embeddings, reindex, explore-view, enrichments]
level: advanced
status: docs-checked
description: "Enable Frigate semantic search, choose the Jina CLIP v1 or v2 model and size, meet RAM and CPU needs and reindex older objects."
sources: ["https://docs.frigate.video/configuration/semantic_search/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Semantic search in Frigate

Semantic search finds tracked objects by image, a text query or a generated description, using embeddings from Jina AI models stored in Frigate's database and run locally. It is used from the Explore view. A one-time internet connection downloads the models from HuggingFace, after which it works offline.

Requirements: at least 8 GB of RAM and a CPU with AVX and AVX2. A Raspberry Pi will not run it reliably. A GPU is not required but gives a large speedup; 16 GB RAM and a dedicated GPU are recommended.

Enable it globally (Settings, Enrichments, Semantic search):
```
semantic_search:
  enabled: True
  reindex: False
```
Frigate does not index older tracked objects automatically when you first enable it; press Reindex in the Enrichments settings or set `reindex: True` and restart (then set it back).

Models:
- `jinav1` with `model_size: small` (quantized, CPU-friendly, little loss in quality) or `large` (full model, uses the GPU when available). V1 embeds images and text into one space, so image to image and text to image searches both work, and it embeds object descriptions that you can edit on the Explore page. English only.
- `jinav2` adds 89 languages but offers only about 3% better retrieval and needs much more RAM and GPU; `large` is recommended and needs a discrete GPU. Native English speakers should stay on V1.
Switching between V1 and V2 requires a reindex because the embeddings are incompatible; without it, results are wrong.

A GenAI provider that has the `embeddings` role can be selected instead of a Jina model.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/semantic_search (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.

---
id: computing-software.systems-network-administration.immich.smart-search-clip-models
name: smart-search-clip-models
category: computing-software
field: systems-network-administration
product: immich
tags: [clip, smart-search, siglip, multilingual, model-name]
level: practitioner
status: docs-checked
description: "Choose and switch the CLIP model behind Immich Smart Search, including multilingual nllb, xlm and siglip2 options, and reprocess assets."
sources:
  - https://docs.immich.app/features/searching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: improve contextual search quality by changing the CLIP model.

Immich uses Postgres for metadata search and for CLIP-based contextual search, powered by the VectorChord extension. Contextual search lets you describe a photo freely without keywords. Other filters cover people, file name or extension, full path or folder, description, OCR text, locations, tags, camera, time frame, media type, display options and star rating.

The default model is fast; other models can return better results but are slower or use more memory, both for background Smart Search indexing and for searching.

Choosing:

- English-only users: look at the curated CLIP section of the model tables on the docs page, ordered from higher to lower quality.
- Other languages: use multilingual models. `nllb` models expect the query in the language set in user settings and perform best when users search mainly in one non-English language. `xlm` and `siglip2` models understand the query regardless of the language setting, which suits mixed-language search.

Switching:

1. Copy the model name, for example `ViT-B-16-SigLIP__webli`.
2. Administration, Settings, Machine Learning Settings, Smart Search: paste it into Model Name and save.
3. Go to the Job Status page and click "All" next to Smart Search to reprocess every asset with the new model.
4. Optionally check server and machine learning logs for errors.

If errors about leftover data from the old model appear in the logs after switching, change back to the previous model, save, and repeat the Job Status step.

## Checked

2026-11-09: read https://docs.immich.app/features/searching in full (search types, CLIP models section, switching steps, nllb/xlm/siglip2 guidance). Removed the preload variables (not on the page) and changed the Hugging Face pointer to the CLIP model list on the page.

Method: documentation only; no commands were run.

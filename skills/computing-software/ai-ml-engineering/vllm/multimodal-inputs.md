---
id: computing-software.ai-ml-engineering.vllm.multimodal-inputs
name: multimodal-inputs
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [multimodal, multi-modal-data, limit-mm-per-prompt, image-inputs, video-inputs, audio-inputs]
level: practitioner
status: docs-checked
description: "Pass image, video and audio inputs offline and online, cap items per prompt, and prune video tokens."
sources:
  - https://docs.vllm.ai/en/latest/features/multimodal_inputs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send images, video and audio to a multimodal model.

Offline, the prompt dict has `prompt` (in the format documented on the model's Hugging Face page) and `multi_modal_data`, a dict keyed by modality. A single image goes to the `image` key; pass a list for several images in one prompt, and raise the cap with `limit_mm_per_prompt={"image": 2}`. Video accepts a list of NumPy arrays under `video` (set `limit_mm_per_prompt={"video": 1}`); audio takes a tuple `(array, sampling_rate)` under `audio`.

Online, the OpenAI-compatible server takes multimodal data on the Chat Completions API. Cap items on the command line, for example `--limit-mm-per-prompt.image 2` for Phi-3.5-vision. If the model has no chat template fallback, supply one with `--chat-template`.

Other controls:
- `media_io_kwargs={"image": {"rgba_background_color": [0, 0, 0]}}` sets the background used when transparent images convert to RGB (default white).
- `--video-pruning-rate 0.75 --video-pruning-method vidcom2` prunes video tokens after the vision encoder for supported models, trading accuracy for prefill time and KV cache.
- `multi_modal_uuids` supplies stable IDs so caching avoids rehashing content; media can be omitted if the UUID is expected to hit the cache, else the request fails.

Security: set `--allowed-media-domains` to restrict fetchable domains against SSRF, and `VLLM_MEDIA_URL_ALLOW_REDIRECTS=0` to block redirects.

## Checked

2026-11-03. Confirmed against the Multimodal Inputs page (docs.vllm.ai/en/latest/): offline and online input forms, rgba_background_color default, video pruning, UUID caching and SSRF settings.

Method: documentation only; no commands were run.

---
id: computing-software.computer-graphics-engineering.computer-vision.vision-transformers-and-dinov2-features
name: vision-transformers-and-dinov2-features
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-deep-learning, vision-transformer, vit, dinov2, clip, foundation-models, linear-probe]
level: sme
status: draft
description: "Use vision transformers and foundation models: ViT patching, DINOv2 features for retrieval and dense tasks, CLIP zero-shot, and linear probes vs fine-tuning."
sources: ["https://arxiv.org/abs/2010.11929", "https://github.com/facebookresearch/dinov2", "https://github.com/openai/CLIP", "https://huggingface.co/docs/transformers/model_doc/dinov2", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vision transformers and foundation models

## 1. ViT essentials
- Image split into P x P patches (14 for DINOv2, 16 for ViT-B/16), each linearly embedded, plus a CLS token
  and position embeddings, through L transformer blocks.
- Token count = (H/P)*(W/P); attention cost grows with its square. 518 px with P=14 gives 37x37 = 1369 tokens.
- Input sizes must be multiples of P; position embeddings are interpolated for other resolutions.

## 2. DINOv2 as a frozen feature extractor
```python
import torch
from transformers import AutoImageProcessor, AutoModel
proc = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
model = AutoModel.from_pretrained("facebook/dinov2-base").eval().cuda()
with torch.inference_mode():
    out = model(**proc(images=imgs, return_tensors="pt").to("cuda"))
cls = out.last_hidden_state[:, 0]          # global descriptor -> retrieval, kNN, linear probe
patch = out.last_hidden_state[:, 1:]       # (B, N, D) dense features -> segmentation, depth, matching
```
- Retrieval/dedup: L2-normalise CLS (or CLS concat mean patch), cosine similarity, FAISS index.
- Dense tasks: reshape patch tokens to (h, w, D), train a linear head or upsample (PCA of patch features is a
  great sanity visualisation: parts get consistent colours across images).
- The `-reg` variants (with register tokens) remove high-norm artefact tokens in attention/feature maps.

## 3. CLIP zero-shot
Encode prompts like "a photo of a {label}" and the image; softmax over cosine similarities x logit scale.
Prompt ensembling (several templates averaged) adds a few points. Good for open-vocabulary filtering and
labelling bootstrap, weak at counting, fine-grained classes and spatial relations.

## 4. Adapting
1. Linear probe on frozen features (minutes, little data, strong baseline).
2. If short of target, fine-tune the last blocks or LoRA with a lower LR for the backbone (1e-5) than the head.
3. Full fine-tuning only with plenty of data; ViTs need strong augmentation and warmup.

## Gotchas
- Wrong normalisation (ImageNet mean/std) or resize policy silently lowers accuracy; use the model's processor.
- ViTs lack CNN inductive bias: small datasets from scratch underperform; always start pretrained.
- Licences differ per checkpoint; check before shipping.

## Verify
- [ ] Linear probe accuracy on a held-out split reported before any fine-tuning; PCA of patch features shows
  coherent object parts.

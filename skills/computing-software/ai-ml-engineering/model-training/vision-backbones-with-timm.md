---
id: computing-software.ai-ml-engineering.model-training.vision-backbones-with-timm
name: vision-backbones-with-timm
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, timm, pretrained-models, transfer-learning, vision-backbones, image-classification]
level: practitioner
status: verified
description: "Use timm for vision transfer learning: model discovery, create_model with num_classes/features_only, matching data config, layer-wise LR decay, and Hub weights."
sources:
  - https://huggingface.co/docs/timm/index
  - https://huggingface.co/docs/timm/feature_extraction
  - https://github.com/huggingface/pytorch-image-models
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vision backbones with timm

## Find a model
```python
import timm, timm.data, timm.optim      # `import timm` alone did not expose timm.optim (AttributeError) in timm 1.0.30
timm.list_models("convnext*", pretrained=True)[:10]   # ran: ['convnext_atto.d2_in1k', 'convnext_atto_ols.a2_in1k', 'convnext_base.clip_laion2b', ...]
timm.list_pretrained("vit_base_patch16_224*")       # pretrained tags (.augreg_in21k_ft_in1k, ...); ran, 11 entries incl. .augreg2_in21k_ft_in1k, .dino, .mae
```
Pick by accuracy/latency for your hardware; the timm results CSVs and the Hub model cards list ImageNet top-1, params and throughput.

## Create for your task
```python
model = timm.create_model("convnext_small.fb_in22k_ft_in1k", pretrained=True,
                          num_classes=12, drop_path_rate=0.1)     # new head, sized for 12 classes (ran with pretrained=False to skip the download: head has 12 outputs; all three tags below appear in `timm.list_pretrained()`)
backbone = timm.create_model("resnet50.a1_in1k", pretrained=True, features_only=True,
                             out_indices=(1, 2, 3, 4))            # multi-scale feature maps for detection/seg (ran: shapes (1,256,56,56), (1,512,28,28), (1,1024,14,14), (1,2048,7,7); strides 4, 8, 16, 32)
emb_model = timm.create_model("vit_small_patch16_224.augreg_in21k", pretrained=True, num_classes=0)  # pooled embeddings (ran with real weights: output (2, 384))
```

## Match preprocessing
```python
cfg = timm.data.resolve_model_data_config(model)
train_tf = timm.data.create_transform(**cfg, is_training=True, auto_augment="rand-m9-mstd0.5")
eval_tf = timm.data.create_transform(**cfg, is_training=False)
```
Input size, interpolation, mean/std and crop percentage come from the pretrained config; mismatches cost accuracy. For the ViT-S above `resolve_model_data_config` returned input (3,224,224), bicubic, mean and std 0.5, crop_pct 0.9; the eval transform printed as Resize(248) then CenterCrop(224) then Normalize, the train transform as RandomResizedCrop, flip, RandAugment (15 ops) then Normalize, and both returned (3, 224, 224) tensors from a 300x400 image.

## Fine-tuning recipe
- AdamW, lr ~1e-4 to 5e-4 (scaled with batch size), cosine schedule with warmup, weight decay 0.05.
- Layer-wise LR decay for ViTs (`timm.optim.create_optimizer_v2(model, "adamw", lr=..., layer_decay=0.75)`; ran: an `AdamW` with 26 param groups carrying graded `lr_scale` values).
- Stochastic depth (`drop_path_rate`), mixup/cutmix (`timm.data.Mixup`; ran: soft labels of shape (4, 12)), label smoothing for small datasets.
- Freeze-then-unfreeze helps when data is very small.

## Hub
`timm.create_model("hf-hub:org/model", pretrained=True)` loads custom weights (ran the `hf-hub:timm/resnet18.a1_in1k` form with `pretrained=False`: the config resolved to that repo); `timm.models.push_to_hf_hub` exists in timm 1.0.30 (checked by attribute only: an upload needs a Hub account) so check its current signature in the timm docs before relying on the arguments.

## Verify
- [ ] Linear-probe baseline (frozen backbone) vs full fine-tune on the same split; eval transform equals `resolve_model_data_config` output.

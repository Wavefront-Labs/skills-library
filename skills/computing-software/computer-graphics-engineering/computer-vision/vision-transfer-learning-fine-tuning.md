---
id: computing-software.computer-graphics-engineering.computer-vision.vision-transfer-learning-fine-tuning
name: vision-transfer-learning-fine-tuning
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, vision-deep-learning, cnn, transfer-learning, fine-tuning, timm, torchvision, frozen-backbone, discriminative-learning-rates, data-augmentation, albumentations]
level: practitioner
status: draft
description: "Fine-tune pretrained vision backbones on small datasets: choosing a backbone, frozen vs full fine-tuning, learning-rate schedules, augmentation with Albumentations."
sources: ["https://szeliski.org/Book/", "https://huggingface.co/docs/timm/index", "https://pytorch.org/vision/stable/models.html", "https://albumentations.ai/docs/", "https://cs231n.github.io/transfer-learning/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vision transfer learning and fine-tuning

**Goal:** a strong classifier/detector/segmenter from hundreds to a few thousand labelled
images by adapting an ImageNet- or foundation-model-pretrained backbone (Szeliski 2e §5.4).

## 1. Pick the backbone
- `timm` gives hundreds of pretrained models with consistent APIs and their preprocessing
  configs: `timm.create_model('convnext_tiny.fb_in22k', pretrained=True, num_classes=5)`.
- Small data, edge deployment: EfficientNet/MobileNetV3/ConvNeXt-T; more data or diverse
  domain: ViT/DINOv2 features (strong linear-probe baselines).
- Use the model's own normalisation: `timm.data.resolve_data_config({}, model=model)`.

## 2. Strategy by data size and domain gap
| situation | approach |
|---|---|
| tiny data (< 500), similar domain | freeze backbone, train head (linear probe) |
| moderate data | unfreeze all, low LR backbone (1e-5–1e-4), higher LR head (1e-3) |
| large domain gap (medical, satellite, thermal) | full fine-tune, longer, maybe in-domain pretraining |
Discriminative LRs:
```python
opt = torch.optim.AdamW([
  {"params": model.get_classifier().parameters(), "lr": 1e-3},
  {"params": [p for n, p in model.named_parameters() if "head" not in n], "lr": 1e-4}],
  weight_decay=0.05)
sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=[1e-3, 1e-4], total_steps=steps, pct_start=0.1)
```
Warm up, then cosine/one-cycle decay. BatchNorm with tiny batches: freeze BN statistics
(`model.eval()` for BN layers) or use GroupNorm/LayerNorm models.

## 3. Augmentation (Albumentations)
```python
train_tf = A.Compose([
  A.RandomResizedCrop(size=(224, 224), scale=(0.6, 1.0)),
  A.HorizontalFlip(p=0.5),                  # only if semantics allow (not for text, left/right labels)
  A.ColorJitter(0.2, 0.2, 0.2, 0.05, p=0.8),
  A.GaussNoise(p=0.2),
  A.Normalize(mean=cfg["mean"], std=cfg["std"]), ToTensorV2()])
```
Detection/segmentation: pass `bbox_params`/masks so boxes transform consistently. Match
augmentation to real variation (camera noise, lighting, blur) — not arbitrary.

## 4. Training hygiene
- Hold out a validation set split by **source** (camera/site/patient), not random frames.
- Monitor per-class metrics; imbalance → class weights or balanced sampling.
- Early stopping on validation metric; keep the best checkpoint; set seeds.
- Mixed precision (`torch.autocast`) for speed.

## Gotchas
- Preprocessing mismatch between training and deployment (RGB/BGR, normalisation, resize mode)
  is the top cause of "works in notebook, fails in prod".
- Fine-tuning everything with a high LR destroys pretrained features (catastrophic forgetting).
- Near-duplicate images across splits inflate validation scores.

## Verify
- [ ] Linear-probe baseline recorded before full fine-tuning.
- [ ] Validation split by source; test set untouched until final evaluation.
- [ ] Exported model + deployment preprocessing reproduces validation metrics.

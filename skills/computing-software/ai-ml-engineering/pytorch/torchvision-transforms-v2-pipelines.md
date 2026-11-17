---
id: computing-software.ai-ml-engineering.pytorch.torchvision-transforms-v2-pipelines
name: torchvision-transforms-v2-pipelines
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, transforms-v2, torchvision-transforms, data-augmentation, tv-tensors, bounding-boxes, randaugment]
level: practitioner
status: gated
description: "Build torchvision.transforms.v2 augmentation pipelines that transform images, boxes, masks and keypoints together, with tv_tensors, GPU batches and MixUp/CutMix."
sources:
  - https://pytorch.org/vision/stable/transforms.html
  - https://pytorch.org/vision/stable/auto_examples/transforms/plot_transforms_getting_started.html
  - https://pytorch.org/vision/stable/auto_examples/transforms/plot_cutmix_mixup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# torchvision.transforms.v2 pipelines

v2 is the current API (`torchvision.transforms.v2`). It is a drop-in for v1 on images and also transforms detection/segmentation targets consistently.

## Classification
```python
import torch
from torchvision.transforms import v2
train_tf = v2.Compose([
    v2.ToImage(),                                  # PIL/ndarray -> tv_tensors.Image (uint8)
    v2.RandomResizedCrop(224, antialias=True),
    v2.RandomHorizontalFlip(),
    v2.RandAugment(),                              # or v2.TrivialAugmentWide()
    v2.ToDtype(torch.float32, scale=True),         # uint8 [0,255] -> float [0,1]
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
eval_tf = v2.Compose([v2.ToImage(), v2.Resize(256, antialias=True), v2.CenterCrop(224),
                      v2.ToDtype(torch.float32, scale=True), v2.Normalize(...)])
```
- Do geometric ops on uint8, convert to float at the end (documented performance advice; not timed here). Both pipelines above ran on a 300x400 PIL image with torchvision 0.29.1 and returned `tv_tensors.Image` of shape `(3, 224, 224)`, float32 after `ToDtype`.
- `v2.ToTensor` is deprecated (constructing it emitted a deprecation warning in 0.29.1); use `ToImage()` + `ToDtype(..., scale=True)`.

## Detection / segmentation: wrap targets
```python
from torchvision import tv_tensors
img = tv_tensors.Image(img)
boxes = tv_tensors.BoundingBoxes(b, format="XYXY", canvas_size=img.shape[-2:])
mask = tv_tensors.Mask(m)
tf = v2.Compose([v2.RandomPhotometricDistort(), v2.RandomZoomOut(), v2.RandomIoUCrop(),
                 v2.RandomHorizontalFlip(), v2.SanitizeBoundingBoxes(), v2.ToDtype(torch.float32, scale=True)])
img, target = tf(img, {"boxes": boxes, "labels": labels, "masks": mask})
```
- Transforms dispatch on type: boxes are flipped/cropped, masks use nearest interpolation, plain tensors in the dict pass through untouched (run: a forced horizontal flip moved `[10,10,100,100]` on a 400-wide canvas to `[300,10,390,100]`, the mask stayed `uint8`, and a plain `torch.ones(3)` entry came back unchanged).
- `SanitizeBoundingBoxes` removes degenerate boxes after crops and drops matching `labels` (key name must be `labels` or set `labels_getter`; with a key named `tags` it raised `Could not infer where the labels are in the sample`).
- Torchvision datasets: `datasets.wrap_dataset_for_transforms_v2(ds)` returns tv_tensors automatically.

## Batch-level: MixUp / CutMix
Applied after the DataLoader on batches:
```python
cutmix_or_mixup = v2.RandomChoice([v2.CutMix(num_classes=1000), v2.MixUp(num_classes=1000)])
for x, y in loader:
    x, y = cutmix_or_mixup(x, y)       # y becomes soft one-hot (float, rows sum to 1); use CrossEntropyLoss with probabilities (checked)
```

## GPU augmentation
v2 ops accept batched `(N, C, H, W)` tensors and apply the same random parameters to the whole batch (checked on CPU: in 20 batches `RandomHorizontalFlip(p=0.5)` never flipped only some samples of a batch). GPU execution was not tested here (no GPU). For per-sample randomness on GPU use Kornia or DALI (gated: unconfirmed, source is paywalled or blocked); for CPU-bound loaders first check `num_workers`.

## Gotchas
- `antialias=True` is the default now (checked in the `Resize` and `RandomResizedCrop` signatures); old v1 code without it on tensors gave different results from PIL.
- Seed augmentation per worker (`worker_init_fn` / generator) or workers repeat identical augmentations.
- Keep eval transforms deterministic and identical to what the deployed model receives.

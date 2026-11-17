---
id: computing-software.computer-graphics-engineering.computer-vision.visual-anomaly-detection
name: visual-anomaly-detection
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, recognition, visual-anomaly-detection, anomalib, patchcore, industrial-inspection, one-class]
level: practitioner
status: draft
description: "Detect visual defects with few or no defect samples: PatchCore/PaDiM/EfficientAD in anomalib, normal-only training, threshold selection, pixel heatmaps and image vs pixel AUROC."
sources: ["https://anomalib.readthedocs.io/en/latest/", "https://www.mvtec.com/company/research/datasets/mvtec-ad", "https://arxiv.org/abs/2106.08265"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visual anomaly detection

Industrial inspection rarely has enough defect images. Train on **normal** images only and flag
deviations.

## Methods
| Method | Idea | Notes |
|---|---|---|
| PatchCore | Memory bank of pretrained patch features, kNN distance | Strong default, no training loop |
| PaDiM | Gaussian per patch position | Needs aligned parts |
| EfficientAD | Student-teacher + autoencoder | Fast inference (ms) |
| Reverse distillation, FastFlow | Feature reconstruction / flows | Good localisation |

## anomalib
```python
from anomalib.data import Folder
from anomalib.models import Patchcore
from anomalib.engine import Engine
dm = Folder(name="parts", root="data", normal_dir="good", abnormal_dir="defect", mask_dir="masks")
model = Patchcore(backbone="wide_resnet50_2", layers=["layer2", "layer3"], coreset_sampling_ratio=0.1)
engine = Engine(); engine.fit(model, datamodule=dm); engine.test(model, datamodule=dm)
```

## Data practice
- Fix the imaging: consistent lighting, pose, background, focus. Anomaly detectors flag any change,
  including a moved light.
- Crop/align to the part (template match or fixture); PaDiM in particular needs alignment.
- 100 to 500 good images usually suffice; include normal variation you want accepted.

## Thresholding
Scores are unitless. Choose the threshold on a validation set with a few real defects for the
required recall (missed defect cost) or, with no defects, at a high percentile of normal scores.
Track false reject rate in production.

## Metrics
Image AUROC, pixel AUROC, and PRO (per-region overlap) for localisation; report the operating point
(recall at fixed false positive rate) not just AUROC.

## Verify
Plant synthetic defects (scratches, spots) on held-out good images to estimate sensitivity
by defect size.

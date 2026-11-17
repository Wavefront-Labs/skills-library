---
id: computing-software.computer-graphics-engineering.computer-vision.grad-cam-model-interpretability
name: grad-cam-model-interpretability
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-deep-learning, grad-cam, interpretability, saliency-maps, explainability, shortcut-learning]
level: practitioner
status: verified
description: "Explain vision model predictions with Grad-CAM and related methods: target layer choice for CNNs/ViTs, pytorch-grad-cam usage, sanity checks and spotting shortcut learning."
sources: ["https://arxiv.org/abs/1610.02391", "https://github.com/jacobgil/pytorch-grad-cam", "https://arxiv.org/abs/1810.03292"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpretability (Grad-CAM)

Grad-CAM weights the feature maps of a convolutional layer by the spatially pooled gradients of
the target class score, then applies ReLU: a coarse heatmap of evidence for that class.

## Usage
```python
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
cam = GradCAM(model=model, target_layers=[model.layer4[-1]])          # ResNet
heat = cam(input_tensor=x, targets=[ClassifierOutputTarget(cls_idx)])[0]
vis = show_cam_on_image(rgb_float01, heat, use_rgb=True)
```
Ran with grad-cam 1.5.7 on torchvision ResNet-18: `heat` is (224, 224) in [0, 1] and `vis` is uint8 (224, 224, 3). `FasterRCNNBoxScoreTarget`, `SemanticSegmentationTarget`, `GradCAMPlusPlus`, `ScoreCAM`, `EigenCAM` and `HiResCAM` all exist in the package.

## Target layer
- CNNs: last conv block (`layer4[-1]`, `features[-1]`); earlier layers give finer but noisier maps.
- ViTs: a late block's norm layer (README: `model.blocks[-1].norm1`; Swin: `model.layers[-1].blocks[-1].norm1`) with a `reshape_transform` that drops the CLS token and reshapes
  tokens to a grid (the constructor is `GradCAM(model, target_layers, reshape_transform=None)`).
- Detectors/segmenters: use library targets (e.g. `FasterRCNNBoxScoreTarget`,
  `SemanticSegmentationTarget`).

## Variants
Grad-CAM++ (multiple instances), Score-CAM (gradient-free, slower), EigenCAM (class-agnostic),
HiResCAM (faithful for some architectures). Integrated Gradients / SHAP for pixel-level
attribution.

## Use it to find shortcut learning
Heatmaps on watermarks, rulers, text overlays, borders or backgrounds instead of the object mean the
model learned a dataset artefact. Fix data (crop, remove artefacts, balance backgrounds) and
retrain.

## Sanity checks (Adebayo et al.)
Randomise model weights or labels: a trustworthy method's maps must change drastically. Do not
present saliency as proof of correctness; pair it with quantitative tests (deletion/insertion
curves, accuracy on counterfactual images).

## Verify
Compare maps for correct vs incorrect predictions on 50 or more images; patterns across many images
matter more than single examples.

## Checked
grad-cam (pytorch-grad-cam) 1.5.7, PyTorch 2.14.1 CPU, torchvision 0.29.1.
- Run: the usage snippet (two targets in a batch of 2) and `show_cam_on_image`; existence of the target classes and CAM variants; inspected the constructor signature.
- Fetched: pytorch-grad-cam README (ViT/Swin target layers, reshape transform removes the class token, method table), arXiv API titles for Grad-CAM (1610.02391) and Sanity Checks for Saliency Maps (1810.03292).

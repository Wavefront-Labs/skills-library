---
id: computing-software.computer-graphics-engineering.computer-vision.cnn-backbones-resnet-efficientnet
name: cnn-backbones-resnet-efficientnet
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-deep-learning, resnet, efficientnet, convnext, mobilenet, backbone]
level: practitioner
status: draft
description: "Choose and adapt CNN backbones (ResNet, EfficientNet, ConvNeXt, MobileNet): accuracy/latency trade-offs, feature pyramid outputs, input resolution, BN handling when fine-tuning."
sources: ["https://arxiv.org/abs/1512.03385", "https://arxiv.org/abs/1905.11946", "https://huggingface.co/docs/timm/index", "https://pytorch.org/vision/stable/models.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CNN backbones (ResNet, EfficientNet)

## Families
| Backbone | Why use it | Watch out |
|---|---|---|
| ResNet-18/50 | Ubiquitous, well-supported in every runtime, robust to fine-tune | Not the most accurate per FLOP |
| EfficientNet B0-B7 / V2 | Compound scaling of depth/width/resolution; strong accuracy per FLOP | Depthwise convs + SiLU can be slow on some accelerators; train with its native resolution |
| ConvNeXt | Modern CNN competitive with ViTs | Heavier, LayerNorm |
| MobileNetV3 / EfficientNet-Lite | Mobile CPUs/NPUs | Lite variants drop SE/swish for quantisation friendliness |
| RegNet | Predictable GPU throughput | |

FLOPs are not latency: benchmark on the target device and runtime.

## Features for dense tasks
```python
m = timm.create_model("resnet50", pretrained=True, features_only=True, out_indices=(1, 2, 3, 4))
c2, c3, c4, c5 = m(x)          # strides 4, 8, 16, 32 -> FPN input
print(m.feature_info.channels())
```

## Resolution
EfficientNet-B0 is designed for 224, B3 for 300, B7 for 600. Feeding much smaller images wastes
the model; larger images help small objects but cost quadratically.

## BatchNorm when fine-tuning
- Small batches (< 8 per GPU) give noisy BN statistics: freeze BN (`model.eval()` for BN layers,
  or `timm.utils.freeze_batch_norm_2d`), use SyncBN across GPUs, or GroupNorm.
- Remember `model.eval()` at inference; forgetting it is a classic accuracy drop.

## Practical defaults
Start with ResNet-50 or ConvNeXt-T pretrained on ImageNet-21k/1k for servers; EfficientNet-Lite0
or MobileNetV3 for edge. Switch only if measurement shows the need.

## Verify
Profile latency (batch 1 and target batch) and accuracy on your validation set for 2 to 3
candidates before committing.

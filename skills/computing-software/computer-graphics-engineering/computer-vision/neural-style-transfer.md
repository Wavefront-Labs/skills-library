---
id: computing-software.computer-graphics-engineering.computer-vision.neural-style-transfer
name: neural-style-transfer
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, comp-photo-cv, style-transfer, gram-matrix, adain, vgg, image-stylization]
level: practitioner
status: draft
description: "Apply neural style transfer: Gatys optimisation with VGG Gram losses, fast feed-forward and AdaIN arbitrary-style networks, content/style weights, and video stability."
sources: ["https://arxiv.org/abs/1508.06576", "https://pytorch.org/tutorials/advanced/neural_style_tutorial.html", "https://arxiv.org/abs/1703.06868", "https://arxiv.org/abs/1603.08155"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Neural style transfer

## Optimisation-based (Gatys)
- Content loss: MSE between VGG-19 features (e.g. `conv4_2`) of output and content image.
- Style loss: MSE between Gram matrices `G = F F^T / (C H W)` at `conv1_1 .. conv5_1`.
- Optimise the output image directly (L-BFGS, initialised from the content image), total loss
  `alpha * content + beta * style + tv * total_variation`; beta/alpha around 1e4 to 1e6.
- Normalise inputs with ImageNet mean/std; replace max-pool with average pool for smoother results.
- Slow: tens of seconds to minutes per image on GPU. Best quality per image.

## Feed-forward
- **Per-style networks** (Johnson et al.): train a transform net with the perceptual loss on
  COCO; real-time inference, one model per style. OpenCV DNN can run the published `.t7` models
  (`samples/dnn/fast_neural_style.py`).
- **Arbitrary style (AdaIN)**: encoder (VGG) -> align channel mean/std of content features to the
  style features -> decoder. One model, any style, a style-strength blend parameter.

## Controls
- Preserve colour: transfer style on luminance only, keep content chrominance (YIQ/Lab).
- Resolution: style patterns scale with image size; run at the resolution where brush strokes look
  right, or multi-scale.
- Masks for spatial control (style only background).

## Video
Per-frame stylisation flickers. Add a temporal loss with optical flow warping of the previous output
(Ruder et al.) or use temporally consistent models.

## Verify
Side-by-side grid over style weights; for video, measure warping error between consecutive stylised
frames.

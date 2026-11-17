---
id: computing-software.ai-ml-engineering.model-training.self-supervised-and-contrastive-pretraining
name: self-supervised-and-contrastive-pretraining
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, self-supervised-learning, contrastive-learning, simclr, dinov2, masked-autoencoder, representation-learning]
level: practitioner
status: draft
description: "Pretrain representations on unlabelled data with self-supervised methods: SimCLR/MoCo contrastive, DINO-style distillation, masked autoencoders, and linear-probe evaluation."
sources:
  - https://arxiv.org/abs/2002.05709
  - https://arxiv.org/abs/2304.07193
  - https://github.com/lightly-ai/lightly
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Self-supervised and contrastive pretraining

When labels are scarce but unlabelled data is plentiful (medical images, industrial inspection, satellite data), pretrain an encoder on the unlabelled data, then fine-tune or linear-probe on the small labelled set.

## First check: do you need to pretrain?
Public self-supervised backbones (DINOv2, CLIP/SigLIP, MAE-pretrained ViTs via timm) often transfer well. Pretrain yourself only when your domain is far from natural images/text and you have a lot of unlabelled data (100k+ samples); otherwise continue pretraining a public model on your domain.

## Method families
| Family | Idea | Notes |
|---|---|---|
| Contrastive (SimCLR, MoCo v3) | two augmented views of the same image are positives; other images negatives; InfoNCE loss | needs large batches (SimCLR) or a queue/momentum encoder (MoCo) |
| Self-distillation (BYOL, DINO, DINOv2) | student matches a momentum teacher's output on different views; no negatives | strong features, robust to batch size |
| Masked modelling (MAE, BEiT; BERT for text) | reconstruct masked patches/tokens | scales well with ViTs; needs fine-tuning more than linear probe |
| Multimodal contrastive (CLIP) | image-text pairs | needs paired data |

## Contrastive loss (InfoNCE)
```python
def info_nce(z1, z2, t=0.1):
    z1, z2 = F.normalize(z1, dim=1), F.normalize(z2, dim=1)
    logits = z1 @ z2.T / t                      # (B, B); diagonal are positives
    labels = torch.arange(len(z1), device=z1.device)
    return (F.cross_entropy(logits, labels) + F.cross_entropy(logits.T, labels)) / 2
```
Components: strong augmentations (random resized crop, color jitter, blur) define what the representation is invariant to; projection head (MLP) used for the loss and discarded afterwards; temperature 0.05-0.2.

## Evaluation
- **Linear probe**: freeze encoder, train logistic regression on embeddings of the labelled set. Measures representation quality directly.
- **kNN accuracy** on embeddings: cheap monitoring during pretraining.
- **Fine-tuning** with few labels (1%, 10%) vs a supervised-from-scratch baseline: the number that matters for the project.

## Practical
- Libraries: lightly (PyTorch SSL methods), solo-learn, VISSL; DINOv2 training code from Meta.
- Augmentations must suit the domain: color jitter may destroy meaning in medical stains; rotations fine for satellite, not for text in images.
- Watch for collapse (all embeddings identical): monitor embedding standard deviation per dimension; BYOL/DINO rely on centering/sharpening and momentum to avoid it.
- Compute: SSL needs many epochs (hundreds) on large data; budget accordingly.

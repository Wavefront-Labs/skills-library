---
id: computing-software.computer-graphics-engineering.computer-vision.vision-dataset-splits-and-leakage
name: vision-dataset-splits-and-leakage
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, vision-datasets, cv-evaluation, dataset-splits, data-leakage, near-duplicate-detection, group-split, video-frame-leakage, test-set-hygiene, fiftyone]
level: practitioner
status: gated
description: "Split vision datasets so metrics predict production: group splits by video/site/subject, near-duplicate detection with embeddings, temporal splits, stratification."
sources: ["https://szeliski.org/Book/", "https://scikit-learn.org/stable/modules/cross_validation.html#group-k-fold", "https://docs.voxel51.com/brain.html#finding-duplicates", "https://arxiv.org/abs/1902.10811"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vision dataset splits and leakage

**Goal:** validation and test scores that hold up in deployment, not inflated by
near-identical images on both sides of the split.

## 1. Where leakage comes from
- **Video frames**: consecutive frames are near-duplicates; random frame-level splits put
  the same scene in train and test.
- Same physical object/person/patient/location photographed multiple times.
- Augmented copies or re-crops of the same image saved as separate files.
- Duplicates scraped from the web (same image, different resolution/compression).
- Test images used for threshold tuning or model selection repeatedly ("test set overfitting").

## 2. Group splits
Split by the unit you'll generalise across: video/session, camera/site, subject, day, product SKU.
```python
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=0)
train_idx, test_idx = next(gss.split(X, y, groups=df["video_id"]))
# class-balanced + grouped folds:
sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)
assert set(df["video_id"].iloc[train_idx]).isdisjoint(df["video_id"].iloc[test_idx])   # no group on both sides
```
Both splitters ran on 1,000 samples in 100 groups of 10 (3 classes assigned per group): zero shared groups in the
shuffle split and in all five stratified folds, with per-fold class counts such as (60, 70, 70).
**Temporal split** (train on earlier, test on later) when deployment sees future data —
catches drift (seasons, new products, camera changes).

## 3. Find near-duplicates
Compute embeddings (CLIP/DINOv2) or perceptual hashes (pHash) and flag pairs above a
similarity threshold across splits; then merge their groups.
```python
import fiftyone.brain as fob
fob.compute_similarity(dataset, brain_key="sim", model="clip-vit-base32-torch")
index = dataset.load_brain_results("sim"); index.find_duplicates(thresh=0.05)
```
The FiftyOne block was not run here (FiftyOne not installed) (gated: unconfirmed, source is paywalled or blocked).

## 4. Test set hygiene
- Freeze the test set (hash list in the repo); evaluate on it rarely — model selection uses
  validation.
- Keep hard slices (night, rain, small objects, rare classes) as tagged subsets and report per
  slice.
- Re-label audit: test labels get a second review — label noise in test caps measurable accuracy.

## 5. Sanity checks
- Train a model on train, evaluate on train vs val: a tiny gap with suspiciously high val can
  signal leakage.
- Shuffle labels test: performance should drop to chance.

## Gotchas
- "We'll split later" after augmentation/cropping → copies leak. Split first, then augment.
- Multiple annotations of the same image in different folders.
- Class stratification and grouping conflict — use StratifiedGroupKFold and check class counts.

## Verify
- [ ] Group key documented; no group appears in more than one split (assertion in pipeline).
- [ ] Cross-split near-duplicate scan run and resolved.
- [ ] Test set frozen with a manifest hash; per-slice metrics reported.

## Checked
scikit-learn 1.x (scratch venv), NumPy 2.5.4.
- Run: `GroupShuffleSplit` and `StratifiedGroupKFold` on grouped synthetic data with a disjointness assertion.
- Fetched: the arXiv API title for 1902.10811 (Do ImageNet Classifiers Generalize to ImageNet?).
- Not run: FiftyOne brain duplicate search (not installed); gated.

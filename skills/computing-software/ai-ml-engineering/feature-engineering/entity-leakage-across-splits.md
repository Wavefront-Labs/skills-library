---
id: computing-software.ai-ml-engineering.feature-engineering.entity-leakage-across-splits
name: entity-leakage-across-splits
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, data-leakage, entity-leakage, group-split, groupkfold, patient-level-split, cold-start-evaluation]
level: practitioner
status: draft
description: "Prevent the same users, patients, devices or documents from appearing in both train and test: group splits, overlap checks, fuzzy entity matching and cold-start evaluation."
sources:
  - https://scikit-learn.org/stable/modules/cross_validation.html#group-k-fold
  - https://www.nature.com/articles/s41746-020-00318-y
  - https://scikit-learn.org/stable/common_pitfalls.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entity leakage across splits

**Goal:** test performance reflects new entities, not memorised ones.

## The problem
Many datasets have several rows per entity: visits per patient, sessions per user, frames per video, sentences per document, transactions per card. Random row splits put the same entity on both sides. The model learns entity identity (a patient's typical lab values, a speaker's voice) and scores well on test for the wrong reason. In medical imaging, image-level splits of multi-image patients are a known source of inflated results.

## Group splits
```python
from sklearn.model_selection import GroupShuffleSplit, GroupKFold, StratifiedGroupKFold
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=0)
tr, te = next(gss.split(X, y, groups=df.patient_id))
assert not set(df.patient_id.iloc[tr]) & set(df.patient_id.iloc[te])
cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)
```
Use the same groups in hyperparameter search CV (pass `groups=`, or route them with metadata routing).

## Finding the real entity
The obvious ID is not always the entity:
- Same person with multiple accounts, same household, same device.
- Same document in different formats/translations.
- Augmented copies of one source image.
Fuzzy-match entities (name + DOB, device fingerprint, near-duplicate content) and assign a cluster ID for grouping.

## Which split matches deployment
- Model serves **new** entities (new patients, new users): group split.
- Model serves **known** entities in the future (next purchase of existing customers): time split, where the same entity can appear on both sides but only past -> future. Group split here would understate performance.
- Recommenders: evaluate warm (known users/items) and cold-start (unseen) separately.

## Verify
- [ ] Entity overlap between train and test is zero (or deliberate, for temporal setups).
- [ ] Score gap between row-split and group-split reported - a big gap confirms the leak existed.
- [ ] Split choice documented against how the model is used.

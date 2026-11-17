---
id: computing-software.ai-ml-engineering.model-training.near-duplicate-and-contamination-checks
name: near-duplicate-and-contamination-checks
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, data-splits, train-test-contamination, near-duplicate-detection, minhash, deduplication, benchmark-contamination]
level: practitioner
status: draft
description: "Find exact and near-duplicate examples shared across train/val/test (MinHash, perceptual hashes, embeddings, n-gram overlap) before trusting any evaluation number."
sources:
  - https://ekzhu.com/datasketch/lsh.html
  - https://arxiv.org/abs/2107.06499
  - https://arxiv.org/abs/2005.14165
  - https://github.com/JohannesBuchner/imagehash
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Near-duplicate and contamination checks across splits

**Goal:** make sure test performance is not inflated by test items that also appear (nearly) verbatim in training data.

## Why it matters
Scraped and user-generated datasets routinely contain duplicates: reposted images, templated text, the same customer with tiny edits. A random split then puts copies on both sides, and the model is graded on memorised items. Lee et al. (2021) found large fractions of near-duplicates in common LM corpora and that removing them changes measured performance.

## Exact duplicates first
Normalise (lowercase, strip whitespace/punctuation, canonical JSON key order, decode images to pixels) and hash:
```python
df["h"] = df.text.str.lower().str.replace(r"\W+", " ", regex=True).str.strip().map(lambda s: hashlib.sha1(s.encode()).hexdigest())
overlap = set(train.h) & set(test.h)
```

## Near-duplicates
- **Text - MinHash LSH** (`datasketch`): shingle into word 5-grams, `MinHash(num_perm=128)`, index train in `MinHashLSH(threshold=0.8)`, query each test item. Jaccard >= 0.8 is a typical near-dup threshold.
- **Images - perceptual hashing** (`imagehash.phash`): Hamming distance <= 4-8 bits on 64-bit hashes flags resized/recompressed copies.
- **Anything - embeddings**: embed with a sentence/image encoder, find nearest train neighbour per test item with FAISS; inspect pairs above cosine ~0.95 and pick a threshold by eye.
- **LLM benchmark contamination**: n-gram overlap between eval items and pretraining/fine-tuning data (GPT-3 used 13-gram overlap); also test with perturbed versions of items - a big drop suggests memorisation.

## What to do with them
- Remove test items that have a near-duplicate in train (report how many), or regroup: cluster near-duplicates and split by cluster with `GroupShuffleSplit`/`GroupKFold`, so the whole cluster lands on one side.
- Deduplicate within train too: duplicates over-weight some examples and skew the learned prior.
- Re-report metrics on the "clean" test subset alongside the original to show the size of the effect.

## Gotchas
- Thresholds are data-specific; sample 50 flagged pairs and label them to estimate precision before deleting anything.
- Boilerplate (licence headers, email signatures) creates false near-dup matches; strip it before shingling.
- Duplicates by entity (same patient, same user) are a group-split problem, not a content-similarity problem; handle both.

## Verify
- [ ] Exact and near-duplicate overlap counts between splits reported.
- [ ] Threshold validated on a labelled sample of pairs.
- [ ] Metrics re-computed on the deduplicated test set.

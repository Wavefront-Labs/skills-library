---
id: computing-software.ai-ml-engineering.hugging-face.dataset-splitting-shuffle-interleave
name: dataset-splitting-shuffle-interleave
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, hf-datasets, interleave-datasets, train-test-split, shuffle, flatten-indices, concatenate-datasets]
level: practitioner
status: verified
description: "Split, shuffle and mix Hugging Face datasets: stratified train_test_split, the shuffle/flatten_indices speed trap, select/shard, concatenate vs interleave."
sources:
  - https://huggingface.co/docs/datasets/main/en/process
  - https://huggingface.co/docs/datasets/main/en/stream#interleave
  - https://huggingface.co/docs/datasets/main/en/package_reference/main_classes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Splitting, shuffling and mixing datasets

## Splits
```python
splits = ds.train_test_split(test_size=0.1, seed=42, stratify_by_column="label")  # label must be a ClassLabel column; a plain Value column raises ValueError
train, val = splits["train"], splits["test"]
```
Three-way split: split twice. For group-aware splits (users, documents) compute split membership from a hash of the group id with `filter`.

## Shuffle and the indices mapping
`ds.shuffle(seed=42)` creates an indices mapping instead of rewriting data; subsequent reads become random-access and can be up to 10x slower. Fix with `ds = ds.shuffle(seed=42).flatten_indices()` (rewrites contiguously), or for training rely on the DataLoader's shuffling of the original dataset.

Streaming: `ids.shuffle(seed=42, buffer_size=10_000)` uses a buffer (approximate shuffle); also shuffles shard order. Call `ids.set_epoch(epoch)` for a new order each epoch.

## Subsets
`ds.select(range(1000))`, `ds.shard(num_shards=8, index=rank, contiguous=True)` for manual data parallel splits, `ds.filter(fn, num_proc=8)`.

## Combine
```python
from datasets import concatenate_datasets, interleave_datasets
both = concatenate_datasets([ds_a, ds_b])                  # same features; rows appended
mix = interleave_datasets([web, code, math], probabilities=[0.6, 0.3, 0.1], seed=0,
                          stopping_strategy="all_exhausted")
```
- `stopping_strategy="first_exhausted"` (default) stops when the smallest source runs out (under-samples others); `"all_exhausted"` oversamples small sources until all are seen; `"all_exhausted_without_replacement"` shows every sample exactly once (datasets 5.1: sources of 3 and 2 rows give 5 rows).
- Features must match: `cast` columns or `select_columns` first.
- Works for streaming IterableDatasets too: the standard way to build pretraining/SFT data mixtures.

## Verify
- [ ] Label distribution per split printed; no id overlap between splits.
- [ ] For mixtures, count samples per source over the first N rows and compare to the probabilities.

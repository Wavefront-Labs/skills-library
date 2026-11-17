---
id: computing-software.ai-ml-engineering.hugging-face.load-dataset-local-hub-and-splits
name: load-dataset-local-hub-and-splits
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, datasets, load-dataset, data-files, split-slicing, dataset-cache, parquet]
level: practitioner
status: verified
description: "Load datasets with load_dataset from local CSV/JSON/Parquet/image folders and the Hub: data_files mapping, split slicing, revisions, cache location and common errors."
sources:
  - https://huggingface.co/docs/datasets/loading
  - https://huggingface.co/learn/llm-course/chapter5/2
  - https://huggingface.co/docs/datasets/cache
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# load_dataset from local files and the Hub

**Goal:** get any dataset into a `Dataset`/`DatasetDict` reproducibly, with control over splits and caching.

## Local files
```python
from datasets import load_dataset
ds = load_dataset("csv", data_files={"train": "data/train.csv", "test": "data/test.csv"})
ds = load_dataset("json", data_files="data/*.jsonl", split="train")            # globs work
ds = load_dataset("json", data_files="nested.json", field="data")               # records under a key
ds = load_dataset("parquet", data_files={"train": "s3://bucket/train/*.parquet"}, storage_options={...})
ds = load_dataset("imagefolder", data_dir="images/")    # class-per-folder -> label column
ds = load_dataset("audiofolder", data_dir="clips/")
```
Compressed files are handled transparently (a `.csv.gz` loaded in datasets 5.1 with no extra arguments).

## From the Hub
```python
ds = load_dataset("rajpurkar/squad", split="train", revision="<commit-sha>")   # pin for reproducibility
ds = load_dataset("allenai/c4", "en", split="validation", streaming=True)      # config name + streaming
```
- Private/gated datasets need `hf auth login` (the `huggingface-cli` command no longer ships with huggingface_hub 2.x) or `HF_TOKEN`.
- Recent `datasets` releases no longer run dataset loading scripts (datasets 5.1 raises `RuntimeError: Dataset scripts are no longer supported`); datasets must be in data formats (Parquet, JSON, CSV...). Use the Hub's auto-converted Parquet branch (`revision="refs/convert/parquet"`) for older script-based datasets.

## Split slicing
```python
load_dataset("imdb", split="train[:10%]")
load_dataset("imdb", split="train[:2000]+test[:500]")
load_dataset("imdb", split=[f"train[{k}%:{k+20}%]" for k in range(0, 100, 20)])   # 5 slices
```
For a validation split you create: `ds["train"].train_test_split(test_size=0.1, seed=42, stratify_by_column="label")` (stratify needs a `ClassLabel` column).

## Cache
Downloaded and prepared data goes to `~/.cache/huggingface/datasets` (override with `HF_DATASETS_CACHE` or `cache_dir=`). Processed results of `map` are cached too, keyed by function fingerprint.
- `download_mode="force_redownload"` after the source changed.
- Shared filesystems: point every job at the same cache directory to avoid N copies.

## Gotchas
- CSV type inference works chunk by chunk; a column that is int in the first chunk and string later fails (checked: 200,000 int rows then `abc` raised `ArrowInvalid: Failed to parse string: 'abc' as a scalar of type int64`, wrapped in `DatasetGenerationError`; on Windows a `PermissionError` from the cleanup can be shown on top, read the chained cause). Pass `features=` explicitly (with `Value("string")` it loads).
- `load_dataset` on local CSV/JSON converts to Arrow once and caches it; Parquet input is already columnar, so it is the better interchange format for large files.

## Verify
- [ ] Revision/commit pinned for Hub datasets.
- [ ] Features (`ds.features`) correct types, labels as `ClassLabel`.
- [ ] Split sizes logged.

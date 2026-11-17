---
id: computing-software.ai-ml-engineering.hugging-face.datasets-arrow-cache-and-save-to-disk
name: datasets-arrow-cache-and-save-to-disk
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, hf-datasets, save-to-disk, arrow-cache, memory-mapping, cache-files, load-from-disk]
level: practitioner
status: verified
description: "Manage Datasets' Arrow storage: memory-mapped cache files, fingerprint-based map caching, cache_dir and cleanup, save_to_disk/load_from_disk and sharded Parquet export."
sources:
  - https://huggingface.co/docs/datasets/main/en/about_cache
  - https://huggingface.co/docs/datasets/main/en/about_arrow
  - https://huggingface.co/docs/datasets/main/en/process#save
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Arrow cache, save_to_disk and memory mapping

## How storage works
- Datasets are Arrow tables memory-mapped from disk: a 200GB dataset can be iterated with little RAM.
- Each `map`/`filter` writes a new Arrow cache file named by a **fingerprint** (hash of the previous fingerprint + function + arguments). Re-running the same code reuses the cache.

## Cache control
- Location: `HF_DATASETS_CACHE` (default `~/.cache/huggingface/datasets`) or `load_dataset(..., cache_dir=...)`.
- Force recompute: `ds.map(fn, load_from_cache_file=False)`.
- Explicit cache path: `ds.map(fn, cache_file_name="/data/cache/tok.arrow")`.
- Disable globally: `datasets.disable_caching()` (transforms then go to temporary files deleted at session end).
- Clean: `ds.cleanup_cache_files()` removes cache files not used by the current dataset and returns how many it removed. Only datasets backed by files (for example from `load_from_disk`) have `ds.cache_files`; a dataset built in memory with `from_dict` returns an empty list even after `map`.
- Hashing failures (`Parameter 'function' ... couldn't be hashed properly`) mean random fingerprints and no reuse; avoid capturing unpicklable objects (tokenizers usually hash fine; open file handles do not).

## Persisting processed datasets
```python
ds.save_to_disk("/data/processed/tokenized", num_shards={"train": 64})
from datasets import load_from_disk
ds = load_from_disk("/data/processed/tokenized")          # memory-mapped, instant
```
- `save_to_disk` writes Arrow shards + state; good for the same library version and fast reload.
- For interchange and the Hub, write Parquet: `ds.to_parquet("train.parquet")` or `push_to_hub` (auto-sharded Parquet).
- Object storage: pass `storage_options` / fsspec URLs (`s3://...`) to `save_to_disk`/`load_from_disk`.

## Memory gotchas
- `ds.to_pandas()` or `ds["text"]` loads the whole column into RAM; slice or iterate instead.
- `keep_in_memory=True` disables memory mapping; only for small data.
- `num_proc` in `map` writes one cache file per process, then concatenates.

## Verify
- [ ] Second run of the preprocessing script prints "Loading cached processed dataset".
- [ ] `ds.cache_files` points at the expected disk.

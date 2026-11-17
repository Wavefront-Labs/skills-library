---
id: computing-software.ai-ml-engineering.hugging-face.creating-and-pushing-datasets-to-the-hub
name: creating-and-pushing-datasets-to-the-hub
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, datasets, push-dataset, push-to-hub, dataset-card, classlabel, parquet-shards]
level: practitioner
status: docs-checked
description: "Build a Dataset from pandas, dicts or generators, set features and ClassLabels, push it to the Hub with configs and splits, and write a useful dataset card."
sources:
  - https://huggingface.co/docs/datasets/upload_dataset
  - https://huggingface.co/docs/datasets/create_dataset
  - https://huggingface.co/docs/hub/datasets-cards
  - https://huggingface.co/docs/hub/datasets-manual-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating and pushing datasets to the Hub

**Goal:** share a dataset (privately or publicly) in a form `load_dataset("org/name")` loads with correct types, splits and documentation.

## Build it
```python
from datasets import Dataset
# large data without loading into memory (the most memory-efficient way to build a dataset;
# it is generated on disk progressively and memory-mapped):
gen_ds = Dataset.from_generator(lambda: iter_records("raw/"))
```
Define explicit `features` (including `ClassLabel` for categorical labels) so types are not guessed; see the create-a-dataset guide.

## Push
```python
from datasets import load_dataset
dataset = load_dataset("stevhliu/demo")
dataset.push_to_hub("stevhliu/processed_demo")
dataset.push_to_hub("stevhliu/private_processed_demo", private=True)
```
- Log in first (`huggingface-cli login`) with the `huggingface_hub` library installed.
- `private=True` only works when the repository is created for the first time.
- To add a configuration (subset) or a new split (train/validation/test), see the `Dataset.push_to_hub()` reference.
- Load a private dataset with `load_dataset("org/name", token=True)`.
- A repository keeps its revision history, so more than one dataset version can be stored.

Alternatively upload files you already have through the web UI (Files and versions tab, Add file) or `huggingface_hub`. Text files (`.csv`, `.json`, `.jsonl`, `.txt`) are not tracked by Git LFS by default and are not committed if larger than 10MB; compress them (`.zip`, `.gz`) and check `.gitattributes` for tracked extensions.

Splits and configurations can be declared in the README YAML:
```yaml
configs:
- config_name: default
  data_files:
  - split: train
    path: "data/train-*.parquet"
  - split: test
    path: "data/test-*.parquet"
```
`config_name` is required even for a single subset. `data_dir` points to a directory whose files are resolved by extension.

## Dataset card (README.md)
The card is the repository README.md. Its YAML header carries metadata such as `license`, `language`, `task_categories` and `pretty_name`. Body: source and collection process, annotation guidelines, intended uses and known biases, personal data handling, splits and how they were made, citation. Teams forget the split methodology most often, and it decides whether others can trust benchmark numbers.

## Gotchas
- Personal data: scrub before pushing; repositories keep history.

## Verify
- [ ] `load_dataset("org/name")` in a fresh environment returns the expected splits and features.
- [ ] Dataset viewer renders.
- [ ] Card documents source, license, splits and limitations.

## Checked
2026-11-01. Confirmed against the Datasets "Share a dataset to the Hub" and "Create a dataset" guides and the Hub dataset-cards and manual-configuration pages: `push_to_hub`, `private=True` first-creation only, `token=True`, `huggingface-cli login`, `from_generator` memory behaviour, the 10MB text and Git LFS note, `configs`/`config_name`/`data_files`/`split` YAML, `data_dir`, card metadata fields. Removed (not found on the pages): `max_shard_size`, `commit_message=`, `revision=`, Parquet shards under `data/`, `stratify_by_column`, `size_categories`, `super_squash_history`, `Image()`/`Audio()` embedding, gated-access menu path, `from_pandas` example.
Method: documentation only; no commands were run.

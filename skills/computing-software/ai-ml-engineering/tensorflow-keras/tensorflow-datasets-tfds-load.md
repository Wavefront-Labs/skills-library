---
id: computing-software.ai-ml-engineering.tensorflow-keras.tensorflow-datasets-tfds-load
name: tensorflow-datasets-tfds-load
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, tfds, tensorflow-datasets, tf-data, dataset-splits, data-dir]
level: practitioner
status: docs-checked
description: "Load and prepare datasets with tfds.load: split slicing, as_supervised, with_info, data_dir and GCS caching, manual downloads, determinism and building a custom dataset."
sources:
  - https://www.tensorflow.org/datasets/overview
  - https://www.tensorflow.org/datasets/splits
  - https://www.tensorflow.org/datasets/determinism
  - https://www.tensorflow.org/datasets/data_source
  - https://www.tensorflow.org/datasets/add_dataset
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TensorFlow Datasets (tfds.load)

**Goal:** get a ready tf.data pipeline for a public or custom dataset with correct splits.

## Load
```python
import tensorflow_datasets as tfds
(train, val), info = tfds.load(
    "imdb_reviews",
    split=["train[:90%]", "train[90%:]"],     # slicing API
    as_supervised=True,                        # (features, label) tuples instead of dicts
    with_info=True,
    shuffle_files=True,
    data_dir="gs://my-bucket/tfds",            # or local path; default ~/tensorflow_datasets
)
print(info.features, info.splits["train"].num_examples)
```
Split syntax: `"train[:1000]"`, `"train[25%:50%]"`, `"train+test"`, cross-validation folds via `tfds.even_splits("train", n=5)` or percent slices.

## Pipeline after loading
```python
train = (train.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
              .cache().shuffle(10_000).batch(64).prefetch(tf.data.AUTOTUNE))
```

## Determinism
With the default `shuffle_files=False` TFDS reads examples in a deterministic order. `shuffle_files=True` shuffles the shards for each epoch and makes reading non-deterministic. For a reproducible shuffle pass `shuffle_files=True` with `read_config=tfds.ReadConfig(shuffle_seed=32)`, and change the seed every epoch, otherwise the shards are read in the same order each epoch.

## Manual / gated datasets
Some datasets (ImageNet) need archives downloaded manually into the manual directory, which defaults to `<download_dir>/manual` (under the default data directory this is `~/tensorflow_datasets/downloads/manual`); builders can supply instructions for what to place there.

## Outside TensorFlow
`tfds.as_numpy(ds)` yields NumPy. `tfds.data_source("fashion_mnist")` creates random-access data sources (ArrayRecord files, via the `array_record` package) for JAX and PyTorch pipelines without tf.data.

## Custom dataset
`tfds new my_dataset` scaffolds a builder (`_info`, `_split_generators`, `_generate_examples`); `tfds build` downloads and prepares the dataset into `~/tensorflow_datasets/`.

## Verify
- [ ] Split sizes from `info.splits` match expectations and train/val slices do not overlap.
- [ ] Inspect a few examples with `tfds.as_dataframe(ds.take(5), info)`.

## Checked

Checked 2026-10-25 against tensorflow/datasets master (docs of 2026-10-19). Confirmed `tfds.load` options (`split` lists and slices, `as_supervised`, `with_info`, `shuffle_files`, `data_dir` with default `~/tensorflow_datasets/`), the percent, absolute and union split syntax, `tfds.even_splits` and cross-validation folds (splits guide), deterministic reading and `ReadConfig(shuffle_seed=...)` (determinism guide), `tfds.as_numpy`, `tfds.as_dataframe`, `tfds.data_source` with ArrayRecord (data source guide), `tfds new` and `tfds build` (add dataset guide), and the manual directory default (`download_manager.py`). Removed the `deterministic=True` advice, `tfds.show_examples` and the cache-ordering remark.

Method: documentation only; no commands were run.

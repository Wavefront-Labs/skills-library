---
id: computing-software.ai-ml-engineering.tensorflow-keras.tf-data-dataset-sources
name: tf-data-dataset-sources
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, tf-data, from-tensor-slices, from-generator, list-files, tfrecord, dataset-sources]
level: practitioner
status: gated
description: "Create tf.data pipelines from the right source: from_tensor_slices, from_generator with output_signature, list_files plus TFRecordDataset, and text/CSV readers."
sources:
  - https://www.tensorflow.org/guide/data#reading_input_data
  - https://www.tensorflow.org/api_docs/python/tf/data/Dataset#from_generator
  - https://www.tensorflow.org/tutorials/load_data/tfrecord
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tf.data dataset sources

## In-memory arrays: from_tensor_slices
```python
ds = tf.data.Dataset.from_tensor_slices((features, labels))      # slices along axis 0
ds = tf.data.Dataset.from_tensor_slices(dict(df))                # pandas columns -> dict of features
```
- The tf.data guide says this embeds the arrays as `tf.constant()` ops, wastes memory (the contents are copied several times) and can hit the 2 GB `tf.GraphDef` protocol buffer limit. For large arrays, save to TFRecord or use `from_generator`/NumPy memmap.
- `from_tensors(x)` gives a single element (no slicing); a common mistake when you meant slices (ran: cardinality 1 vs 10 for a (10, 1) array; the dict-of-columns form gave `{'a': int64, 'b': float64}` specs).

## Python generators: from_generator
```python
def gen():
    for path, y in index:
        yield load(path), y
ds = tf.data.Dataset.from_generator(gen, output_signature=(
        tf.TensorSpec(shape=(None, None, 3), dtype=tf.uint8),
        tf.TensorSpec(shape=(), dtype=tf.int32)))
```
- The tf.data guide cautions that it must run in the same Python process that created the generator and is subject to the GIL, so it is often the bottleneck. Better: make the generator yield only paths/ids and do loading in `map(tf_load, num_parallel_calls=AUTOTUNE)` with TF ops or `tf.numpy_function`.
- `output_signature` is the current argument; the 2.21 signature is `from_generator(generator, output_types=None, output_shapes=None, args=None, output_signature=None, name=None)` (ran with variable-length uint8 arrays: shapes `(2,2,3)`, `(3,2,3)`, `(4,2,3)`).
- Iterator checkpointing fails for it (see the snapshot skill: `FailedPreconditionError: PyFunc is stateful`).

## Files: list_files, interleave, readers
```python
files = tf.data.Dataset.list_files("gs://bucket/train-*.tfrecord", shuffle=True, seed=42)
ds = files.interleave(lambda f: tf.data.TFRecordDataset(f, compression_type="GZIP"),
                      cycle_length=16, num_parallel_calls=tf.data.AUTOTUNE, deterministic=False)
ds = ds.map(parse_example, num_parallel_calls=tf.data.AUTOTUNE)
```
- `list_files` shuffles by default and reshuffles on each pass (ran with 4 files: two passes gave different orders; `shuffle=False` gave `train-0..3` in order); set `shuffle=False` for evaluation reproducibility.
- Images on disk: `list_files("data/*/*.jpg")` then `tf.io.read_file` + `tf.io.decode_jpeg` in map; or `keras.utils.image_dataset_from_directory` which does this with labels from folder names.
- Text: `tf.data.TextLineDataset(files)`; CSV: `tf.data.experimental.make_csv_dataset(pattern, batch_size, label_name="y")`.
- Other: `tf.data.Dataset.range`, `zip`, `sample_from_datasets` (mixing), `tf.data.Dataset.load` (saved datasets); `make_csv_dataset`, `Dataset.load`, `sample_from_datasets`, `Dataset.snapshot` and `keras.utils.image_dataset_from_directory` all exist in TF 2.21 / Keras 3.15 (checked with `hasattr`; the CSV and image-folder readers were not run). (gated: unconfirmed, source is paywalled or blocked)

## Choosing
| Data | Source |
|---|---|
| Small NumPy/pandas | from_tensor_slices |
| Many image files | list_files + map, or image_dataset_from_directory |
| Large training corpus | TFRecord shards + interleave |
| Custom format with Python reader | from_generator of ids + parallel map |
| Public datasets | TFDS `tfds.load` (needs downloads, not run here) |

## Verify
`for x, y in ds.take(2): print(x.shape, x.dtype, y)` and check `ds.element_spec` matches the model input.

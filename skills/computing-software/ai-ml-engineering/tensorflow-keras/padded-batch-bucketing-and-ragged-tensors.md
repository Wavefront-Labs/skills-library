---
id: computing-software.ai-ml-engineering.tensorflow-keras.padded-batch-bucketing-and-ragged-tensors
name: padded-batch-bucketing-and-ragged-tensors
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, tf-data, padded-batch, ragged-tensors, bucket-by-sequence-length, variable-length-sequences]
level: practitioner
status: gated
description: "Batch variable-length examples in tf.data: padded_batch with padded_shapes, bucket_by_sequence_length to cut padding waste, ragged_batch and RaggedTensor handling."
sources:
  - https://www.tensorflow.org/api_docs/python/tf/data/Dataset#padded_batch
  - https://www.tensorflow.org/api_docs/python/tf/data/Dataset#bucket_by_sequence_length
  - https://www.tensorflow.org/guide/ragged_tensor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# padded_batch, bucketing and ragged tensors

**Goal:** batch sequences of different lengths without wasting most compute on padding.

## padded_batch
```python
import tensorflow as tf
ds = tf.data.Dataset.from_generator(gen, output_signature=(
    tf.TensorSpec([None], tf.int32), tf.TensorSpec([], tf.int32)))
ds = ds.padded_batch(32, padded_shapes=([None], []), padding_values=(0, 0), drop_remainder=True)
```
- `padded_shapes=[None]` pads to the longest in the batch (ran on 200 random sequences of length 1-299: batch shapes `(32, 291)`, `(32, 299)`); `[128]` pads to a fixed length and fails on longer elements, so truncate first with `map(lambda x, y: (x[:128], y))` (ran: shapes `(32, 128)`). Fixed shapes are what static-shape compilers such as XLA want.

## Bucketing by length
```python
ds = ds.bucket_by_sequence_length(
    element_length_func=lambda x, y: tf.shape(x)[0],
    bucket_boundaries=[32, 64, 128, 256],
    bucket_batch_sizes=[128, 64, 32, 16, 8],   # len(boundaries) + 1 entries
    pad_to_bucket_boundary=False, drop_remainder=True)
```
Similar-length examples batch together. Ran on the same data: the fraction of padding positions fell from 0.457 with plain `padded_batch(32)` to 0.174 with the call above. `len(bucket_batch_sizes)` must equal `len(bucket_boundaries) + 1` (ran: otherwise `ValueError`). A bucket holds lengths below its boundary, and the last bucket takes everything above the final boundary. Shuffle before bucketing (with a large buffer) to keep randomness.

`pad_to_bucket_boundary=True` pads each bucket to `boundary - 1` (ran: batch widths `[127, 255]`) so each bucket has one static shape, but then every element must be shorter than the last boundary: with lengths up to 299 and last boundary 256 the pipeline failed with an `InvalidArgumentError` from an `assert_less` inside `group_by_window`. Truncate or filter to `length < bucket_boundaries[-1]` first.

## Ragged tensors
```python
ds = ds.ragged_batch(32)                     # yields tf.RaggedTensor batches
x = batch.to_tensor(default_value=0)         # densify when a layer needs it
mask = tf.sequence_mask(batch.row_lengths())
```
Ran: `ragged_batch(32)` gave a `RaggedTensor` of shape `(32, None)`, `to_tensor` and `sequence_mask` both gave `(32, 291)`; `Embedding` accepted the ragged batch and returned a `RaggedTensor`, while `Dense` raised `ValueError` (`TypeError: object of type 'RaggedTensor' has no len()`), so densify with `to_tensor()` before dense layers. Ragged support on the JAX/PyTorch backends was not tested. (gated: unconfirmed, source is paywalled or blocked)

## Verify
- [ ] Measure padding ratio: `1 - real_tokens / (batch * padded_len)` before and after bucketing.
- [ ] `ds.element_spec` shows the expected shapes (padded dims `None`); under XLA, no recompiles per step (check logs).

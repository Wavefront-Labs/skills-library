---
id: computing-software.ai-ml-engineering.tensorflow-keras.backend-agnostic-input-pipelines
name: backend-agnostic-input-pipelines
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, backend-agnostic-input, keras-3, tf-data, pytorch-dataloader, grain, keras-pydataset]
level: practitioner
status: docs-checked
description: "Feed Keras 3 models on JAX, TensorFlow or PyTorch backends from tf.data, torch DataLoader, Grain or keras.utils.PyDataset, with each option's performance and pitfalls."
sources:
  - https://keras.io/keras_3/
  - https://keras.io/getting_started/
  - https://keras.io/api/utils/python_utils/#pydataset-class
  - https://github.com/keras-team/keras/blob/master/keras/src/trainers/data_adapters/__init__.py
  - https://github.com/keras-team/keras/blob/master/keras/src/trainers/data_adapters/py_dataset_adapter.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backend-agnostic input pipelines (Keras 3)

`model.fit()` in Keras 3 accepts several input types regardless of backend:
- NumPy arrays / backend tensors
- `tf.data.Dataset`
- `torch.utils.data.DataLoader`
- `keras.utils.PyDataset`
- Grain datasets (`grain.Dataset` and `grain.DataLoader`)

## Choosing
| Input | Good with | Notes |
|---|---|---|
| `tf.data` | any backend | a tf.data pipeline that does not use Keras layers feeds `fit`, `evaluate` and `predict` on all backends; TensorFlow must be installed; TensorFlow maps nearly all GPU memory by default, so set memory growth if it shares a GPU with another framework |
| torch `DataLoader` | any backend | accepted by `fit`/`evaluate`/`predict`; targets and sample weights must come from the loader (`y`, `sample_weight` and `class_weight` arguments are rejected) |
| `PyDataset` | custom Python batch loading | subclass with `__len__` and `__getitem__` returning one batch per index; constructor arguments `workers` (default 1), `use_multiprocessing` (default False), `max_queue_size` (default 10) |
| Grain | any backend | `grain.Dataset` and `grain.DataLoader` objects are accepted; `y`, `sample_weight` and `class_weight` arguments are rejected |

## PyDataset
```python
class Batches(keras.utils.PyDataset):
    def __init__(self, paths, labels, bs, **kw):
        super().__init__(**kw); self.p, self.y, self.bs = paths, labels, bs
    def __len__(self): return math.ceil(len(self.p) / self.bs)
    def __getitem__(self, i):
        s = slice(i * self.bs, (i + 1) * self.bs)
        return np.stack([load(p) for p in self.p[s]]), self.y[s]
model.fit(Batches(paths, labels, 64, workers=8, use_multiprocessing=True, max_queue_size=16), epochs=5)
```
Shuffle by permuting indices in `on_epoch_end`.

## Preprocessing layers on non-TF backends
With a non-TensorFlow backend Keras 3 has limited support for `tf.data`: you cannot `.map()` arbitrary layers or models into a pipeline, but specific preprocessing layers such as `IntegerLookup` and `CategoryEncoding` can be used with it (Keras 3 FAQ).

## Pitfalls
- Mixing frameworks: TensorFlow maps nearly all memory of every visible GPU by default; call `tf.config.experimental.set_memory_growth` before any TF op when TF is only used for data.
- Distribution: `keras.distribution` classes take `auto_shard_dataset` (default True), which shards the dataset among processes in a multi-process setting.

## Verify
Time an epoch of the loader alone; confirm steps/epoch (`len(loader)`) and that the last partial batch is handled as intended (drop or keep).

## Checked

Checked 2026-10-25 against Keras 3 (keras-team/keras master of 2026-10-23, keras-io of 2026-09-23). Confirmed the accepted input types and the rejected y, sample_weight and class_weight arguments for DataLoader and Grain inputs (data_adapters source), the PyDataset constructor arguments and defaults, the Keras 3 FAQ on tf.data with non-TensorFlow backends, `auto_shard_dataset` in `keras.distribution`, and TensorFlow's default GPU memory behaviour (TensorFlow GPU guide). Removed unconfirmed performance rankings, the Grain recommendation, the torch pre-allocation claim and the `distribute_dataset` call.

Method: documentation only; no commands were run.

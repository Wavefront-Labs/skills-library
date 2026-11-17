---
id: computing-software.ai-ml-engineering.ray.data-map-batches
name: data-map-batches
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, map-batches, ray-data-transform, compute-strategy, batch-format]
level: practitioner
status: docs-checked
description: "Transform Ray Data with map, map_batches and flat_map: function vs class UDFs, batch_size, batch_format, compute strategy, GPUs."
sources:
  - https://docs.ray.io/en/latest/data/transforming-data.html
  - https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.map_batches.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# map_batches transforms

```python
import ray

def normalize(batch: dict) -> dict:               # default batch_format: dict of numpy arrays
    batch["x"] = (batch["x"] - batch["x"].mean()) / batch["x"].std()
    return batch

ds = ds.map_batches(normalize, batch_size=1024)

class Embedder:                                   # callable class: stateful, one instance per actor
    def __init__(self): self.m = load_model().cuda()    # load_model is your own
    def __call__(self, batch):
        batch["emb"] = self.m.encode(batch["text"].tolist()); return batch

ds = ds.map_batches(Embedder, compute=ray.data.ActorPoolStrategy(size=4),
                    num_gpus=1, batch_size=64, batch_format="pandas")
```

## Facts from the docs and API source
- Functions run as stateless tasks; callable classes run as actors, `__init__` called once per worker, so put expensive setup (model weights) there.
- `compute`: functions default to `TaskPoolStrategy()` (cap with `TaskPoolStrategy(size=n)`). Classes default to an autoscaling `ActorPoolStrategy(min_size=1, max_size=None)`; use `ActorPoolStrategy(size=n)` for a fixed pool or `(min_size=m, max_size=n)` to autoscale. The `concurrency` argument is deprecated in favour of `compute`.
- `batch_format`: `"default"`/`"numpy"` gives `Dict[str, numpy.ndarray]`, `"pandas"` a DataFrame, `"pyarrow"` a `pyarrow.Table`. UDFs may also be generators yielding batches.
- `batch_size` defaults to None (whole blocks); `"auto"` picks a size. With `num_gpus` set, `batch_size` must be an explicit integer. Larger batches speed vectorised work and inference but can OOM.
- `zero_copy_batch=True` (default) can give read-only views; set `False` (or copy only what you modify) to mutate in place.
- Resources per worker: `num_cpus`, `num_gpus`, `memory`, `resources`; `num_cpus` and `num_gpus` accept fractions.
- `map` (row-wise) and `flat_map` also exist; row-wise is not vectorised.

## Verify
`ds.take_batch(5)` shows the new column.

## Checked
2026-11-03. Confirmed in Ray repo docs `data/transforming-data.md` and the `Dataset.map_batches` docstring in `python/ray/data/dataset.py`. Fixed: `concurrency=` was used as the actor-pool argument but is deprecated in favour of `compute`. Removed: `ActorPoolStrategy` "legacy spelling" claim (inverted), type-error claim for bare arrays, `filter` lambda line, dashboard Data tab claim.
Method: documentation only; no commands were run.

---
id: computing-software.ai-ml-engineering.ray.data-batch-inference
name: data-batch-inference
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, batch-inference, offline-inference, gpu-inference, actor-pool]
level: practitioner
status: docs-checked
description: "Run offline batch inference with Ray Data: class UDF on an actor pool, GPUs, batch size, separate preprocessing, ray.data.llm processors."
sources:
  - https://docs.ray.io/en/latest/data/batch_inference.html
  - https://docs.ray.io/en/latest/data/working-with-llms.html
  - https://docs.ray.io/en/latest/data/transforming-data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch inference

```python
import ray, torch

class Predictor:
    def __init__(self):                         # runs once per actor
        self.model = torch.jit.load("model.pt").cuda().eval()
    def __call__(self, batch):
        x = torch.as_tensor(batch["image"]).cuda()
        with torch.inference_mode():
            batch["pred"] = self.model(x).argmax(1).cpu().numpy()
        return batch

ds = ray.data.read_images("<DATA_URI>/imgs/", size=(224, 224))
ds = ds.map_batches(Predictor, compute=ray.data.ActorPoolStrategy(size=4),
                    num_gpus=1, batch_size=128)
ds.write_parquet("<OUTPUT_URI>/preds/")
```

## Facts from the docs
- The guide's four steps: load data, define a class that loads the pre-trained model in `__init__`, call `map_batches`, then iterate or save results.
- Size the actor pool to the GPUs in the cluster (the guide's comment: "Set the concurrency to the number of GPUs in your cluster", passed as `compute=ray.data.ActorPoolStrategy(size=n)`). The `concurrency` argument of `map_batches` is deprecated.
- Larger batch size makes inference faster (vectorised) and raises GPU utilisation; too large risks OOM. With GPUs, `batch_size` must be an explicit integer.
- With expensive CPU preprocessing, do it in a separate operation so inference on batch N overlaps preprocessing on batch N+1.
- LLMs: `ray.data.llm` provides `vLLMEngineProcessorConfig` and `build_processor`; its `concurrency` and `batch_size` config fields set the number of engine replicas (int `n` autoscales 1 to n for GPU stages; `(n, n)` is fixed) and rows per batch.
- Batch-inference checkpointing exists: rerunning with the same checkpoint configuration skips records already processed (see the guide for how to enable it).

## Verify
Output row count matches the input; the Ray dashboard shows GPUs busy.

## Checked
2026-11-03. Confirmed in Ray repo docs `data/batch-inference.md`, `data/working-with-llms.md`, `data/transforming-data.md` and `python/ray/data/dataset.py`, `llm.py`. Fixed: `concurrency=4` on `map_batches` is deprecated (use `compute`). Removed: "fused stages starve GPUs", `ray.put(weights)` advice, 80 percent utilisation threshold, tuning range `(1, 8)` for map_batches.
Method: documentation only; no commands were run.

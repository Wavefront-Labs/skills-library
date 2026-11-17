---
id: computing-software.ai-ml-engineering.mlops.triton-ensembles-and-business-logic-scripting
name: triton-ensembles-and-business-logic-scripting
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, triton-ensemble, triton-inference-server, bls, python-backend, model-serving]
level: practitioner
status: draft
description: "Chain preprocessing, models and postprocessing inside Triton with ensemble configs, and use Python-backend Business Logic Scripting when you need loops or conditionals."
sources:
  - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/architecture.html#ensemble-models
  - https://github.com/triton-inference-server/python_backend#business-logic-scripting
  - https://github.com/triton-inference-server/model_analyzer
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Triton ensembles and business logic scripting

**Goal:** a full inference pipeline (decode, preprocess, model, postprocess) runs in one Triton request, with tensors passed in server memory instead of extra network hops.

## Ensemble config
Repository layout: `preprocess/` (Python backend), `detector/` (TensorRT/ONNX), `postprocess/`, and `pipeline/` with only a `config.pbtxt` and an empty version folder `1/`.
```
name: "pipeline"
platform: "ensemble"
max_batch_size: 8
input  [ { name: "IMAGE_BYTES" data_type: TYPE_STRING dims: [ 1 ] } ]
output [ { name: "DETECTIONS" data_type: TYPE_FP32 dims: [ -1, 6 ] } ]
ensemble_scheduling {
  step [
    { model_name: "preprocess" model_version: -1
      input_map  { key: "RAW" value: "IMAGE_BYTES" }
      output_map { key: "PIXELS" value: "pixels" } },
    { model_name: "detector" model_version: -1
      input_map  { key: "images" value: "pixels" }
      output_map { key: "output0" value: "raw_boxes" } },
    { model_name: "postprocess" model_version: -1
      input_map  { key: "RAW_BOXES" value: "raw_boxes" }
      output_map { key: "BOXES" value: "DETECTIONS" } }
  ]
}
```
`input_map` keys are the step model's tensor names; values are ensemble-level tensor names. Each step model keeps its own instance groups and dynamic batching, so a slow CPU preprocess can get more instances than the GPU model.

## When ensembles are not enough: BLS
Ensembles are static DAGs: no conditionals, loops or early exit. Use a Python-backend model that calls other models:
```python
import triton_python_backend_utils as pb_utils
class TritonPythonModel:
    def execute(self, requests):
        responses = []
        for req in requests:
            text = pb_utils.get_input_tensor_by_name(req, "TEXT")
            emb = pb_utils.InferenceRequest(model_name="encoder", requested_output_names=["EMB"],
                                            inputs=[text]).exec()
            if emb.has_error():
                raise pb_utils.TritonModelException(emb.error().message())
            e = pb_utils.get_output_tensor_by_name(emb, "EMB")
            target = "large_ranker" if needs_rerank(e) else "small_ranker"
            out = pb_utils.InferenceRequest(model_name=target, requested_output_names=["SCORES"], inputs=[e]).exec()
            responses.append(pb_utils.InferenceResponse(output_tensors=[pb_utils.get_output_tensor_by_name(out, "SCORES")]))
        return responses
```
Use `async_exec()` with `async def execute` to fan out calls concurrently.

## Performance
- Python steps hold the GIL per instance; scale with `instance_group { count: N kind: KIND_CPU }` or move heavy preprocessing to DALI.
- Profile with `perf_analyzer -m pipeline --concurrency-range 1:32` and tune configs with Model Analyzer; check per-step queue time in `/metrics` (`nv_inference_queue_duration_us`).
- Large intermediate tensors on GPU stay on device between GPU steps; Python steps may force copies to host.

## Gotchas
- Shape and dtype mismatches between steps fail at load time - read the server log.
- Version `-1` means latest; pin versions in production ensembles for reproducibility.
- Ensemble itself has no instances; batching happens in the step models.

## Verify
- [ ] End-to-end output matches the offline pipeline on golden inputs.
- [ ] perf_analyzer throughput and p95 meet target at expected concurrency.

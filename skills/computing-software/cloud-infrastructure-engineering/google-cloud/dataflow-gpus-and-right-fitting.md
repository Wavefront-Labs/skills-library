---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataflow-gpus-and-right-fitting
name: dataflow-gpus-and-right-fitting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataflow, dataflow-gpu, right-fitting, runinference, resource-hints]
level: advanced
status: docs-checked
description: "Run ML inference on Dataflow GPUs: worker_accelerator options, NVIDIA driver install, custom containers, RunInference, and right fitting so only GPU steps get GPU workers."
sources: ["https://cloud.google.com/dataflow/docs/gpu/gpu-support", "https://cloud.google.com/dataflow/docs/gpu/use-gpus", "https://cloud.google.com/dataflow/docs/guides/right-fitting", "https://beam.apache.org/documentation/ml/about-ml/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataflow GPUs and right fitting

## 1. Enable GPUs on workers
```bash
python pipeline.py --runner=DataflowRunner --region=us-central1 \
  --dataflow_service_options="worker_accelerator=type:nvidia-l4;count:1;install-nvidia-driver" \
  --sdk_container_image=<AR>/beam-gpu:<TAG> --experiments=use_runner_v2
```
- GPUs need the Portable Runner (Runner v2). Supported `worker_accelerator` types include `nvidia-l4` and `nvidia-tesla-a100`; T4 and P4 are deprecated on Dataflow (end of life 2027-08-01), so use L4 with a G2 machine type.
- `install-nvidia-driver` installs the driver on the worker; the driver binaries are mounted into the container at `/usr/local/nvidia/`, so put `/usr/local/nvidia/lib64` on `LD_LIBRARY_PATH`. Your container supplies the rest of the GPU stack (for example an NVIDIA CUDA base image).
- If one SDK process can use most of the GPU memory, set `--experiments=no_use_multiple_sdk_containers` (or use one-vCPU workers) so several processes don't each load a model onto the GPU.
- GPU quota is per region; Dataflow assigns workers to a zone with GPUs in the region.

## 2. RunInference
```python
from apache_beam.ml.inference.base import RunInference
from apache_beam.ml.inference.pytorch_inference import PytorchModelHandlerTensor
handler = PytorchModelHandlerTensor(state_dict_path="gs://.../model.pt", model_class=Net)  # see the Beam docs for device options
preds = examples | RunInference(handler)
```
RunInference loads the model once per process and batches elements with `BatchElements`; override `batch_elements_kwargs` in the ModelHandler to set `min_batch_size`/`max_batch_size`. It supports batch and streaming and needs Beam 2.40.0 or later.

## 3. Right fitting
Only the inference step needs GPUs. With right fitting you request them per step with the `accelerator` resource hint instead of the `worker_accelerator` service option (do not use both):
```python
preds = examples | RunInference(handler).with_resource_hints(
    accelerator="type:nvidia-tesla-l4;count:1;install-nvidia-driver", min_ram="16GB")
```
Pipeline-level hints: `--resource_hints=min_ram=...`. Resource hints need Beam Java or Python 2.31.0 or later. Right fitting supports batch pipelines; streaming needs Horizontal Autoscaling and `--experiments=enable_streaming_rightfitting`. The driver version option (or its absence) must be the same across the whole pipeline.

## Gotchas
- Check that `worker_accelerator` is visible in `dataflow_service_options` in the monitoring UI; the order of tokens in the accelerator string matters.
- GPUs may be unavailable in a zone or region, which can fail the job at startup.

## Verify
- [ ] The job starts with GPU workers, `dataflow_service_options` shows the accelerator string, and only the inference step runs on GPU workers when using right fitting.

## Checked
2026-10-27. Confirmed against Dataflow GPU support and Use GPUs pages (Portable Runner requirement, supported type strings, T4/P4 deprecation date, install-nvidia-driver behaviour and mount path, no_use_multiple_sdk_containers, regional quota, zone assignment, token-order troubleshooting), Right fitting page (SDK versions, accelerator and min_ram hints, batch and streaming support, driver version rule, resource_hints option) and the Beam ML page (RunInference, BatchElements, Beam 2.40.0, state_dict_path). Removed: g2-standard-8 machine type and number_of_worker_harness_threads flag, PyTorch device argument, CUDA-compatibility, idle-cost and large-model statements, the nvidia-smi verify step.
Method: documentation only; no commands were run.

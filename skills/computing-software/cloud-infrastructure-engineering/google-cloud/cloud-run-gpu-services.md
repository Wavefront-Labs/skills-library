---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-gpu-services
name: cloud-run-gpu-services
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run, cloud-run-gpu, nvidia-l4, llm-inference, serverless-gpu]
level: advanced
status: docs-checked
description: "Serve inference on Cloud Run with GPUs: required CPU and memory, regions and quota, zonal redundancy choice, cold-start reduction for model loading, and concurrency tuning."
sources: ["https://docs.cloud.google.com/run/docs/configuring/services/gpu", "https://docs.cloud.google.com/run/docs/configuring/request-timeout"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run GPU services

## 1. Deploy
```bash
gcloud run deploy llm --image=<AR>/vllm-server@sha256:... --region=us-central1 \
  --gpu=1 --gpu-type=nvidia-l4 --cpu=8 --memory=32Gi \
  --no-cpu-throttling --max-instances=4 --concurrency=16 \
  --no-gpu-zonal-redundancy \
  --service-account=llm-run@<P>.iam.gserviceaccount.com --no-allow-unauthenticated
```
- GPU services need instance-based billing (CPU always allocated, `--no-cpu-throttling`) and minimums (at least 4 vCPU / 16 GiB for L4).
- Only some regions offer GPUs (L4: asia-southeast1, asia-south1 by invitation, europe-west1, europe-west4, us-central1, us-east4 at the time of checking); quota is per project per region. The quota metrics are `run.googleapis.com/nvidia_l4_gpu_allocation` (zonal redundancy on) and `run.googleapis.com/nvidia_l4_gpu_allocation_no_zonal_redundancy` (off).
- Zonal redundancy off (`--no-gpu-zonal-redundancy`) is the lower-cost option and quota increases for it are more likely to be granted.
- The NVIDIA driver is provided by Cloud Run (580.x.x, CUDA 13.0 at the time of checking), mounted under `/usr/local/nvidia/lib64` and appended to `LD_LIBRARY_PATH`; images need only the CUDA user-space libraries.

## 2. Cold start is the problem
Loading a multi-GB model usually dominates start-up time.
- Bake small models into the image, or mount a Cloud Storage bucket (`--add-volume=name=models,type=cloud-storage,bucket=<B>`) and load from the mount path; for big models download in parallel or use a format that memory-maps (safetensors).
- `--min-instances=1` for latency-sensitive endpoints (you pay for the idle GPU instance).
- Use startup probes with a long enough window so instances only get traffic once the model is in GPU memory.

## 3. Concurrency
Set `--concurrency` to what the server batches well. Too high queues requests inside one
instance; too low scales out more GPU instances than needed.
`--max-instances` is your spend cap.

## Gotchas
- Requests time out at the service request timeout (default 300 s, maximum 3600 s); stream tokens for long generations.
- GPU quota is separate from CPU quota; request it per region before deploying.
- GPU services use instance-based billing, so you pay while an instance is alive, including idle time.

## Verify
- [ ] `gcloud run services describe llm --region=<R>` shows the GPU type and count in the service configuration.
- [ ] Logs show the model loaded before the startup probe passed; p95 latency at target concurrency meets SLO.

## Checked

2026-10-24, Cloud Run GPU configuration page (docs.cloud.google.com/run/docs/configuring/services/gpu) and the request-timeout page. Confirmed: L4 minimum 4 CPU and 16 GiB, `--gpu`, `--gpu-type=nvidia-l4`, `--no-gpu-zonal-redundancy`, `--no-cpu-throttling` with instance-based billing, L4 regions, quota metric names, driver path and version, request timeout default 300 s and maximum 3600 s. Removed unconfirmed claims (GPU start in seconds, vLLM concurrency range, describe format expression).

Method: documentation only; no commands were run.

---
id: computing-software.ai-ml-engineering.vllm.kubernetes-deployment
name: kubernetes-deployment
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [kubernetes, deployment, probes, hf-token, shm]
level: practitioner
status: docs-checked
description: "Deploy vLLM on native Kubernetes with a PVC, a Hugging Face token Secret, GPU limits, probes and the startup-probe fix."
sources:
  - https://docs.vllm.ai/en/latest/deployment/k8s/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run vLLM as a Deployment plus Service on Kubernetes.

Setup from the guide:
1. Create a PersistentVolumeClaim (CPU example `vllm-models`, ReadWriteOnce, 50Gi) and an Opaque Secret (`hf-token-secret`, key `token`) holding your Hugging Face access token. For GPUs the page says the PVC (model cache) is optional, hostPath or other storage works, and the Secret is only needed for gated models.
2. Create a Deployment whose container runs `vllm serve <model>`, exposes `containerPort: 8000`, and sets `HF_TOKEN` from the Secret via `secretKeyRef`, plus a ClusterIP Service targeting port 8000.

CPU deployment is for demonstration and testing only; use image `public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:latest` for x86_64 or `vllm-arm64-cpu-release-repo:latest` for arm64.

GPU deployment (the page deploys Mistral-7B-Instruct-v0.3 with image `vllm/vllm-openai:latest`): set `nvidia.com/gpu: "1"` in resources (example limits cpu "10" and memory 20G, requests cpu "2" and memory 6G), mount an `shm` emptyDir (`medium: Memory`; the NVIDIA example uses `sizeLimit: "2Gi"`, the AMD ROCm one `8Gi`) at `/dev/shm` because tensor parallel inference needs host shared memory, and add liveness and readiness `httpGet` probes on `/health` port 8000 with `initialDelaySeconds: 60`. The AMD example uses `amd.com/gpu`, `hostNetwork`, `hostIPC` and extra securityContext settings.

Test with a `curl` to `/v1/completions` on the Service. For gRPC serving and its probes see grpc-serving-probes.

Troubleshooting: if a startup or readiness probe `failureThreshold` is too low for model load time, Kubernetes kills the container. Signs: the log shows `KeyboardInterrupt: terminated` and `kubectl get events` shows `Container $NAME failed startup probe, will be restarted`. Raise `failureThreshold`; to size it, remove the probes and measure how long the server takes to become ready.

Alternatives listed by the docs: Helm, NVIDIA Dynamo, llmaz, llm-d, KAITO, KServe, Kthena, KubeRay, LeaderWorkerSet, llama-stack, kubeai, AIBrix and production-stack.

## Checked

Method: 2026-11-08 read the vLLM Kubernetes deployment page (docs source markdown) in full and compared every claim.
Changes: corrected the shm size (page shows 2Gi for NVIDIA, 8Gi for AMD, not 8Gi for both), removed an unsupported claim about not naming a Service `vllm`, and added which resources are optional and the probe path. Other claims were unchanged and match the page.

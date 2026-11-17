---
id: computing-software.ai-ml-engineering.vllm.helm-chart
name: helm-chart
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [helm, chart, values-yaml, autoscaling, model-download]
level: practitioner
status: docs-checked
description: "Install the vLLM Helm chart and set its main values: image, resources, probes, autoscaling and S3 model download."
sources:
  - https://docs.vllm.ai/en/latest/deployment/frameworks/helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deploy vLLM to Kubernetes with the Helm chart in the repository's chart-helm example.

Prerequisites: a running cluster, the NVIDIA Kubernetes device plugin (`k8s-device-plugin`), available GPUs, and optionally an S3 bucket holding the model weights for automatic download.

```bash
helm upgrade --install --create-namespace \
  --namespace=ns-vllm test-vllm . -f values.yaml \
  --set secrets.s3endpoint=$ACCESS_POINT --set secrets.s3bucketname=$BUCKET \
  --set secrets.s3accesskeyid=$ACCESS_KEY --set secrets.s3accesskey=$SECRET_KEY
helm uninstall test-vllm --namespace=ns-vllm
```

Uninstall removes all chart components including persistent volumes.

Selected `values.yaml` keys and defaults:
- `image.repository` `vllm/vllm-openai`, `image.tag` `latest`, `image.command` `["vllm","serve","/data/","--served-model-name","opt-125m","--host","0.0.0.0","--port","8000"]`.
- `replicaCount` 1; `containerPort` 8000; `servicePort` 80.
- `resources` request and limit 4 CPU, 16Gi memory, `nvidia.com/gpu` 1.
- `livenessProbe` httpGet `/health` port 8000, initialDelaySeconds 15, periodSeconds 10, failureThreshold 3; `readinessProbe` same path with delay 5 and period 5.
- `autoscaling.enabled` false, minReplicas 1, maxReplicas 100, targetCPUUtilizationPercentage 80.
- `extraInit.modelDownload.enabled` true (download job and wait container, default image `amazon/aws-cli` tag 2.6.4), `extraInit.pvcStorage` "1Gi", `extraInit.s3modelpath` `relative_s3_model_path/opt-125m`.
- `gpuModels` `["TYPE_GPU_USED"]`.

## Checked

2026-11-03. Confirmed against the Helm deployment page (docs.vllm.ai/en/latest/): chart values, defaults, install and uninstall commands.

Method: documentation only; no commands were run.

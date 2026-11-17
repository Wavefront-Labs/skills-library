---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-lora-adapters
name: kserve-llmisvc-lora-adapters
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [lora, specmodellora, adapters, maxrank, maxadapters, maxcpuadapters, hf-token, vllm-lora, pvc]
level: practitioner
status: docs-checked
description: "Serve LoRA adapters with LLMInferenceService via spec.model.lora: adapter name and uri (hf, s3, pvc), maxRank, maxAdapters, maxCpuAdapters, service account credentials."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/lora-adapters.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LoRA adapters on LLMInferenceService

Requires vLLM (default runtime) and a base model of the same architecture as the adapters. Adapters are loaded at startup (no dynamic loading); vLLM switches per request.

```yaml
spec:
  model:
    uri: hf://Qwen/Qwen2.5-7B-Instruct
    name: Qwen/Qwen2.5-7B-Instruct
    lora:
      maxRank: 16        # vLLM --max-lora-rank (default 16)
      maxAdapters: 2     # vLLM --max-loras (default 1)
      maxCpuAdapters: 4  # vLLM --max-cpu-loras (default maxAdapters)
      adapters:
        - name: sql-adapter
          uri: hf://my-org/qwen-sql-lora
        - name: code-adapter
          uri: s3://my-bucket/adapters/code-lora
        - name: local
          uri: pvc://adapter-pvc/domain-lora
```

Constraints: adapter `name` unique, case-sensitive and different from the base model name; `uri` must be `hf://`, `s3://` or `pvc://`. Clients request an adapter by using its name as the model.

## Credentials
Env vars cannot be added to the storage-initializer via `spec.template`. Put a Secret on the service account (default `default`):
```bash
kubectl create secret generic hf-token --from-literal=HF_TOKEN=<token>
kubectl patch serviceaccount default -p '{"secrets": [{"name": "hf-token"}]}'
```
For S3 use keys `awsAccessKeyID` and `awsSecretAccessKey`. `pvc://` gives fastest startup and suits air-gapped clusters. Only `hf://` was specifically tested; OCI is not supported for adapters (only one modelcar per pod, already taken by the base model). A pvc:// adapter path must hold `adapter_config.json` and `adapter_model.safetensors` (or `adapter_model.bin`); the page recommends ReadOnlyMany. With the storage-initializer disabled, only `pvc://` adapters work. A manual `--lora-modules` container arg makes the controller skip automatic LoRA configuration.

## Checked
Confirmed against the KServe LoRA Adapters for LLMInferenceService page: field reference and vLLM flag mapping with defaults, constraints, URI schemes, credential mechanism and key names, testing note, OCI limitation. Added PVC layout, storage-initializer and manual-args notes from the same page.

Method: docs-only read of cited pages, 2026-11-08

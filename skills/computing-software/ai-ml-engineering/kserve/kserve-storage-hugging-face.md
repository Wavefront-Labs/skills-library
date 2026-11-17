---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-hugging-face
name: kserve-storage-hugging-face
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [hf, hf-token, huggingface-hub, private-models, storage-config]
level: practitioner
status: docs-checked
description: "Deploy from Hugging Face Hub with hf://REPO/MODEL:HASH; anonymous for public models; HF_TOKEN via a ServiceAccount storage-config Secret or a ClusterStorageContainer."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/providers/hf.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hugging Face Hub storage

Format: `hf://${REPO}/${MODEL}:${HASH}` (hash optional), for example `hf://facebook/opt-125m`. Public models use an anonymous client.

Private models need `HF_TOKEN`. Two ways:

Option 1: ServiceAccount with a Secret reference.

```yaml
apiVersion: v1
kind: Secret
metadata: {name: storage-config}
type: Opaque
data:
  HF_TOKEN: <base64 token>
---
apiVersion: v1
kind: ServiceAccount
metadata: {name: hfserviceacc}
secrets:
  - name: storage-config
---
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata: {name: huggingface-llama3}
spec:
  predictor:
    serviceAccountName: hfserviceacc
    model:
      modelFormat: {name: huggingface}
      args: [--model_name=llama3, --model_dir=/mnt/models]
      storageUri: hf://meta-llama/meta-llama-3-8b-instruct
      resources:
        limits: {cpu: "6", memory: 24Gi, nvidia.com/gpu: "1"}
```

Option 2 (to set `HF_TOKEN` directly on the storage-initializer container): define a ClusterStorageContainer with `workloadType: initContainer`, a supported URI format with the `hf://` prefix, and a Secret-backed `HF_TOKEN` environment variable. The ClusterStorageContainer is cluster-scoped, but the referenced Secret must be in the same namespace as the InferenceService. KServe's "Providing Credentials with a ClusterStorageContainer" page has a complete example.

The ServiceAccount example also sets matching `requests` for cpu, memory and GPU. Check readiness with `kubectl get inferenceservices huggingface-llama3`.

## Checked
Confirmed against KServe's Hugging Face storage page: URI format with optional hash, anonymous download for public models, `HF_TOKEN` in the `storage-config` Secret, the ServiceAccount option and example, and the ClusterStorageContainer option. Removed the earlier `env`/`secretKeyRef` option, which the page does not describe.
Method: docs-only read of cited pages, 2026-11-08

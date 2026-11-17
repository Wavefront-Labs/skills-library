---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-multiple-uris
name: kserve-storage-multiple-uris
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [storageuris, mountpath, multiple-storage-uris, lora-adapters, knative-init-container, storage-uri-env]
level: practitioner
status: docs-checked
description: "Fetch several artifacts into one pod with storageUris (uri plus mountPath): common root rule, absolute paths, exclusive with storageUri, conflict handling."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/multiple-storage-uris.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multiple storage URIs

`storageUris` is a list of `{uri, mountPath}` entries fetched from any supported provider. Use it for a base model plus LoRA adapters, or a model plus preprocessing artifacts.

```yaml
spec:
  predictor:
    model:
      modelFormat: {name: huggingface}
    storageUris:
      - uri: hf://microsoft/DialoGPT-medium
        mountPath: /mnt/models/base
      - uri: s3://my-bucket/lora-adapters/customer-service
        mountPath: /mnt/models/adapters
```

Rules:
- Default `mountPath` is `/mnt/models`; omitted entries all land there.
- Custom paths must be absolute and share one common root (not `/`): `/mnt/models/a` + `/mnt/models/b` is valid, `/models/a` + `/other/b` is not. Paths are validated against directory traversal.
- `storageUri` and `storageUris` are mutually exclusive. `storageUris: [{uri: X}]` equals `storageUri: X`.
- Same path with the same filename in two URIs overwrites non-deterministically; use separate subdirectories. Different filenames merge into one directory.
- Available on predictor, transformer and explainer.
- Knative deployments need the Knative init container feature flag enabled.
- The legacy `STORAGE_URI` env var is not supported with this feature.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited KServe multiple storage URIs page in full; every claim matches it. No content removed.

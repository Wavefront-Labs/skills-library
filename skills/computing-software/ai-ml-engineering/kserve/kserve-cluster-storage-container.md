---
id: computing-software.ai-ml-engineering.kserve.kserve-cluster-storage-container
name: kserve-cluster-storage-container
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [clusterstoragecontainer, supporteduriformats, storage-initializer, custom-protocol, model-registry, hf-token, prefix, regex]
level: advanced
status: docs-checked
description: "Customise the storage initializer with ClusterStorageContainer (v1alpha1): supportedUriFormats prefix/regex, container name, custom model-registry:// protocol, HF_TOKEN."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/storage-containers/storage-containers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ClusterStorageContainer

Since KServe 0.11 the `ClusterStorageContainer` CRD (`serving.kserve.io/v1alpha1`) maps URI formats to a container spec for the storage initializer. The default one (installed by the Helm chart) is named `default`, uses `kserve/storage-initializer:latest`, requests 100m CPU / 100Mi and limits 1 CPU / 1Gi, with:

```yaml
supportedUriFormats:
  - prefix: gs://
  - prefix: s3://
  - prefix: hdfs://
  - prefix: webhdfs://
  - regex: "https://(.+?).blob.core.windows.net/(.+)"
  - regex: "https://(.+?).file.core.windows.net/(.+)"
  - regex: "https?://(.+)/(.+)"
  - regex: "hf://"
```

Rules:
- `spec.container.name` MUST be `storage-initializer`, otherwise the init container is not recognised and duplicate-value errors occur.
- Each URI format must be claimed by only one CR; with two matches the winner is undefined.

## Custom protocol
Build an image whose entrypoint takes two positional args: source URI (the `storageUri`) and destination path (for example `/mnt/models`). Add a CR with `supportedUriFormats: [{prefix: model-registry://}]`, plus env such as `MODEL_REGISTRY_BASE_URL`, then use `storageUri: "model-registry://iris/v1"`.

## Credentials
Put secrets in container env, for example `HF_TOKEN` via `valueFrom.secretKeyRef` (`name: hf-secret`, `key: HF_TOKEN`, `optional: false`) with prefix `hf://`. The Secret must live in the InferenceService namespace.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website storage-containers page: the 0.11 introduction, default CR contents and URI formats, both warnings, the custom-protocol steps and the credentials example. No claims removed.

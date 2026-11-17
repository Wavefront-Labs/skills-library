---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-pvc
name: kserve-storage-pvc
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [pvc, persistentvolumeclaim, storagekserveioreadonly, pvc-uri, direct-mount]
level: practitioner
status: docs-checked
description: "Serve a model from a PersistentVolumeClaim with pvc://CLAIM/path/: folder layout, direct mount at /mnt/models, read-only by default, readonly annotation to enable writes."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/providers/pvc.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PVC model storage

Create a PV and PVC, then copy the model into the volume, for example with a throwaway pod that mounts the claim at `/pv` and `kubectl cp model.joblib model-store-pod:/pv/model.joblib -c model-store`, then delete the pod.

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: sklearn-pvc
spec:
  predictor:
    model:
      modelFormat: {name: sklearn}
      storageUri: "pvc://${PVC_NAME}/${MODEL_NAME}/"
```

The folder `${PVC_NAME}/${MODEL_NAME}/` must contain the model file (here `model.joblib`). `${MODEL_NAME}` is just a folder name; matching the service name is a convention.

## Read-write
PVC volumes are mounted read-only by default. For write access add the annotation on the InferenceService:

```yaml
metadata:
  annotations:
    storage.kserve.io/readonly: "false"
```

## Mount behaviour
KServe mounts the PVC directly at `/mnt/models` in the user container instead of symlinking `/mnt/models` to a shared volume, which improves performance and simplifies the storage layout.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited KServe PVC storage page in full; every claim matches it. No content removed.

---
id: computing-software.ai-ml-engineering.kserve.kserve-modelcar-oci
name: kserve-modelcar-oci
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [oci, modelcar, enablemodelcar, uidmodelcar, cpumodelcar, memorymodelcar, shareprocessnamespace, oci-image]
level: practitioner
status: docs-checked
description: "Modelcars: serve a model from an OCI image with oci:// URIs. Enable enableModelcar in storageInitializer config, build an image with /models, pin the tag, tune uidModelcar."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/providers/oci.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Modelcars (OCI image storage)

Modelcars avoid per-pod model downloads: a sidecar container runs the model image and the runtime reads the files through the shared process namespace. Benefits: faster scale-up, less duplicated disk, image pre-fetching and lazy loading.

## Enable (off by default)
In the `storageInitializer` JSON of `inferenceservice-config`, add `"enableModelcar": true` and `"uidModelcar": 1010` (the UID is required for minikube), then restart the controller (`kubectl delete pod -n kserve -l control-plane=kserve-controller-manager`).

| Key | Meaning | Example |
|---|---|---|
| `enableModelcar` | allow `oci://` source URLs | `true` |
| `cpuModelcar` | CPU request and limit of the modelcar container | `10m` |
| `memoryModelcar` | memory request and limit | `15Mi` |
| `uidModelcar` | UID of the modelcar and main container; `0` for root; unset uses the containers UID | `1042` |

## Build the image
The base image needs `ln` and `sleep`; the model must be in `/models`:

```dockerfile
FROM busybox
RUN mkdir /models && chmod 775 /models
COPY data/ /models/
```

## Use
```yaml
spec:
  predictor:
    model:
      modelFormat: {name: sklearn}
      storageUri: oci://myuser/mymodel:1.0
```

Always use a specific tag. A fixed tag gives pull policy `IfNotPresent` (local cache reuse); `latest` or no tag gives `Always`, re-downloading on every restart or scale-up.

Mechanism: the modelcar runs `ln -sf /proc/$$/root/models /mnt/`; this needs `.spec.shareProcessNamespace: true`, which KServe sets for `oci://` URIs. Verify with `kubectl get $pod -o jsonpath="{.spec.shareProcessNamespace}"`; `/mnt/models` then points to `/proc/<pid>/root/models`.

## Checked
Confirmed against KServe's OCI (Modelcars) page: off by default, `storageInitializer` keys `enableModelcar`, `cpuModelcar`, `memoryModelcar`, `uidModelcar` (UID setting shown for minikube), controller restart, Dockerfile requirements (`ln`, `sleep`, `/models`), `oci://` URI, pull policy by tag, and the `ln -sf` plus `shareProcessNamespace` mechanism.
Method: docs-only read of cited pages, 2026-11-08

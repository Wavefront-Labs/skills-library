---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-thanos-sidecar
name: prometheus-operator-thanos-sidecar
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [thanos-sidecar, objectstorageconfig, object-storage, disable-compaction, shipper-meta-file]
level: advanced
status: docs-checked
description: "Add a Thanos sidecar to a Prometheus resource and upload TSDB blocks to object storage via a Secret, including the Prometheus v3.9 and Thanos v0.42 compaction coordination."
sources: ["https://prometheus-operator.dev/docs/platform/thanos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The operator manages the Thanos **sidecar** (via `Prometheus`) and **Thanos Ruler** (via `ThanosRuler`). Querier, Receiver, Compactor and Store Gateway are deployed separately, for example from kube-thanos.

## Enable the sidecar
Set a non-empty `spec.thanos`; the minimum is an image:
```yaml
spec:
  thanos:
    image: quay.io/thanos/thanos:v0.28.1
```
(The image tag is the docs example, not a recommendation; use a current Thanos release.)

## Object storage upload
Write a Thanos objstore file (`type: s3`, `config: {bucket, endpoint, access_key, secret_key}`), create a Secret from it, and reference it:
```sh
kubectl -n monitoring create secret generic thanos-objstore-config --from-file=thanos.yaml=<objstore-config-file>
```
```yaml
spec:
  thanos:
    objectStorageConfig:
      key: thanos.yaml
      name: thanos-objstore-config
```
The sidecar then uploads every new block Prometheus produces (every 2 hours).

## Compaction
With Prometheus older than v3.9.0 or sidecar older than v0.42.0, this disables local compaction (min and max block durations equal), leaving the Thanos Compactor as the sole compactor. With Prometheus v3.9.0 or newer and sidecar v0.42.0 or newer, local compaction stays on: Prometheus starts with `--storage.tsdb.delay-compact-file.path` and the sidecar with `--shipper.meta-file-name` and `--shipper.ignore-unequal-block-size`, so only uploaded blocks are compacted. Force the old behaviour with `spec.disableCompaction: true`.

## Checked

2026-11-08. Read the Thanos page in full. Replaced a temp path with a placeholder and noted the image tag is the docs example.

Method: documentation only; no commands were run.

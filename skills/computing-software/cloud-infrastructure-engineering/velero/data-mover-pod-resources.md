---
id: computing-software.cloud-infrastructure-engineering.velero.data-mover-pod-resources
name: data-mover-pod-resources
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [podresources, data-mover-memory, oom, memorylimit, upload-concurrency]
level: advanced
status: docs-checked
description: "Size data mover pods with podResources and tie memory limits to --parallel-files-upload and --parallel-blocks-upload to avoid OOM kills."
sources:
  - https://velero.io/docs/main/data-movement-pod-resource-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set CPU, memory and ephemeral storage for data mover pods in the node-agent ConfigMap:

```json
{
    "podResources": {
        "cpuRequest": "1000m",
        "cpuLimit": "1000m",
        "ephemeralStorageRequest": "5Gi",
        "ephemeralStorageLimit": "10Gi",
        "memoryRequest": "512Mi",
        "memoryLimit": "1Gi"
    }
}
```

Values must be valid Kubernetes quantities and each request must not exceed its limit; if any value fails, the entire `podResources` section is ignored and the default (BestEffort) applies.

Memory and upload concurrency are separate. Uploads are asynchronous and data stays in memory until written to the repository, so pod memory grows with `--parallel-files-upload` or `--parallel-blocks-upload`. If unset these default to GOMAXPROCS, derived from the pod CPU limit or else the node CPU count, so a 96-CPU node defaults to 96. If you set `memoryLimit`, also set the concurrency on the backup or schedule. Changing `cpuLimit` changes the default concurrency but is not the intended memory control.

Starting value: divide the bandwidth to backup storage by the throughput of one stream (measure with concurrency 1), round up and add headroom. In the documented example 130 MiB/s of storage bandwidth was filled by 2 streams; the default of 96 used about 1 GiB versus 330 MiB.

The block data mover memory also grows with the provisioned volume size. For restores, `--parallel-files-download` is the equivalent for the file system mover; the block mover has none.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/data-movement-pod-resource-configuration/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.

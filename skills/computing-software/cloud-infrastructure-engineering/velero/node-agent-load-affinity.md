---
id: computing-software.cloud-infrastructure-engineering.velero.node-agent-load-affinity
name: node-agent-load-affinity
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [loadaffinity, node-selection, anti-affinity, matchexpressions, storageclass-affinity]
level: advanced
status: docs-checked
description: "Constrain data movement pods to or away from nodes with loadAffinity, including the first-element rule and per-storage-class entries."
sources:
  - https://velero.io/docs/main/data-movement-node-selection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`loadAffinity` in the node-agent ConfigMap chooses which nodes data movement runs on. Reasons: keep it off nodes with critical workloads, run it on nodes with more resources, or only where the storage can provision volumes and snapshots.

Gotcha: only the first array element without a `storageClass` is used for general selection. Extra elements are ignored unless they carry a `storageClass`. To require several conditions, combine them in a single element:

```json
{
    "loadAffinity": [
        {
            "nodeSelector": {
                "matchLabels": {
                    "environment": "production",
                    "disk-type": "ssd"
                }
            }
        }
    ]
}
```

Two separate elements for those labels would apply only the first.

Affinity: use `matchLabels` (treated as `In`) or `matchExpressions` with operator `In` or `Exists`. Anti-affinity: `matchExpressions` with operator `NotIn` or `DoesNotExist`.

Per storage class, add `"storageClass": "fast-ssd"` to an entry; DataUpload and DataDownload pods for PVCs of that class then use that entry's selector, and for a class with several entries the first match is chosen.

This applies to CSI snapshot data movement pods (DataUpload and DataDownload). Create the ConfigMap and pass `--node-agent-configmap`, then restart node-agent.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/data-movement-node-selection/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.

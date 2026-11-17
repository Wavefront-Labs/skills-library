---
id: computing-software.cloud-infrastructure-engineering.velero.node-agent-load-concurrency
name: node-agent-load-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [loadconcurrency, pernodeconfig, globalconfig, preparequeuelength, node-agent-concurrency]
level: advanced
status: docs-checked
description: "Set concurrent data mover loads per node with globalConfig and perNodeConfig, and cap pending intermediate objects with prepareQueueLength."
sources:
  - https://velero.io/docs/main/node-agent-concurrency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default node-agent runs one data mover load at a time per node. Raise it when nodes have spare CPU, memory and bandwidth; lower it if backups hang, lag or are OOM killed.

```json
{
    "loadConcurrency": {
        "globalConfig": 2,
        "perNodeConfig": [
            {
                "nodeSelector": {
                    "matchLabels": {
                        "kubernetes.io/hostname": "node1"
                    }
                },
                "number": 3
            }
        ]
    }
}
```

- `globalConfig`: applies to every node without a per-node rule. Minimum 1 (no concurrency); no upper limit. Missing or invalid falls back to 1.
- `perNodeConfig`: a list of label selector rules, each with a `number`. It overrides the global value for matching nodes. A rule matching no node has no effect. A node matching several rules gets the smallest number.

`prepareQueueLength` limits how many DataUpload, DataDownload, PodVolumeBackup and PodVolumeRestore objects may sit in preparation phases (`Accepted`, `Prepared`) without being processed. This bounds intermediate PVCs, VolumeSnapshots and pods that otherwise linger when node parallelism is far below the number of volumes.

```json
{ "loadConcurrency": { "prepareQueueLength": 10 } }
```

Create with `kubectl create cm node-agent-config -n velero --from-file=<json file name>` and restart node-agent for changes.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/node-agent-concurrency/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.

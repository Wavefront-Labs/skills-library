---
id: computing-software.cloud-infrastructure-engineering.velero.node-agent-configmap-basics
name: node-agent-configmap-basics
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [node-agent-configmap, node-agent-config, rollout-restart, daemonset, data-mover-pods]
level: practitioner
status: docs-checked
description: "Create the node-agent ConfigMap, attach it with --node-agent-configmap and restart the DaemonSet so changes take effect."
sources:
  - https://velero.io/docs/main/supported-configmaps/node-agent-configmap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Advanced data mover pod settings live in a JSON ConfigMap in the Velero namespace. It covers PodVolumeBackup, PodVolumeRestore, DataUpload and DataDownload pods. You create and maintain the ConfigMap yourself; its life cycle is outside Velero.

Create it:

```bash
kubectl create cm <ConfigMap-Name> -n velero --from-file=<json-file-name>
```

Attach it at install time:

```bash
velero install --node-agent-configmap=<ConfigMap-Name>
```

or afterwards by editing the DaemonSet (`kubectl edit ds node-agent -n velero`) and adding the argument:

```yaml
spec:
  template:
    spec:
      containers:
      - args:
        - --node-agent-configmap=<ConfigMap-Name>
```

The node-agent reads configuration only at startup, so after editing the ConfigMap restart it:

```bash
kubectl rollout restart -n <velero-namespace> daemonset/node-agent
```

One ConfigMap per Velero instance namespace.

Top-level sections: `loadConcurrency`, `loadAffinity`, `podResources`, `priorityClassName`, `backupPVC`, `restorePVC`, `privilegedFsBackup`, `cachePVC`, `podLabels`, `podAnnotations`, `tolerations`.

Invalid `podResources` values cause that whole section to be ignored.

A practical workflow is to start with a small JSON file containing a single section, apply it, restart the node-agent, then confirm the new data mover pods pick it up before adding further sections. Keep the JSON file in Git, since Velero does not manage the ConfigMap for you.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/supported-configmaps/node-agent-configmap/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.

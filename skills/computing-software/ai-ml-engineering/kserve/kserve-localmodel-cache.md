---
id: computing-software.ai-ml-engineering.kserve.kserve-localmodel-cache
name: kserve-localmodel-cache
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [localmodelcache, localmodelnamespacecache, localmodelnodegroup, localmodelnode, model-cache, local-storage, sourcemodeluri, modelsize, nodegroups, workloadtype, jobnamespace, hostpath]
level: advanced
status: docs-checked
description: "Cache models on nodes with LocalModelCache, LocalModelNamespaceCache, LocalModelNodeGroup: localModel config, credentials, local.path matching agent hostPath, status checks."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/modelcache/localmodel.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Local model cache

Resources: `LocalModelCache` (cluster scoped), `LocalModelNamespaceCache` (namespaced, checked first for a matching InferenceService), `LocalModelNodeGroup` (node set plus local PV), `LocalModelNode` (per-node status). Disabled by default; enable in `inferenceservice-config`:

```yaml
localModel: |-
  {"enabled": true, "jobNamespace": "kserve-localmodel-jobs", "defaultJobImage": "kserve/storage-initializer:latest",
   "fsGroup": 1000, "localModelAgentImage": "kserve/kserve-localmodelnode-agent:latest"}
```

## Credentials
Download jobs run in `jobNamespace`; Secrets and ServiceAccounts must exist there. Option A, inline on the cache resource: `serviceAccountName`, `storage.key` (key in `storage-config`, for example `{"type":"hf","token":"..."}`), or `storage.parameters` (for example `type: s3`, `region`). Job image and resources derive from `storageInitializer` config. Option B: a `ClusterStorageContainer` with `workloadType: localModelDownloadJob`; it takes precedence over inline fields.

## Node group
```yaml
apiVersion: serving.kserve.io/v1alpha1
kind: LocalModelNodeGroup
metadata: {name: workers}
spec:
  storageLimit: 1.7T
  persistentVolumeClaimSpec: {accessModes: [ReadWriteOnce], resources: {requests: {storage: 1700G}}, storageClassName: local-storage, volumeMode: Filesystem}
  persistentVolumeSpec:
    # capacity, accessModes, nodeAffinity omitted
    local: {path: /mnt/models}
    storageClassName: local-storage
```
`local.path` MUST equal the `kserve-localmodelnode-agent` DaemonSet hostPath (Helm default `/mnt/models` via `kserve.localmodel.agent.hostPath`; Kustomize `/models`) or duplicate download jobs loop. hostPath ignores fsGroup: chown the directory to 1000:1000. Label nodes `kserve/localmodel=worker`.

## Cache and use
```yaml
kind: LocalModelCache
metadata: {name: meta-llama3-8b-instruct}
spec: {sourceModelUri: "hf://meta-llama/meta-llama-3-8b-instruct", modelSize: 10Gi, nodeGroups: [workers]}
```
An InferenceService uses the cache when its `storageUri` equals `sourceModelUri`. Check `kubectl get localmodelcache NAME -oyaml` (`status.copies`, `nodeStatus: NodeDownloaded`) and `kubectl get localmodelnode NODE -oyaml` (`ModelDownloaded`).

## Checked
Confirmed against KServe's local model cache page: the four resources and resolution order, `inferenceservice-config` `localModel` settings, credential options and ClusterStorageContainer precedence, `local.path` versus agent hostPath (Helm and Kustomize defaults), hostPath ignoring fsGroup, node label, and the status checks `copies`, `NodeDownloaded` and `ModelDownloaded`.
Method: docs-only read of cited pages, 2026-11-08

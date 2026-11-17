---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-kv-cache-offloading
name: kserve-llmisvc-kv-cache-offloading
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [kvcacheoffloading, kv-cache, offloadingconnector, evictionpolicy, secondary, emptydir, pvc-ref, pvc-spec, lru, arc]
level: advanced
status: docs-checked
description: "Offload vLLM KV cache from GPU to CPU RAM and disk with spec.workload.kvCacheOffloading: cpu size, evictionPolicy lru/arc, secondary emptyDir/pvc.spec/pvc.ref tiers, mount paths."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/kv-cache-offloading.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService KV cache offloading

vLLM `OffloadingConnector` cascades evicted KV blocks GPU -> CPU RAM -> disk, and promotes them back on a hit. Allows longer contexts or more concurrent requests without more GPUs.

```yaml
spec:
  workload:
    kvCacheOffloading:
      cpu: "10Gi"           # required to enable
      evictionPolicy: lru   # lru (default) or arc
      secondary:            # optional ordered disk tiers
        - fileSystem:
            emptyDir:
              size: "100Gi"
```

Each `secondary` entry needs `fileSystem` with exactly one of:
- `emptyDir.size`: node-local, lives with the pod; the controller adds an `ephemeral-storage` request equal to `size`.
- `pvc.spec`: controller creates one ephemeral PVC per pod from a PersistentVolumeClaimSpec (for example `storageClassName: fast-local-nvme`, `resources.requests.storage: 100Gi`); deleted with the pod.
- `pvc.ref`: existing PVC (`name`, optional `path` subdirectory) that must exist before the service; survives restarts; use an RWX PVC such as CephFS to share across replicas.

Mount paths are automatic: `/mnt/kv-cache-0`, `/mnt/kv-cache-1`, by list position. Tiers can be mixed (for example emptyDir spill then shared CephFS). Without `secondary`, offloading stops at CPU RAM.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited KV cache offloading page in full. Removed the memory-limit sizing advice, which the page does not state.

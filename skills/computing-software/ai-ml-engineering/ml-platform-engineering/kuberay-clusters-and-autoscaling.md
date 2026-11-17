---
id: computing-software.ai-ml-engineering.ml-platform-engineering.kuberay-clusters-and-autoscaling
name: kuberay-clusters-and-autoscaling
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, ray, kuberay, raycluster, rayjob, rayservice, ray-autoscaler, kubernetes]
level: practitioner
status: docs-checked
description: "Run Ray on Kubernetes with KubeRay: RayCluster head/worker groups, in-tree autoscaling and its idle timeout, GPU worker groups from zero, and RayJob shutdown behaviour."
sources:
  - https://docs.ray.io/en/latest/cluster/kubernetes/index.html
  - https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/configuring-autoscaling.html
  - https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/rayjob-quick-start.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KubeRay clusters and autoscaling

**Goal:** Ray clusters for training, tuning and batch inference on Kubernetes, sized automatically to the work.

## RayCluster
```yaml
apiVersion: ray.io/v1
kind: RayCluster
metadata: {name: ml}
spec:
  enableInTreeAutoscaling: true
  headGroupSpec:
    rayStartParams: {num-cpus: "0"}          # keep tasks off the head
    template:
      spec:
        containers:
        - name: ray-head
          image: rayproject/ray-ml:<pinned-version>   # match the client's Ray version
  workerGroupSpecs:
  - groupName: gpu
    replicas: 0
    minReplicas: 0
    maxReplicas: 8
    template:
      spec:
        containers:
        - name: ray-worker
          image: rayproject/ray-ml:<pinned-version>
          resources: {limits: {cpu: "16", memory: 64Gi, nvidia.com/gpu: "1"}}
        tolerations: [{key: nvidia.com/gpu, operator: Exists, effect: NoSchedule}]
```
- `enableInTreeAutoscaling: true` makes the KubeRay operator add an autoscaling sidecar container to the head Pod.
- Set `minReplicas` and `maxReplicas` per worker group; initialise `replicas` and `minReplicas` to the same value, and the Ray Autoscaler then adjusts `replicas`.
- The Autoscaler scales on **logical resource requests** (declared in `@ray.remote`, visible in `ray status`), not physical utilisation. Unsatisfiable requests are queued, and nodes are added to meet the queue.
- A worker is idle when it has no tasks, actors or referenced objects (in memory or spilled); `idleTimeoutSeconds` (default 60s) is the wait before it is scaled down.
- `upscalingMode` controls the scale-up rate; `Conservative` rate-limits so pending worker Pods never exceed the connected workers.
- `num-cpus: "0"` in the head's `rayStartParams` stops Ray scheduling tasks and actors on the head.
- Starting with Ray 2.41.0 the Autoscaler reads resources from `rayStartParams`, container limits or container requests (earlier versions ignore requests). `rayStartParams` is optional from KubeRay 1.4.0; if omitted with autoscaling, the image needs Ray 2.45.0 or later.
- Autoscaler V2: with KubeRay 1.4.0 or later set `spec.autoscalerOptions.version: v2`.
- Use separate worker groups per hardware type (CPU-only, GPU) and scale GPU groups from 0.

## RayJob (batch)
Submits a Ray job to a new RayCluster. `shutdownAfterJobFinishes` (default `false`) recycles the cluster after the job finishes; `ttlSecondsAfterFinished` (default 0) works only when it is true. `backoffLimit` (default 0, since KubeRay 1.2.0) is the number of retries before the RayJob is marked failed, and each retry creates a new RayCluster.

## Pitfalls
- Ray version mismatch between client, head and workers fails in confusing ways; use one image tag everywhere.
- Logs disappear with pods; ship them off the cluster.

## Verify
- [ ] A job requesting GPUs scales the GPU group up from 0 and back down after the idle timeout.
- [ ] The RayJob cluster deletes itself on completion when `shutdownAfterJobFinishes` is true.
- [ ] Same Ray version in client and cluster.

## Checked
2026-11-01. Confirmed on the KubeRay autoscaling guide and RayJob quick start: `enableInTreeAutoscaling`, `minReplicas`/`maxReplicas`/`replicas`, logical-resource scaling, `idleTimeoutSeconds` default 60s, `upscalingMode`, `num-cpus: "0"`, Ray 2.41.0/2.45.0 and KubeRay 1.4.0 notes, Autoscaler V2 setting, `shutdownAfterJobFinishes`, `ttlSecondsAfterFinished`, `backoffLimit` defaults. Removed (not on the pages): `/dev/shm` sizing, RayService `serveConfigV2` upgrade behaviour, GCS fault tolerance with Redis, Fluent Bit, Kueue admission.
Method: documentation only; no commands were run.

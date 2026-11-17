---
id: computing-software.ai-ml-engineering.ray.kuberay-rayservice
name: kuberay-rayservice
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, rayservice, serveconfigv2, kuberay-service, zero-downtime-upgrade]
level: practitioner
status: docs-checked
description: "Host Ray Serve apps on Kubernetes with the KubeRay RayService CRD: serveConfigV2, zero-downtime upgrades, health and the head service."
sources:
  - https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/rayservice-quick-start.html
  - https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/rayservice.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KubeRay RayService

A RayService holds a Ray Serve config (`spec.serveConfigV2`, a multi-application Serve config available from KubeRay v0.6.0) and a cluster definition (`spec.rayClusterConfig`). KubeRay creates the RayCluster, waits for the head pod to be ready, then submits the Serve applications to the head's dashboard port.

```yaml
apiVersion: ray.io/v1
kind: RayService
metadata:
  name: llm
spec:
  serveConfigV2: |
    applications:
      - name: m
        route_prefix: /
        import_path: app:model_app
        runtime_env:
          working_dir: "https://example.com/code.zip"
  rayClusterConfig:
    rayVersion: "<ray version>"
    enableInTreeAutoscaling: true
    headGroupSpec:
      template:
        spec:
          containers:
            - name: ray-head
              image: <your image>
    workerGroupSpecs:
      - groupName: workers
        replicas: 1
        minReplicas: 1
        maxReplicas: 8
        template:
          spec:
            containers:
              - name: ray-worker
                image: <your image>
```
```bash
kubectl apply -f rayservice.yaml
kubectl get rayservice llm
kubectl get services
curl -X POST -H 'Content-Type: application/json' llm-serve-svc:8000/ -d '...'   # from a pod in the namespace
```

## Services
- When the Serve apps are healthy and ready, KubeRay creates `<name>-head-svc` (dashboard, jobs) and `<name>-serve-svc` (Serve HTTP, typically port 8000, routes across workers that run Serve replicas).
- During a zero-downtime upgrade the new RayCluster gets its own head service; the RayService head service selector is switched to it afterwards.

## Updates
- Changing only `serveConfigV2` and re-applying updates the Serve config on the existing RayCluster (in-place update); no new cluster is created.
- Changing `rayClusterConfig` triggers the default `NewCluster` upgrade: a new RayCluster is created, KubeRay waits until it is ready, switches traffic, then deletes the old cluster. This temporarily duplicates resources; `NewClusterWithIncrementalUpgrade` exists for large deployments (see the docs' incremental upgrade page).
- Fields managed by the Ray autoscaler (`replicas`, `minReplicas`, `maxReplicas`, `scaleStrategy.workersToDelete`) do not trigger an upgrade and are not propagated to the RayCluster.
- Changing `rayVersion` determines the autoscaler sidecar image and triggers a zero-downtime upgrade.
- `working_dir` in `runtime_env` can be a remote archive URL that RayService downloads at runtime.

## Verify
`kubectl get rayservice` shows `Running`; requests through `<name>-serve-svc:8000` succeed before, during and after a config change.

## Checked
Checked 2026-11-09 against the RayService quickstart and user guide (both read). Removed unconfirmed items: the exact `upgradeStrategy` YAML shape, `status.activeServiceStatus` path, port-forward command, GPU example and "serve-svc only routes to ready clusters".

Method: docs-checked 2026-11-09 against docs.ray.io RayService quickstart and user-guides rayservice pages; documentation only, no commands were run.

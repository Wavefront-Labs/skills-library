---
id: computing-software.ai-ml-engineering.ray.kuberay-raycluster
name: kuberay-raycluster
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, raycluster, kuberay, head-group-spec, worker-group-specs]
level: practitioner
status: docs-checked
description: "Deploy a Ray cluster on Kubernetes with the KubeRay operator RayCluster CRD: head and worker groups, autoscaling, resources, and kubectl checks."
sources:
  - https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html
  - https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KubeRay RayCluster

Install the KubeRay operator first (the quickstart points to the KubeRay operator Helm install guide for the latest stable release). The quickstart then deploys a sample RayCluster from the KubeRay Helm chart repo with `helm install raycluster kuberay/ray-cluster --version <chart version>`; confirm the current version in the docs.

```yaml
apiVersion: ray.io/v1
kind: RayCluster
metadata:
  name: demo
spec:
  rayVersion: "<ray version>"      # must match the image's Ray version
  enableInTreeAutoscaling: true
  headGroupSpec:
    rayStartParams:
      dashboard-host: "0.0.0.0"
      num-cpus: "0"
    template:
      spec:
        containers:
          - name: ray-head
            image: rayproject/ray:<ray version>
            resources:
              requests: {cpu: "2", memory: 8Gi}
              limits: {cpu: "2", memory: 8Gi}
  workerGroupSpecs:
    - groupName: cpu
      replicas: 2
      minReplicas: 0
      maxReplicas: 10
      template:
        spec:
          containers:
            - name: ray-worker
              image: rayproject/ray:<ray version>
              resources:
                requests: {cpu: "4", memory: 16Gi}
                limits: {cpu: "4", memory: 16Gi}
```
```bash
kubectl apply -f raycluster.yaml
kubectl get rayclusters
kubectl get pods --selector=ray.io/cluster=demo
kubectl port-forward service/demo-head-svc 8265:8265
```

## Notes
- `headGroupSpec` configures the head pod; `workerGroupSpecs` can hold several groups, each with `replicas` and optional `minReplicas`/`maxReplicas` (needed for autoscaling).
- The image must carry the same Ray version as `spec.rayVersion` (for a nightly image, use the latest release version).
- KubeRay sets Ray's logical CPU, memory and GPU capacity from the container limits (CPU request if no limit, since KubeRay 1.3.0; CPU rounded up). It ignores memory and GPU requests, so set them equal to limits.
- `rayStartParams` is a string-to-string map; all values, including `num-cpus`, must be strings. It is optional from KubeRay 1.4.0 and was required (possibly empty) before.
- `dashboard-host: "0.0.0.0"` on the head exposes the dashboard outside the pod. `num-cpus: "0"` on the head stops workloads with non-zero CPU needs being scheduled there.
- `enableInTreeAutoscaling: true` runs the Ray autoscaler in a sidecar container and sets `no-monitor: "true"` on the head.
- The head service is named `<RayCluster name>-head-svc`; the Ray Client is reachable on port 10001 and the dashboard on 8265.
- For GPUs set limits such as `nvidia.com/gpu` (with the NVIDIA device plugin).

## Verify
`kubectl get rayclusters` shows status `ready`; pods reach `Running` (image pulls take most of the time).

## Checked
Checked 2026-11-09 against the RayCluster quickstart and the RayCluster configuration guide (both read). Removed unconfirmed items: a pinned operator version and Helm repo URL, the /dev/shm emptyDir advice, the GKE/EKS toleration remark and the kubectl exec check.

Method: docs-checked 2026-11-09 against docs.ray.io RayCluster quickstart and user-guides config pages; documentation only, no commands were run.

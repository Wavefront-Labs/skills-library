---
id: computing-software.ai-ml-engineering.ray.kuberay-rayjob
name: kuberay-rayjob
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, rayjob, kuberay-job, entrypoint, shutdown-after-job]
level: practitioner
status: docs-checked
description: "Run batch jobs on ephemeral Kubernetes Ray clusters with the KubeRay RayJob CRD: entrypoint, runtimeEnvYAML, shutdownAfterJobFinishes and backoff."
sources:
  - https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/rayjob-quick-start.html
  - https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/rayjob.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KubeRay RayJob

A RayJob creates a RayCluster (or uses an existing one), submits the entrypoint as a Ray job, and can recycle the cluster afterwards.

```yaml
apiVersion: ray.io/v1
kind: RayJob
metadata:
  name: train
spec:
  entrypoint: python train.py --epochs 10
  runtimeEnvYAML: |
    pip:
      - torch
    env_vars:
      WANDB_MODE: offline
  shutdownAfterJobFinishes: true
  ttlSecondsAfterFinished: 300
  activeDeadlineSeconds: 7200
  backoffLimit: 1
  submissionMode: K8sJobMode
  rayClusterSpec:
    rayVersion: "<ray version>"
    headGroupSpec:
      template:
        spec:
          containers:
            - name: ray-head
              image: rayproject/ray:<ray version>
    workerGroupSpecs:
      - groupName: workers
        replicas: 2
        template:
          spec:
            containers:
              - name: ray-worker
                image: rayproject/ray:<ray version>
```
```bash
kubectl apply -f rayjob.yaml
kubectl get rayjobs.ray.io train -o jsonpath='{.status.jobStatus}'
kubectl logs -l=job-name=train
```

## Fields
- `entrypoint`: the submitter runs `ray job submit --address ... --submission-id ... -- $entrypoint`.
- `runtimeEnvYAML` (optional): runtime environment as a multi-line YAML string (files, packages, env vars).
- `clusterSelector`: run on an existing RayCluster instead of creating one.
- `submissionMode`: default `K8sJobMode` (operator creates a submitter Kubernetes Job). Others: `HTTPMode` (operator sends an HTTP request to the cluster), `InteractiveMode` (alpha, waits for you to submit), `SidecarMode` (injects a submitter container into the head pod; no `clusterSelector` or `submitterPodTemplate`; head restart policy must be `Never`).
- `backoffLimit` (added in KubeRay 1.2.0): retries before the RayJob is marked failed; each retry creates a new RayCluster. Default 0. A separate `submitterConfig.backoffLimit` (default 2) governs the submitter.
- `shutdownAfterJobFinishes` (default false) recycles the RayCluster after the job finishes; `ttlSecondsAfterFinished` (default 0, needs `shutdownAfterJobFinishes`) delays deletion of the cluster after the job finishes.
- `activeDeadlineSeconds`: if the RayJob is not `Complete` or `Failed` in time, `JobDeploymentStatus` becomes `Failed` with reason `DeadlineExceeded`.
- `preRunningDeadlineSeconds`: fails the RayJob with `PreRunningDeadlineExceeded` if it never reaches `Running` in time (default 0, none).

## Gotchas
- With shutdown enabled the submitter Job is kept (it holds the Ray job logs) and is cleaned up when the RayJob is deleted. Setting the operator environment variable `DELETE_RAYJOB_CR_AFTER_JOB_FINISHES` to true also deletes the RayJob itself.
- Rules-based deletion mode is incompatible with `shutdownAfterJobFinishes` and the global `ttlSecondsAfterFinished`.
- The code run by `entrypoint` must be available in the image or fetched through the runtime environment.

## Verify
`jobStatus` becomes `SUCCEEDED` and `jobDeploymentStatus` becomes `Complete`; with shutdown enabled the RayCluster is deleted after the TTL.

## Checked
Checked 2026-11-09 against the RayJob quickstart (field list, submission modes, shutdown walkthrough) and the RayJob user guide headings relevant to the above. Removed: the exit code 0 mapping, the pinned torch version, GPU worker example, and the claim that shutdown deletes logs (docs say the submitter Job with logs is kept).

Method: docs-checked 2026-11-09 against docs.ray.io RayJob quickstart and user-guides rayjob pages; documentation only, no commands were run.

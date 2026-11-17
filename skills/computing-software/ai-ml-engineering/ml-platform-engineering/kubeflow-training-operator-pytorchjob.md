---
id: computing-software.ai-ml-engineering.ml-platform-engineering.kubeflow-training-operator-pytorchjob
name: kubeflow-training-operator-pytorchjob
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, kubeflow, training-operator, pytorchjob, trainjob, distributed-training, kubernetes]
level: practitioner
status: docs-checked
description: "Run distributed PyTorch training on Kubernetes with the Kubeflow Training Operator: PyTorchJob master/worker specs, restarts, the Istio sidecar trap, and the move to Trainer v2."
sources:
  - https://www.kubeflow.org/docs/components/trainer/legacy-v1/user-guides/pytorch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubeflow Training Operator: PyTorchJob

**Goal:** multi-node PyTorch training as a Kubernetes resource. PyTorchJob is a Kubernetes custom resource to run PyTorch training jobs; the Kubeflow implementation lives in the training-operator. The page documenting it is marked "Old Version": it covers Training Operator V1, and Kubeflow Trainer V2 is the current line (the docs link a V1-to-V2 migration guide).

## PyTorchJob (Training Operator v1)
```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata: {name: llm-ft, namespace: team-a}
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
          - name: pytorch                       # container is named "pytorch"
            image: registry/llm-ft:1.4.0
    Worker:
      replicas: 3
      restartPolicy: OnFailure
      template: {}          # same pod spec as Master (copy it; omitted here for brevity)
```
- Replica types are `Master` and `Worker`; the docs sample uses `restartPolicy: OnFailure` for both and a container named `pytorch`.
- Running the docs example creates pods labelled `training.kubeflow.org/job-name=<job>` and `training.kubeflow.org/replica-type=master|worker`; read master logs with `kubectl logs -f` on the pod with `replica-index=0`.
- Inspect status with `kubectl get -o yaml pytorchjobs <name>`: the `status.conditions` list shows Created, Running and Succeeded.
- **Istio trap:** PyTorchJob does not work in a user namespace by default because of automatic Istio sidecar injection; add the annotation `sidecar.istio.io/inject: "false"` to the PyTorchJob pods or the namespace.

## Failures and restarts
A pod failure restarts per `restartPolicy`; whole-job progress depends on your checkpoints. Save checkpoints to shared storage (object store or PVC) regularly and resume from the latest on start.

## Kubeflow Trainer v2
New platforms should evaluate Kubeflow Trainer V2 and its migration guide; V1 PyTorchJob remains in use. Check the Trainer docs for the V2 resource names and Python SDK.

## Verify
- [ ] All ranks log the same world size and distinct ranks.
- [ ] Killing a worker pod leads to restart and resume from checkpoint.

## Checked
2026-11-01. Confirmed on the Kubeflow legacy-v1 PyTorchJob guide: `kubeflow.org/v1`, `PyTorchJob`, `pytorchReplicaSpecs` Master/Worker, `restartPolicy: OnFailure`, container name `pytorch`, the job-name/replica-type/replica-index labels, status conditions, the Istio annotation, the "Old Version" note and the Trainer V2 pointer. Removed (not on the page): `runPolicy`/`backoffLimit`, injected `MASTER_ADDR`/`WORLD_SIZE` env claims, `elasticPolicy` fields, torchrun flags, `/dev/shm` 64 MB note, Kueue label, `TrainJob`/`ClusterTrainingRuntime`/JobSet details.
Method: documentation only; no commands were run.

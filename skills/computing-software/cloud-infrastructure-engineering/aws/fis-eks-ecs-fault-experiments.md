---
id: computing-software.cloud-infrastructure-engineering.aws.fis-eks-ecs-fault-experiments
name: fis-eks-ecs-fault-experiments
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fault-injection-service, fis, chaos-engineering, eks-fault-injection, ecs-fault-injection, pod-delete, pod-network-latency, ecs-task-actions, kubernetes-rbac, stop-conditions, game-day]
level: advanced
status: docs-checked
description: "Run AWS FIS experiments against EKS pods and ECS tasks: pod delete/stress/network actions with RBAC setup, ECS task actions with the SSM agent sidecar, targets, stop conditions."
sources: ["https://docs.aws.amazon.com/fis/latest/userguide/eks-pod-actions.html", "https://docs.aws.amazon.com/fis/latest/userguide/ecs-task-actions.html", "https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html", "https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIS fault experiments on EKS and ECS

**Goal:** prove that a containerised service survives pod/task loss, CPU or memory
pressure and network latency/blackholes, with a stop condition that halts the experiment
if customer-facing alarms fire.

## 1. EKS pod actions
Actions: `aws:eks:pod-delete`, `aws:eks:pod-cpu-stress`, `aws:eks:pod-memory-stress`,
`aws:eks:pod-io-stress`, `aws:eks:pod-network-latency`, `aws:eks:pod-network-packet-loss`,
`aws:eks:pod-network-blackhole-port`; plus node-level `aws:eks:terminate-nodegroup-instances`
and `aws:eks:inject-kubernetes-custom-resource`.

Setup:
1. A Kubernetes service account in the target namespace with an RBAC Role allowing what
   FIS needs (the rules below follow the guide's example; copy them from the guide):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: {name: fis-experiment-role, namespace: checkout}
rules:
- apiGroups: [""]
  resources: [configmaps]
  verbs: [get, create, patch, delete]
- apiGroups: [""]
  resources: [pods]
  verbs: [create, list, get, delete, deletecollection]
- apiGroups: [""]
  resources: [pods/ephemeralcontainers]
  verbs: [update]
- apiGroups: [""]
  resources: [pods/exec]
  verbs: [create]
- apiGroups: [apps]
  resources: [deployments]
  verbs: [get]
```
   Bind it with a RoleBinding to the service account and to the Kubernetes user the guide
   names (`fis-experiment`), which the FIS experiment role must be mapped to in the cluster.
2. Experiment template target and action:
```json
"targets": {"checkoutPods": {"resourceType": "aws:eks:pod", "selectionMode": "PERCENT(50)",
   "parameters": {"clusterIdentifier": "prod", "namespace": "checkout",
                  "selectorType": "labelSelector", "selectorValue": "app=checkout", "targetContainerName": "app"}}},
"actions": {"latency": {"actionId": "aws:eks:pod-network-latency",
   "parameters": {"duration": "PT5M", "delayMilliseconds": "200", "jitterMilliseconds": "20",
                  "kubernetesServiceAccount": "fis-sa", "interface": "eth0"},
   "targets": {"Pods": "checkoutPods"}}}
```
All pod actions except `pod-delete` work through an ephemeral container injected into the target pod.
The target pod's `securityContext` must set `readOnlyRootFilesystem: false` or every EKS pod
action fails. The network actions (`pod-network-blackhole-port`, `pod-network-latency`,
`pod-network-packet-loss`) do not work with Fargate. Set `maxErrorsPercent` above its default
of 0 if the action should tolerate failed injections.

## 2. ECS task actions
Actions: `aws:ecs:task-cpu-stress`, `task-io-stress`, `task-kill-process`,
`task-network-blackhole-port`, `task-network-latency`, `task-network-packet-loss`; plus
`aws:ecs:stop-task` and `aws:ecs:drain-container-instances`.
Setup for the `task-*` actions:
- Add the **SSM agent as a sidecar** container to the task definition (image
  `public.ecr.aws/amazon-ssm-agent/amazon-ssm-agent`) with a managed-instance role, as in
  the guide's template; FIS drives the faults through SSM.
- Set `pidMode: task` in the task definition (required for `task-kill-process` and the network
  actions). For network actions on Fargate also set `enableFaultInjection: true` on the task definition
  and the action parameter `useEcsFaultInjectionEndpoints` to `true`. The network blackhole action
  cannot be used with `networkMode: bridge`.
- Target `aws:ecs:task` by cluster/service or tags.

## 3. Stop conditions and safety
```json
"stopConditions": [{"source": "aws:cloudwatch:alarm", "value": "arn:aws:cloudwatch:<REGION>:<ACCOUNT_ID>:alarm:checkout-slo-burn"}]
```
- Start at small blast radius (`COUNT(1)`, `PERCENT(10)`), staging first.
- Scope the experiment role to the target cluster; log experiments with `logConfiguration`.
- Write a hypothesis: "p99 stays < 800 ms and error rate < 0.5% with 200 ms latency on 50% of pods".

## Gotchas
- `pod-delete` against a Deployment with 1 replica proves nothing but an outage; check
  PodDisruptionBudgets and replica counts first.
- ECS task actions need the SSM agent container: it registers the task as an SSM managed instance
  tagged `ECS_TASK_ARN`, which is how FIS resolves the target.

## Verify
- [ ] Experiment `completed`; stop condition tested by forcing the alarm into ALARM mid-run (experiment `stopped`).
- [ ] Service SLO alarms stayed green during pod-delete of 50% of replicas.
- [ ] Findings (timeouts, retry storms) recorded with fixes and a re-run scheduled.

## Checked
2026-10-28: Confirmed against the FIS User Guide pages eks-pod-actions, ecs-task-actions, fis-actions-reference and stop-conditions: the EKS pod action IDs, inject-kubernetes-custom-resource and terminate-nodegroup-instances, ECS task action IDs plus stop-task and drain-container-instances, the RBAC example rules (configmaps, pods, ephemeralcontainers, exec, deployments get), ephemeral-container mechanism, readOnlyRootFilesystem false requirement, Fargate limitation for EKS network actions, SSM agent sidecar image, pidMode task, enableFaultInjection and useEcsFaultInjectionEndpoints for Fargate, the aws:cloudwatch:alarm stop condition source. Read end to end. Error fixed: the RBAC rules lacked the apps/deployments get rule and the readOnlyRootFilesystem condition was described backwards. Removed as unconfirmed: the access-entry command with a made-up group, Pod Security admission claim, Chaos Mesh/Litmus remark, per-action-minute billing note, and error-message claims.

Method: documentation only; no commands were run.

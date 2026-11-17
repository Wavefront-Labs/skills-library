---
id: computing-software.cloud-infrastructure-engineering.kubernetes.init-container-patterns
name: init-container-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, init-containers, init-container-patterns, db-migration-init, wait-for-dependency, config-rendering, ckad]
level: practitioner
status: docs-checked
description: "Apply init container patterns well: wait-for-dependency with timeouts, config rendering into emptyDir, permissions fixes, and database migrations without racing replicas."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/init-containers/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-initialization/", "https://kubernetes.io/docs/tasks/configure-pod-container/security-context/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Init container patterns

Init containers run sequentially, each to completion, before app containers start. They support
resource limits, volumes and security settings like app containers, but regular init containers
do not support `lifecycle`, `livenessProbe`, `readinessProbe` or `startupProbe`. Use them for
**preconditions**, not daemons (native sidecars are for those).

## 1. Wait for a dependency (bounded)
```yaml
initContainers:
- name: wait-db
  image: busybox:1.28
  command: ['sh','-c','for i in $(seq 1 60); do nslookup mydb && exit 0; sleep 2; done; echo mydb not found; exit 1']
```
The Kubernetes docs use an `nslookup` loop against a Service name in the same way. A bounded
loop with a non-zero exit fails visibly; an unbounded `until` loop leaves the Pod in
`Init:0/1` indefinitely. If a failed init container exits with the Pod `restartPolicy` set to
`Never`, the whole Pod is treated as failed; otherwise the kubelet keeps retrying it (with the
Pod policy `Always`, init containers use `OnFailure`). `activeDeadlineSeconds` on the Pod
bounds init containers failing forever, but it also applies after init has finished, so the docs
recommend it only for Job-style workloads. Making the app retry its own connections is better than
waiting at startup.

## 2. Render config into a shared volume
```yaml
initContainers:
- name: render
  image: <template-tool-image>
  args: ["<render args>"]
  env: [{name: POD_IP, valueFrom: {fieldRef: {fieldPath: status.podIP}}}]
  volumeMounts: [{name: tmpl, mountPath: /tmpl}, {name: config, mountPath: /config}]
containers:
- name: app
  volumeMounts: [{name: config, mountPath: /etc/app, readOnly: true}]
volumes:
- {name: config, emptyDir: {}}
- {name: tmpl, configMap: {name: app-tmpl}}
```
The docs list this use: place values such as `POD_IP` into a configuration and generate the
app's file with a template tool.

## 3. Fix volume permissions (last resort)
Prefer `fsGroup` with `fsGroupChangePolicy: OnRootMismatch` (only changes permissions and
ownership if the volume root does not already match), because recursive ownership changes slow
Pod startup on large volumes. An init container running `chown` is the fallback.

## 4. Database migrations
Running migrations in an init container of a Deployment with N replicas means N Pods run the
migration on every rollout and scale-up. That is safe only if the migration tool takes a
database lock and is idempotent. Better patterns:
- a **Job** run before the rollout (a Helm `pre-upgrade` hook, or an Argo CD `PreSync` hook, which
  stops the sync if it fails), with `backoffLimit` and the same image tag;
- expand/contract migrations so old and new code both work during the rollout.

## Gotchas
- If the Pod restarts (or is restarted), all init containers execute again, so they must be
  idempotent; code that writes into an `emptyDir` must tolerate existing output files.
- The Pod's effective request or limit for a resource is the higher of the sum of app
  containers and the highest init container value.
- An init container with container-level `restartPolicy: Always` is a native sidecar, a
  different feature. Only the `image` field of an init container can be changed on a live Pod.
- A Pod that is initializing is `Pending` with condition `Initialized` false, and cannot be Ready.

## Verify
- [ ] `kubectl get pod` never shows `Init:` states lasting longer than the wait budget.
- [ ] Two simultaneous rollouts do not run migrations concurrently (lock observed in DB logs).

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Init Containers" and "Configure a Security
Context for a Pod or Container", Helm "Chart Hooks" and Argo CD "Resource Hooks" (current
docs; latest Kubernetes release v1.37.1). Confirmed: sequential completion, unsupported fields,
restart behaviour, `activeDeadlineSeconds` caveat, idempotency, effective resource rule,
`fsGroupChangePolicy: OnRootMismatch`, `pre-upgrade` and `PreSync` hooks. Removed unconfirmed
named tools (template image, migration tools that lock), `nc`, and the failure-state wording.
Method: documentation only; no commands were run.

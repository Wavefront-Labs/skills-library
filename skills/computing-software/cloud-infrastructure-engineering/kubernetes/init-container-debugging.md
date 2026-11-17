---
id: computing-software.cloud-infrastructure-engineering.kubernetes.init-container-debugging
name: init-container-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, init-containers, init-crashloopbackoff, init-error, pod-debugging, cka]
level: practitioner
status: docs-checked
description: "Debug pods stuck in Init:N/M, Init:Error or Init:CrashLoopBackOff: read init container status and logs, find which one failed, and reproduce it interactively."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-init-containers/", "https://kubernetes.io/docs/concepts/workloads/pods/init-containers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging init containers

## Status strings
| STATUS | Meaning |
|---|---|
| `Init:1/3` | 3 init containers, 1 completed so far |
| `Init:Error` | an init container has failed to execute |
| `Init:CrashLoopBackOff` | an init container has failed repeatedly |
| `Pending` | the pod has not yet begun executing init containers |
| `PodInitializing` or `Running` | init containers have finished |

## Find the failing one
```bash
kubectl get pod p -o jsonpath='{range .status.initContainerStatuses[*]}{.name}{"\t"}{.ready}{"\t"}{.restartCount}{"\t"}{.state}{"\n"}{end}'
kubectl describe pod p | sed -n '/Init Containers/,/Containers:/p'
kubectl logs p -c wait-db               # init container logs need -c
kubectl logs p -c wait-db --previous    # previous attempt if it restarted
```
`describe` shows `Exit Code`, `Reason` (Error/OOMKilled), and `Last State`.

## Typical causes
- Waiting loop on a dependency that is down or wrong DNS name → stuck `Init:0/1` with no
  error (unbounded loop). Test from a throwaway pod in the same namespace, with the same
  labels (so the same NetworkPolicies apply): `nslookup`/`nc -zv <host> <port>`.
- NetworkPolicy default-deny blocks the init container's egress (DNS too).
- Missing ConfigMap/Secret key → `CreateContainerConfigError` on the init container.
- Migration failures: read the tool's output in logs; the DB may be half-migrated — fix
  forward, don't just delete the pod.
- OOMKilled: init containers have their own `resources` — templates often forget them and a
  LimitRange default (e.g. 128Mi) kills a migration tool.

## Reproduce interactively
```bash
# override the command of the init container in a copy of the pod spec:
kubectl get pod p -o yaml > p.yaml   # edit: initContainers[x].command: ["sleep","3600"]; strip status/uid
```

## Gotchas
- App containers have not started while init containers run, so pass `-c <init-container>` to read logs.
- If the Pod restarts, all init containers must execute again; if init succeeded once and the app
  fails, look at app containers.
- A failed init container is retried according to the pod `restartPolicy`; with `Never` the whole pod is treated as failed.

## Verify
- [ ] Each init container has bounded runtime, explicit resources, and logs the reason before exiting non-zero.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Init status strings (`Init:N/M`, `Init:Error`, `Init:CrashLoopBackOff`, `PodInitializing`) and `-c <init-container>` for
  logs: debug-init-containers page.
- All init containers run again when the pod restarts; retry behaviour and `restartPolicy: Never` marking the pod failed:
  init-containers concept page.
- Removed: the quoted `kubectl logs` error text and the `kubectl debug --copy-to --container` recipe for init
  containers, which the docs do not show for init containers.

Method: documentation only; no commands were run.

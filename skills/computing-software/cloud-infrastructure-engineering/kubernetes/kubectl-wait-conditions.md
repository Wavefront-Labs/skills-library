---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-wait-conditions
name: kubectl-wait-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl, kubectl-wait, rollout-status, ci-cd]
level: practitioner
status: docs-checked
description: "Block scripts and pipelines until resources are ready with kubectl wait: --for condition, delete, jsonpath and create, timeouts, selectors and common pitfalls."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_wait/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/wait", "https://kubernetes.io/docs/concepts/workloads/controllers/job/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl wait

```bash
kubectl wait --for=condition=Available deployment/web --timeout=5m
kubectl wait --for=condition=Ready pod -l app=web --timeout=120s
kubectl wait --for=condition=Complete job/migrate --timeout=10m
kubectl wait --for=condition=Established crd/certificates.cert-manager.io
kubectl wait --for=delete pod/old-0 --timeout=60s
kubectl wait --for=jsonpath='{.status.phase}'=Running pod/db-0
kubectl wait --for=jsonpath='{.status.loadBalancer.ingress[0].ip}' svc/web --timeout=5m   # non-empty
kubectl wait --for=create pod/web-0 --timeout=60s
kubectl wait --for=condition=Ready=false pod/x             # wait for a False condition
```

## Pitfalls
- Waiting on pods with `-l` right after `kubectl apply` races: if no pods exist yet, `wait`
  errors with `no matching resources found`. Wait on the controller instead
  (`deployment ... Available`) or use `kubectl rollout status`.
- `condition=Complete` never fires for a failed Job; wait for either outcome:
  ```bash
  kubectl wait --for=condition=Complete job/migrate --timeout=10m &
  kubectl wait --for=condition=Failed job/migrate --timeout=10m && exit 1 &
  wait -n
  ```
- The `Available` condition does not tell you a rollout has finished. For rollouts use
  `kubectl rollout status deploy/web --timeout=5m`.
- CRDs: after applying a CRD, wait for `Established` before creating CRs.
- Scripts must check the exit status of `kubectl wait`.

## In CI
```bash
kubectl apply -f manifests/ && kubectl rollout status deploy/web -n shop --timeout=10m || { kubectl -n shop describe deploy/web; kubectl -n shop get events --sort-by=.lastTimestamp | tail -30; exit 1; }
```

## Checked
Checked 2026-10-24 against the kubectl wait source (main) and Kubernetes documentation v1.37: `--for` forms create, delete, condition=name[=value] (default true) and jsonpath='{...}'[=value] (no value matches any non-empty result), several `--for` flags, the `no matching resources found` error, the Job `Failed` condition. Removed the unconfirmed exit-code and Deployment Available wording.
Method: documentation only; no commands were run.

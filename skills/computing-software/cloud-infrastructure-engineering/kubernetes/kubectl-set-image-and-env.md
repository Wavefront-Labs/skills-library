---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-set-image-and-env
name: kubectl-set-image-and-env
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, deployment, kubectl-set-image, kubectl-set-env, rollout, rolling-update]
level: practitioner
status: docs-checked
description: "Trigger and control rollouts with kubectl set image, set env, set resources and set serviceaccount, record intent, and avoid drift with GitOps."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_set/", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#updating-a-deployment", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/set", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl set image, env and resources

## Commands
```bash
kubectl set image deployment/web web=registry.example.com/web:1.4.2          # container=image
kubectl set image deployment/web '*=registry.example.com/web:1.4.2'           # all containers
kubectl set image deploy/web web=... --dry-run=server -o yaml | kubectl diff -f -
kubectl set env deployment/web LOG_LEVEL=debug
kubectl set env deployment/web --from=configmap/web-config --prefix=APP_
kubectl set env deployment/web LOG_LEVEL-                                     # remove
kubectl set env deployment/web --list
kubectl set resources deployment/web -c web --requests=cpu=200m,memory=256Mi --limits=memory=512Mi
kubectl set serviceaccount deployment/web web-sa
```
Each changes the pod template, so each triggers a rollout (one rollout per command; batch
multiple changes with `kubectl rollout pause` / `resume`).

## Follow and record
```bash
kubectl rollout status deployment/web --timeout=5m
kubectl annotate deployment/web kubernetes.io/change-cause="web 1.4.2: fix login" --overwrite
kubectl rollout history deployment/web
```

## Init containers and other kinds
`set image` and `set env` accept pods, replication controllers, Deployments, DaemonSets, StatefulSets, CronJobs and ReplicaSets (Jobs are not in the list).

## Gotchas
- List container names with
  `kubectl get deploy web -o jsonpath='{.spec.template.spec.containers[*].name}'` before `set image`.
- Under GitOps, imperative changes diverge from the repository; commit the change there too.
- `set env --from=secret/x` injects keys as `secretKeyRef` references rather than copying values (`--keys` limits which keys; `--prefix` prefixes names).
- A rollout starts only when the pod template changes; use `kubectl rollout restart` to recreate pods without a template change.

## Checked
Checked 2026-10-24 against the kubectl set image and set env source (main) and the Deployment page (v1.37): supported resource kinds, `container=image` and `*=image` forms, `set env` flags `--from`, `--prefix`, `--keys`, `--list`, `--containers`, secretKeyRef/configMapKeyRef injection, a rollout is triggered if and only if the pod template changes, pause and resume to batch changes, `kubernetes.io/change-cause`. Removed the Jobs claim, the init-container and Argo CD/Flux claims and the error text.
Method: documentation only; no commands were run.

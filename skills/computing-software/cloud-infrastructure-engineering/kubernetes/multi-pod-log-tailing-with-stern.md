---
id: computing-software.cloud-infrastructure-engineering.kubernetes.multi-pod-log-tailing-with-stern
name: multi-pod-log-tailing-with-stern
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, logging, stern, kubetail, kubectl-logs, multi-pod-logs, troubleshooting]
level: practitioner
status: docs-checked
description: "Tail logs across many pods and containers at once with stern (regex queries, selectors, filters, JSON output) and the kubectl logs flags that cover simple cases."
sources: ["https://github.com/stern/stern", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tailing logs across pods with stern

## kubectl logs covers the simple cases
```bash
kubectl logs -f deploy/web                          # ONE pod of the deployment
kubectl logs deploy/web --all-pods                  # every pod of the deployment (sets --prefix)
kubectl logs -l app=web --all-containers --prefix -f --max-log-requests=20 --tail=50
kubectl logs web-1 -c app --previous                # last crashed instance
kubectl logs web-1 --since=15m --timestamps
```
Limits: with `-l`, `--tail` defaults to 10 lines per pod, and `--max-log-requests` (concurrent
streams when following by selector) defaults to 5.

## stern
```bash
kubectl krew install stern     # or brew install stern
stern web -n shop                                  # pod name regex; new pods are tailed automatically
stern -l app.kubernetes.io/name=web -n shop -c app # selector + container regex
stern . -A --since 10m --include 'ERROR|panic' --exclude healthz
stern 'web|api' -n shop --tail 20 --timestamps
stern web -o raw | jq -r 'select(.level=="error")'  # raw = message only, for JSON app logs
stern web --template '{{.PodName}} {{.ContainerName}} {{.Message}}{{"\n"}}'
stern deployment/web -n shop                       # resource/name syntax
stern web --container-state terminated --tail 100  # crash investigation
stern web --exclude-container istio-proxy
```
Colour-coded per pod; deleted pods drop out and new pods are added, which suits deploys and
incident triage. Resource queries accept `pod`, `replicationcontroller`, `service`, `daemonset`,
`deployment`, `replicaset`, `statefulset` and `job`.

## Gotchas
- Live tailing reads from the kubelet; logs are gone when the pod is deleted or rotated
  (kubelet `containerLogMaxSize` 10Mi / `containerLogMaxFiles` 5). For history use the log
  backend (Loki/OpenSearch).
- Every tailed container is a separate log stream through the apiserver; scope queries.
- RBAC (stern's README): `get`, `watch`, `list` on `pods` and `pods/log`.

## Verify
- [ ] During a rollout, `stern -l app=web` shows logs from new pods without restarting the command.

## Checked
2026-10-27, against the stern README (stern/stern master), the `kubectl logs` reference and the kubelet configuration reference (kubernetes/website main, v1.38 dev tree). Confirmed: stern query forms and supported resources, automatic tailing of new pods, `--include`, `--exclude`, `--exclude-container`, `--container-state`, `--template` fields, `-o raw`, the RBAC rules; kubectl `--all-pods`, `--prefix`, `--max-log-requests` default 5, `--tail` default 10 with a selector; kubelet `containerLogMaxSize` 10Mi and `containerLogMaxFiles` 5.
Method: documentation only; no commands were run.

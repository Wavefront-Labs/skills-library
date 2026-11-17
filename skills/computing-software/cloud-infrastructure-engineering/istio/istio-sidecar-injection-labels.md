---
id: computing-software.cloud-infrastructure-engineering.istio.istio-sidecar-injection-labels
name: istio-sidecar-injection-labels
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, sidecar-injection, istio-injection, namespace-label]
level: practitioner
status: docs-checked
description: "Label a namespace for sidecar injection with istio-injection or a revision label, restart workloads, and understand label precedence."
sources: ["https://istio.io/latest/docs/ops/common-problems/injection/", "https://istio.io/latest/docs/setup/upgrade/canary/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A namespace opts in with a label; the `istio-sidecar-injector` webhook (calling istiod) injects pods created in matching namespaces. Existing pods are not touched, so restart them.

```sh
kubectl label namespace shop istio-injection=enabled --overwrite
kubectl rollout restart deployment -n shop
kubectl get namespace -L istio-injection
```

Moving a namespace to a revision: `kubectl label namespace shop istio-injection- istio.io/rev=<revision>`, then restart. The `istio-injection` label must be removed because it takes precedence over `istio.io/rev` for backward compatibility. The revision tag `default` also injects for `istio-injection=enabled`, `sidecar.istio.io/inject=true` and `istio.io/rev=default`.

Gotchas: the per-pod override `sidecar.istio.io/inject` (`"true"` forces, `"false"` suppresses) must be in the pod template's metadata; the Deployment's own metadata is ignored. Automatic injection is ignored for pods in `kube-system` and `kube-public` and for pods with `hostNetwork: true`. Whether a namespace needs the label depends on the webhook's `namespaceSelector` (opt-in `istio-injection: enabled`, or opt-out `istio-injection NotIn [disabled]`).

Check results with `istioctl proxy-status`, as the canary guide does for revision migration.

## Checked

2026-11-03. Confirmed against the Sidecar Injection Problems page and the Canary Upgrades guide: label precedence, restart step, per-pod override placement, excluded namespaces and host network, default tag selectors. Removed: the `istio-init`/CNI container remark, the SYNCED claim, and the policy-engine and Job/CronJob advice, which neither page covers.
Method: documentation only; no commands were run.

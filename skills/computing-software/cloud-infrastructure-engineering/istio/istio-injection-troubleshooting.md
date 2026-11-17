---
id: computing-software.cloud-infrastructure-engineering.istio.istio-injection-troubleshooting
name: istio-injection-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, injection-troubleshooting, istio-sidecar-injector, webhook]
level: practitioner
status: docs-checked
description: "Diagnose pods missing a sidecar or failing admission: namespace labels, injector config policy, webhook caBundle and kube-apiserver proxy settings."
sources: ["https://istio.io/latest/docs/ops/common-problems/injection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Work from the cheapest check outward (all from Istio's Sidecar Injection Problems page).

```sh
kubectl get namespace -L istio-injection
kubectl get mutatingwebhookconfiguration istio-sidecar-injector -o yaml | grep "namespaceSelector:" -A5
kubectl -n istio-system get configmap istio-sidecar-injector -o jsonpath='{.data.config}' | grep policy:
kubectl get events -n shop
```

Unexpected result (no sidecar, or an unwanted one):
- Injection is ignored for pods in `kube-system` and `kube-public`, and for pods with `hostNetwork: true`.
- Read the webhook `namespaceSelector`: opt-in matches `istio-injection: enabled`; opt-out uses `istio-injection NotIn [disabled]`. Label namespaces to match, for example `kubectl label namespace default istio-injection=enabled --overwrite`.
- The default `policy` in the `istio-sidecar-injector` configmap is `enabled` or `disabled`; it applies only if the namespaceSelector matches, and an unrecognised value disables injection completely.
- The per-pod label `sidecar.istio.io/inject: "true"` or `"false"` overrides the policy and must be in the pod template metadata; the Deployment's metadata is ignored.

Pods cannot be created: run `kubectl describe` on the Deployment and read its events. `x509: certificate signed by unknown authority` is typically an empty or mismatched `caBundle`; compare the md5 of the webhook's `.webhooks[0].clientConfig.caBundle` with the base64 of `root-cert.pem` in the `istio-ca-root-cert` configmap, and restart the istiod pods if they differ. A `connection refused` webhook error means istiod is not running or its endpoints are not ready; check its pods, `kubectl -n istio-system get endpoints istiod` and logs.

If the kube-apiserver has proxy variables (`http_proxy`, `https_proxy`, `no_proxy`), injection fails and the only trace is a "failing open" webhook line in the kube-apiserver log. Make sure pod and service CIDRs are not proxied, for example by adding `.svc` to `no_proxy`, and restart the kube-apiserver after the change.

Startup problems when the proxy is not ready: set `holdApplicationUntilProxyStarts` (global `values.global.proxy.holdApplicationUntilProxyStarts: true`, or per pod annotation `proxy.istio.io/config: '{ "holdApplicationUntilProxyStarts": true }'`).

## Checked

2026-11-03. Confirmed against the Istio Sidecar Injection Problems page. Real error fixed: the draft's `istioctl x check-inject` command is not on the page (removed). Corrected the proxy failure mode (it fails open with a kube-apiserver log line, not silently). Removed the ReplicaSet-events advice and the unsourced verify step.
Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.istio.istio-peerauthentication-strict-mtls
name: istio-peerauthentication-strict-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, peerauthentication, strict-mtls, mtls]
level: practitioner
status: docs-checked
description: "Enforce STRICT mTLS mesh-wide, per namespace or per workload with PeerAuthentication, including port-level exceptions and policy precedence."
sources: ["https://istio.io/latest/docs/tasks/security/authentication/authn-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default (auto mutual TLS) Istio configures client proxies to send mTLS to workloads that have sidecars and plain text to those without, but workloads can still receive plain text. PeerAuthentication with `mtls.mode: STRICT` makes a workload accept only mTLS.

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata: {name: default, namespace: istio-system}
spec:
  mtls: {mode: STRICT}
```

Scope: a policy with no selector in the root namespace (`istio-system` unless you changed it at install) is mesh-wide. The same spec in another namespace is namespace-wide. Adding `selector.matchLabels` targets one workload (for example `app: httpbin`). A workload-specific policy takes precedence over a namespace-wide one: in the task, a `mode: DISABLE` policy for httpbin.foo overrode a STRICT namespace policy and curl from the sidecar-less legacy namespace succeeded again.

Per-port: `portLevelMtls` (for example `8080: {mode: DISABLE}` alongside `mtls: {mode: STRICT}`) requires mTLS on all ports except that one. The port is the container's port, and `portLevelMtls` only works if the port is bound to a Service; Istio ignores it otherwise.

Gotcha: clients without a sidecar fail against STRICT workloads, in the task with `curl` exit code 56 and HTTP code 000. A presence of the `X-Forwarded-Client-Cert` header on the upstream request is evidence mTLS was used; it is absent when the server has no sidecar. Check that no DestinationRule overrides TLS for your hosts before testing, and list policies with `kubectl get peerauthentication --all-namespaces`.

## Checked

2026-11-03. Confirmed against the Istio Authentication Policy task: auto mTLS, mesh/namespace/workload STRICT policies, portLevelMtls rules, precedence, exit code 56 for sidecar-less clients, XFCC header evidence. Removed: the PERMISSIVE-first rollout order, kubelet probe remark, "silently re-opens" claim, the `istioctl x describe` verify step and the Kiali/metric-label advice, none of which the page covers.
Method: documentation only; no commands were run.

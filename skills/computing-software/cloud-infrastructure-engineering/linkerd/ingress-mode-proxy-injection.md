---
id: computing-software.cloud-infrastructure-engineering.linkerd.ingress-mode-proxy-injection
name: ingress-mode-proxy-injection
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, ingress, proxy-configuration, l5d-dst-override]
level: advanced
status: docs-checked
description: "Mesh an ingress controller in ingress mode so the proxy routes by Host or l5d-dst-override, and strip the override header at the edge."
sources:
  - https://linkerd.io/2.19/reference/proxy-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Proxy ingress mode helps Linkerd work with ingress controllers that cannot be configured to use the Service port and IP as the destination. Enable it with the annotation `linkerd.io/inject: ingress` on the ingress controller's pods.

In ingress mode the proxy routes requests based on their `:authority`, `Host` or `l5d-dst-override` header rather than their original destination. This overrides the ingress container's own endpoint selection, so Linkerd performs load balancing, retries and mTLS for the real target.

Security requirement: the ingress must be configured to remove the `l5d-dst-override` header from incoming external requests. If it does not, an outside client can choose the destination, creating an open relay to cluster-local and external endpoints.

```yaml
spec:
  template:
    metadata:
      annotations:
        linkerd.io/inject: ingress
```

Other proxy settings use the same annotation mechanism. For example, to set the proxy's resources you add `config.linkerd.io/proxy-cpu-limit: '1'`, `config.linkerd.io/proxy-cpu-request: '0.2'`, `config.linkerd.io/proxy-memory-limit: 2Gi` and `config.linkerd.io/proxy-memory-request: 128Mi` to `spec.template.metadata.annotations`. For proxies injected with `linkerd inject`, use that command's flags instead.

Pick ingress mode only when the controller cannot send traffic to the Service address itself.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/reference/proxy-configuration/.

Removed or reworded: Nothing.

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.gateway-api.allowed-routes-namespaces-and-kinds
name: allowed-routes-namespaces-and-kinds
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [allowedroutes, namespaces, selector, kinds, listener, attachment]
level: practitioner
status: docs-checked
description: "Restrict which Routes attach to a listener: allowedRoutes.namespaces (Same, All, Selector), kinds, hostname overlap, and the safe label to select on."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/security.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/multiple-ns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each Listener can restrict attachment three ways:

1. **Hostname**: if the listener sets `hostname`, a Route that sets `hostnames` must overlap with it.
2. **Namespaces**: `allowedRoutes.namespaces.from` is `Same` (default, only Routes in the Gateway namespace), `All`, or `Selector` (requires `namespaces.selector`; selector is not allowed with `All` or `Same`).
3. **Kinds**: `allowedRoutes.kinds` limits Route kinds (for example only HTTPRoute).

With none specified, a listener trusts Routes from the same namespace that support the listener protocol.

```yaml
listeners:
- name: https
  protocol: HTTPS
  port: 443
  allowedRoutes:
    namespaces:
      from: Selector
      selector:
        matchLabels:
          shared-gateway-access: "true"
```

Safety: select on `kubernetes.io/metadata.name`, which is always set to the namespace name:

```yaml
selector:
  matchExpressions:
  - key: kubernetes.io/metadata.name
    operator: In
    values: [foo, bar]
```

A custom label such as `env` means anyone who can label namespaces can change which namespaces attach.

Attachment is bidirectional: the Route owner names the Gateway in `parentRefs`, and the Gateway owner allows the Route. Attachment only succeeds if both owners agree. Constraints on the Gateway are not required but are a best practice in clusters with many teams and namespaces; without `allowedRoutes`, all Routes can freely use the Gateway.

## Checked

2026-11-04. Confirmed on the Gateway API API-overview, security and multiple-namespaces pages (api-overview.md, security.md, multiple-ns.md): hostname overlap, namespaces.from values and selector rule, kinds, default trust, kubernetes.io/metadata.name advice, bidirectional attachment, best-practice note. Removed the attachedRoutes sentence (not on the pages).

Method: documentation only; no commands were run.

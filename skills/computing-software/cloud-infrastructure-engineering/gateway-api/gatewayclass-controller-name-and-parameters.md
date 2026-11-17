---
id: computing-software.cloud-infrastructure-engineering.gateway-api.gatewayclass-controller-name-and-parameters
name: gatewayclass-controller-name-and-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [gatewayclass, controllername, parametersref, cluster-scoped]
level: practitioner
status: docs-checked
description: "Define a GatewayClass: controllerName ownership string, optional parametersRef, internet versus private classes, and how multiple classes map to controllers."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/gatewayclass.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/implementers-guide/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`GatewayClass` is cluster-scoped and defined by the infrastructure provider; it plays the role IngressClass plays for Ingress.

```yaml
kind: GatewayClass
metadata:
  name: cluster-gateway
spec:
  controllerName: "example.net/gateway-controller"
```

`spec.controllerName` selects the implementation. Its format is opaque, but implementations should claim a domain-prefixed string under a domain they control (e.g. `example.com/example-ingress`) to avoid collisions. Versioning can be encoded in the path (`example.net/gateway/v1`, `example.net/gateway/v2.1`, or unversioned for the default).

Providers can publish several classes, for example `internet` and `private`, so users choose behaviour without knowing the implementation.

Parameters go through `spec.parametersRef` (`group`, `kind`, `name`):

```yaml
spec:
  controllerName: "example.net/gateway-controller"
  parametersRef:
    group: example.net
    kind: Config
    name: internet-gateway-config
```

A custom resource for `parametersRef` is encouraged; a ConfigMap is allowed if needed. If the implementation does not support the referenced parameters object, it should mark the class not `Accepted`.

Implementers: watch all GatewayClasses and reconcile those whose `controllerName` matches. Set `Accepted: true` on each class you take and `Accepted: false` on matching classes you do not.

## Checked

2026-11-04. Confirmed on the Gateway API GatewayClass reference and implementers guide (gatewayclass.md, implementers-guide): cluster scope, controllerName guidance and versioning examples, internet/private classes, parametersRef, Accepted rules. Nothing removed.

Method: documentation only; no commands were run.

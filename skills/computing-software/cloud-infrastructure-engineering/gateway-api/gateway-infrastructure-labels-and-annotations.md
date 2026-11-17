---
id: computing-software.cloud-infrastructure-engineering.gateway-api.gateway-infrastructure-labels-and-annotations
name: gateway-infrastructure-labels-and-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [infrastructure, labels, annotations, sidecar-injection, gatewayinfrastructurepropagation]
level: practitioner
status: docs-checked
description: "Propagate labels and annotations to the Service, Deployment or load balancer a Gateway creates using spec.infrastructure (extended feature GatewayInfrastructurePropagation)."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/infrastructure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Implementations create backing infrastructure for each Gateway (in-cluster Services and Deployments, or cloud load balancer resources). The `spec.infrastructure` field lets you stamp labels and annotations onto those generated resources.

Support level: Extended, feature name `GatewayInfrastructurePropagation`. Check that your implementation supports it before relying on it.

Example that opts the generated proxy into both Istio and Linkerd injection:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: meshed-gateway
  namespace: incoming
spec:
  gatewayClassName: meshed-gateway-class
  listeners:
  - name: http-listener
    protocol: HTTP
    port: 80
  infrastructure:
    labels:
      istio-injection: enabled
    annotations:
      linkerd.io/inject: enabled
```

Use it to propagate labels and annotations to generated infrastructure, for example mesh injection, so the infrastructure fits whichever service mesh you have installed.

## Checked

2026-11-08. Read in full: the Gateway infrastructure labels and annotations guide (raw markdown on GitHub). Confirmed: the infrastructure field, labels and annotations, the Extended feature name GatewayInfrastructurePropagation, and the Istio and Linkerd example. Removed: the supportedFeatures pointer, the cost-allocation and cloud load balancer examples, and the claim that annotations are discouraged as an extension mechanism, none of which are on the page.

Method: documentation only; no commands were run.

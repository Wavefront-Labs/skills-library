---
id: computing-software.cloud-infrastructure-engineering.linkerd.gateway-api-crd-compatibility
name: gateway-api-crd-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, gateway-api, crds, compatibility, httproute]
level: practitioner
status: docs-checked
description: "Check the installed Gateway API version and match it to your Linkerd version before using HTTPRoute and GRPCRoute policy."
sources:
  - https://linkerd.io/2.19/features/gateway-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Many Linkerd features, including authorization policy, dynamic traffic routing and request timeouts, require Gateway API CRDs from `gateway.networking.k8s.io`. The two primary types are HTTPRoute and GRPCRoute.

Check what is installed:

```bash
kubectl get crds/httproutes.gateway.networking.k8s.io -o "jsonpath={.metadata.annotations.gateway\.networking\.k8s\.io/bundle-version}"
```

A Not Found error means the Gateway API is not installed. Otherwise the output is the version, to compare with this table:

| Linkerd versions | Gateway API version | HTTPRoute | GRPCRoute |
| --- | --- | --- | --- |
| 2.15 - 2.17 | 0.7 - 1.1.1 | v1beta1 | v1alpha2 |
| 2.18 - 2.19 | 1.1.1 - 1.2.1 | v1 | v1 |

If you use GRPCRoute, moving from Gateway API 1.1.1 to 1.2.0 or higher needs extra care, so read the 1.2.0 release notes first.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/features/gateway-api/.

Removed or reworded: Closing warnings not on the page.

Method: documentation only; no commands were run.

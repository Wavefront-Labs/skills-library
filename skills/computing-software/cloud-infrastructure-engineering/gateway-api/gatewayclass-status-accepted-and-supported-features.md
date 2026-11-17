---
id: computing-software.cloud-infrastructure-engineering.gateway-api.gatewayclass-status-accepted-and-supported-features
name: gatewayclass-status-accepted-and-supported-features
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [gatewayclass, status, accepted, supportedfeatures, supportedversion]
level: advanced
status: docs-checked
description: "Read GatewayClass status: Accepted lifecycle, the sorted status.supportedFeatures list (max 64), and the SupportedVersion condition for installed CRD bundle versions."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/gatewayclass.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/implementers-guide/_index.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/api-design/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Accepted.** A new GatewayClass starts with `Accepted: False` (controller has not seen it). After validation the controller sets `Accepted: True`; a bad spec leaves `False` with a `reason` and `message`.

**supportedFeatures.** Implementations publish capabilities in `status.supportedFeatures`, before or in the same update that sets `Accepted`:

```yaml
status:
  supportedFeatures:
  - name: Gateway
  - name: HTTPRoute
  - name: HTTPRoutePortRedirect
  - name: ReferenceGrant
```

Rules: each entry has `name` taken from the `pkg/features` package; the list MUST be sorted ascending by name; at most 64 entries. Publish only Gateway features here (Mesh features belong on the experimental XMesh resource; the conformance suite ignores and warns on Mesh features found on a GatewayClass). Publish a feature only when it passes conformance.

Users read this list to learn what a class can do, and the conformance suite reads it to choose tests.

**SupportedVersion.** The CRD annotation `gateway.networking.k8s.io/bundle-version` tells which release is installed. Implementations with a GatewayClass MUST publish the `SupportedVersion` condition: `status: true` means the installed CRD version is supported, `false` that it is not.

If a Gateway references a GatewayClass that is missing or not Accepted, the implementation will not reconcile it.

## Checked

2026-11-04. Confirmed on the Gateway API GatewayClass, implementers guide and API design pages (gatewayclass.md, implementers-guide, api-design): Accepted lifecycle, supportedFeatures ordering, 64-entry limit, Gateway-only features, SupportedVersion and bundle-version annotation, non-Accepted class not reconciled. Nothing removed.

Method: documentation only; no commands were run.

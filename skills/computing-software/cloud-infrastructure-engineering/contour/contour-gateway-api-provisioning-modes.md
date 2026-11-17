---
id: computing-software.cloud-infrastructure-engineering.contour.contour-gateway-api-provisioning-modes
name: contour-gateway-api-provisioning-modes
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [gateway-api, gatewayclass, gateway, static-provisioning, dynamic-provisioning, gateway-provisioner, gatewayref]
level: advanced
status: docs-checked
description: "Contour Gateway API: static vs dynamic provisioning, GatewayClass controller name, gateway.gatewayRef config, 1:1 Gateway to Contour+Envoy, 63-character name limit."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/gateway-api.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gateway API provisioning in Contour

A Contour Gateway maps 1:1 to one Contour (control plane) plus Envoy (data plane) deployment. Controller name: `projectcontour.io/gateway-controller`. Contour aims to support all core and extended Gateway API features, and implements HTTPRoute, TLSRoute, GRPCRoute and TCPRoute.

Static provisioning (operator deploys Contour and keeps it matching the Gateway; best for a single Gateway, ports 80/443, custom YAML):
1. Install the Gateway API experimental channel CRDs.
2. Create a GatewayClass with the controller name above.
3. Create a Gateway of that class.
4. Reference it in the Contour config file:

```yaml
gateway:
  gatewayRef:
    name: contour
    namespace: projectcontour
```
5. Install Contour using that config file. Example manifest: quickstart `contour-gateway.yaml`.

Dynamic provisioning (best for many Gateways, extra listener ports, fully conformant): install the Contour Gateway Provisioner (`quickstart/contour-gateway-provisioner.yaml`, bundles Gateway API CRDs), create the GatewayClass and Gateway; the provisioner deploys a Contour instance in the Gateway's namespace.

Gateway names must be 63 characters or fewer. Provisioner upgrades also upgrade the control and data planes of every Gateway it manages.

## Checked

2026-11-08: read the Contour docs config/gateway-api in full. Confirmed: 1:1 Gateway to Contour plus Envoy, controller name projectcontour.io/gateway-controller, static and dynamic provisioning steps and when each fits, gateway.gatewayRef, the provisioner deploying Contour in the Gateway namespace, the 63-character Gateway name limit, route types HTTPRoute, TLSRoute, GRPCRoute and TCPRoute, and provisioner upgrades. Removed: the rollout restart step and the port-forward service names, which belong to the separate quickstart guide.

Method: documentation only; no commands were run.

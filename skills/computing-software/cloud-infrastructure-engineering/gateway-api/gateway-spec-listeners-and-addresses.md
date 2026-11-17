---
id: computing-software.cloud-infrastructure-engineering.gateway-api.gateway-spec-listeners-and-addresses
name: gateway-spec-listeners-and-addresses
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [gateway, listeners, addresses, gatewayclassname, status]
level: practitioner
status: docs-checked
description: "Gateway spec essentials: gatewayClassName, listeners, requested addresses, what creating a Gateway provisions, and which status fields to read."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/gateway.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/getting-started/simple-gateway.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Gateway is 1:1 with the lifecycle of the configuration of infrastructure. Other resources are only configuration snippets until a Gateway links them together.

Spec fields:

- `gatewayClassName`: the GatewayClass to instantiate. It must exist and be Accepted for the implementation to reconcile the Gateway.
- `listeners`: hostnames, ports, protocol, TLS settings and which routes may attach.
- `addresses`: network addresses requested for the Gateway. The spec expresses intent and may omit addresses or TLS; the controller can fill them in.

What creation does depends on the class: call cloud APIs for a load balancer, spawn a software LB (in this or another cluster), add configuration to an existing LB, or program the SDN. The API does not say which.

Minimal Gateway plus HTTPRoute ("simple gateway"): a Gateway listening for HTTP on port 80 from a class that auto-assigns an IP, and an HTTPRoute with no hostnames or paths that sends all port-80 traffic to `foo-svc`. The IP appears in `Gateway.status`. Routes in the same namespace are trusted by default.

Status:

- `status.addresses`: addresses actually bound.
- `status.listeners`: one entry per listener, each with its own `conditions`.
- `status.conditions`: Gateway-level conditions.
- `status.attachedListenerSets`: count of attached ListenerSets, when used.

If the desired configuration cannot be achieved the Gateway shows an error state in conditions.

## Checked

2026-11-04. Confirmed on the Gateway API Gateway reference, API overview, simple gateway guide and implementers guide (gateway.md, api-overview.md, simple-gateway.md): spec fields, user-intent note, deployment models, simple example, status fields, error state, Accepted-class requirement; attachedListenerSets from the ListenerSet reference. Nothing removed.

Method: documentation only; no commands were run.

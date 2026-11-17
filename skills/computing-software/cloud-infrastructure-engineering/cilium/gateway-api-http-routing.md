---
id: computing-software.cloud-infrastructure-engineering.cilium.gateway-api-http-routing
name: gateway-api-http-routing
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, gateway-api, httproute, gateway, gatewayclass, bookinfo]
level: practitioner
status: docs-checked
description: "Expose services through a Cilium Gateway and HTTPRoute, read the gateway address from status.addresses and test path routing; EKS FQDN note."
sources:
  - https://docs.cilium.io/en/stable/network/servicemesh/gateway-api/http/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gateway API HTTP routing

Example (bookinfo app): apply `examples/kubernetes/gateway/basic-http.yaml`. It creates a Gateway `my-gateway` (GatewayClass `cilium`) listening on port 80 and two HTTPRoutes: `/details` to the `details` service, and `/` to `productpage`.

The cloud provider provisions the external address, which may take up to 20 minutes. Check:
```
kubectl get gateway my-gateway
```
`PROGRAMMED True` and an `ADDRESS` mean ready. Some providers (EKS) give a fully-qualified domain name instead of an IP.

Test:
```
GATEWAY=$(kubectl get gateway my-gateway -o jsonpath='{.status.addresses[0].value}')
curl --fail -s http://"$GATEWAY"/details/1 | jq
curl -v -H 'magic: foo' http://"$GATEWAY"\?great\=example
```
The first returns JSON from details; the second returns the productpage HTML. If the address stays empty, the LoadBalancer Service is not provisioning (see installation prerequisites).

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/network/servicemesh/gateway-api/http/. 

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.istio.istio-ingress-gateway-config
name: istio-ingress-gateway-config
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, ingress-gateway, gateway, istio-ingressgateway]
level: practitioner
status: docs-checked
description: "Configure an Istio Gateway plus VirtualService for external HTTP traffic, find the ingress address, and test with a Host header."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `Gateway` configures the edge load balancer's ports and protocols but, unlike a Kubernetes Ingress, holds no routing; a `VirtualService` bound to it routes traffic.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata: {name: web-gw}
spec:
  selector: {istio: ingressgateway}
  servers:
  - {port: {number: 80, name: http, protocol: HTTP}, hosts: ["web.example.com"]}
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata: {name: web}
spec:
  hosts: ["web.example.com"]
  gateways: [web-gw]
  http:
  - route: [{destination: {host: web, port: {number: 8080}}}]
```

Gotchas: the Gateway `selector` must match the ingress gateway pod labels. Because the VirtualService lists only `web-gw` in `gateways`, other external requests are rejected with 404. Internal mesh requests are not subject to these rules; to apply them to internal calls, add the special value `mesh` to `gateways` and add the internal hostname (for example `web.default.svc.cluster.local`) to `hosts`.

Finding the address: every Gateway is backed by a Service of type LoadBalancer. With `INGRESS_NAME=istio-ingressgateway` and `INGRESS_NS=istio-system` (the task also shows `istio-ingress`), read `.status.loadBalancer.ingress[0].ip` (or `.hostname` when the load balancer uses a host name) from that service, and the `http2` port from `.spec.ports`. Without DNS, test with `curl -s -I -HHost:web.example.com "http://$INGRESS_HOST:$INGRESS_PORT/..."`; a browser cannot send that Host header, so for browser tests the task suggests a wildcard `*` host in the Gateway and VirtualService.

## Checked

2026-11-03. Confirmed against the Istio Ingress Gateways task: Gateway and VirtualService shape, selector, 404 behaviour, `mesh` gateway note, LoadBalancer address lookup, Host-header curl and wildcard advice. Removed: `istio=ingress` selector claim, `istioctl proxy-config listener` and `kubectl get svc` verify steps, PodDisruptionBudget and health-check port (15021) advice, none of which the page covers.
Method: documentation only; no commands were run.

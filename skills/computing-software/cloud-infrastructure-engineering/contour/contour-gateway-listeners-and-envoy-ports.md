---
id: computing-software.cloud-infrastructure-engineering.contour.contour-gateway-listeners-and-envoy-ports
name: contour-gateway-listeners-and-envoy-ports
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [gateway-listeners, container-port, envoy-service, allowedroutes, projectcontour-https, httpproxy-with-gateway]
level: advanced
status: docs-checked
description: "Gateway API listener port mapping to Envoy container ports, using HTTPProxy or Ingress under a Gateway with the projectcontour.io/https protocol."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/gateway-api.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gateway listeners and Envoy ports

Every unique Gateway Listener port must be exposed by the Envoy Service and mapped to a container port Envoy listens on. Listeners `http:80` and `https:443` need service ports 80/443 mapped to container ports 8080/8443.

Container port formula:
1. add 8000 to the Listener port
2. if the result exceeds 65535, subtract 65535
3. if the result is 1023 or less, add 1023.

Rare port conflicts are possible; check Gateway status to confirm Listeners were provisioned. Dynamic provisioning keeps the Envoy service and daemonset/deployment in sync automatically; with static provisioning you must do it yourself.

Keep using HTTPProxy or Ingress while Gateway API is enabled (migration, or provisioner plus advanced HTTPProxy features) with these listeners:

```yaml
listeners:
- name: http
  protocol: HTTP
  port: 80
  allowedRoutes:
    namespaces:
      from: All
- name: https
  protocol: projectcontour.io/https
  port: 443
  allowedRoutes:
    namespaces:
      from: All
```

The Contour-specific `projectcontour.io/https` protocol carries no TLS details; TLS stays on the HTTPProxy or Ingress. This area is still evolving, so mixed-mode support is limited.

## Checked

2026-11-08: read the Contour docs config/gateway-api in full (Gateway Listeners and Routing with HTTPProxy or Ingress). Confirmed: service ports mapped to container ports 8080 and 8443, the three-step container port formula, port-conflict caveat, provisioner versus static syncing, the listener YAML with projectcontour.io/https, and TLS staying on the HTTPProxy or Ingress.

Method: documentation only; no commands were run.

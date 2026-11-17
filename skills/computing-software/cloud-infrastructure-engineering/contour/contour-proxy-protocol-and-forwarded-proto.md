---
id: computing-software.cloud-infrastructure-engineering.contour.contour-proxy-protocol-and-forwarded-proto
name: contour-proxy-protocol-and-forwarded-proto
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [proxy-protocol, use-proxy-protocol, aws-elb, x-forwarded-proto, https-destination-ports, redirect-loop, client-ip]
level: advanced
status: docs-checked
description: "Enabling PROXY protocol v1/v2 for client IPs behind a TCP load balancer, and deriving X-Forwarded-Proto from destination ports when the load balancer terminates TLS."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/proxy-proto.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PROXY protocol and X-Forwarded-Proto

A layer 7 HTTP load balancer cannot balance TLS traffic, so a layer 4 (TCP) load balancer is used when Contour handles HTTP and HTTPS. The cost is that Envoy sees the balancer's internal address as the client. PROXY protocol forwards the original client details.

- GKE: a `type: LoadBalancer` Service is a Network Load Balancer that keeps client addresses; no PROXY protocol needed (see `X-Forwarded-For` or `X-Envoy-External-Address`).
- AWS ELB: annotate the `contour` Service with `service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp` and `service.beta.kubernetes.io/aws-load-balancer-proxy-protocol: '*'`.
- Then start Contour with `contour serve --incluster --use-proxy-protocol`, which enables PROXY on all Envoy listening ports.

TLS terminated at the load balancer (for example an NLB with an ACM certificate) makes Envoy see plaintext and stamp `X-Forwarded-Proto: http`, so HTTP to HTTPS redirects loop. Derive it from the destination port in the PROXY header (requires `--use-proxy-protocol`):

```yaml
listener:
  proxy-protocol-settings:
    https-destination-ports: [443]
    http-destination-ports: [80]
```

In `ContourConfiguration` the fields are `spec.envoy.listener.useProxyProtocol` and `proxyProtocolSettings.httpsDestinationPorts`/`httpDestinationPorts`; for the Gateway provisioner use `ContourDeployment` `spec.runtimeSettings.envoy.listener`. Ports not listed keep Envoy's default.

Since Envoy sees no TLS, the HTTPProxy has no `tls` block and Contour's automatic upgrade does not apply: add a first route matching header `X-Forwarded-Proto` exact `http` with `requestRedirectPolicy` `scheme: https`, `statusCode: 301`.

## Checked

2026-11-08: read the Contour docs guides/proxy-proto in full. Confirmed: GKE behaviour, the two AWS Service annotations, contour serve --incluster --use-proxy-protocol, the X-Forwarded-Proto problem behind a TLS-terminating NLB, the proxy-protocol-settings fields, the ContourConfiguration and ContourDeployment field locations, and the redirect route. Reworded the layer 7 versus layer 4 sentence to match the guide.

Method: documentation only; no commands were run.

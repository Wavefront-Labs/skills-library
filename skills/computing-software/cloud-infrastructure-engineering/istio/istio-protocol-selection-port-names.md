---
id: computing-software.cloud-infrastructure-engineering.istio.istio-protocol-selection-port-names
name: istio-protocol-selection-port-names
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, protocol-selection, appprotocol, port-naming]
level: practitioner
status: docs-checked
description: "Declare port protocol with name prefixes or appProtocol so HTTP routing, metrics and policies apply instead of falling back to opaque TCP."
sources: ["https://istio.io/latest/docs/ops/configuration/traffic-management/protocol-selection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Istio decides protocol handling from the Service port: by explicit selection (port name or `appProtocol`) or, failing that, automatic protocol detection.

```yaml
apiVersion: v1
kind: Service
metadata: {name: api, namespace: shop}
spec:
  ports:
  - {name: http-web, port: 8080, appProtocol: http}
  - {name: grpc-api, port: 9090, appProtocol: grpc}
  selector: {app: api}
```

The two forms are the port name `<protocol>[-<suffix>]` and, on Kubernetes 1.18+, `appProtocol: <protocol>`. If both are defined, `appProtocol` takes precedence over the port name.

Gotchas: server-first protocols such as MySQL are incompatible with automatic protocol selection. Unlike sidecars, gateways cannot detect the specific HTTP protocol automatically: unless you select `http` (HTTP/1.1) or `http2`/`grpc` (HTTP/2) explicitly, gateways forward all HTTP requests using HTTP/1.1; the `useClientProtocol` option makes them follow the client protocol, which is risky for backends that do not support HTTP/2.

Verify: `istioctl proxy-config listeners <pod>` shows the listener for the port.

## Checked

2026-11-03. Confirmed in the Istio protocol selection page: name form, `appProtocol` and precedence, the Kubernetes 1.18+ note, server-first protocols, and gateway HTTP/1.1 versus HTTP/2 behaviour. Removed: the claim that undeclared ports are treated as TCP and lose retries and L7 telemetry, the 400/502 remark, the headless Service remark, `istio_requests_total` as a detection check and the CI advice (not on the page).

Method: documentation only; no commands were run.

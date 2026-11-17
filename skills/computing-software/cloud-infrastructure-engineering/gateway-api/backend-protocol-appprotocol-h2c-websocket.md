---
id: computing-software.cloud-infrastructure-engineering.gateway-api.backend-protocol-appprotocol-h2c-websocket
name: backend-protocol-appprotocol-h2c-websocket
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [appprotocol, h2c, websocket, backend-protocol, service, http2]
level: practitioner
status: docs-checked
description: "Tell the gateway which protocol a backend speaks using Service appProtocol: kubernetes.io/h2c for HTTP/2 prior knowledge and kubernetes.io/ws for WebSocket."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/backend-protocol.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/httproute.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Not all implementations automatically select the backend protocol; some disable protocols until you opt in. When a Route backend references a Kubernetes Service, set `appProtocol` on the `ServicePort`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: store
spec:
  selector:
    app: store
  ports:
  - protocol: TCP
    appProtocol: kubernetes.io/h2c
    port: 8080
    targetPort: 8080
```

Values with conformance tests:

- `kubernetes.io/h2c`: HTTP/2 Prior Knowledge (cleartext HTTP/2).
- `kubernetes.io/ws`: WebSocket over HTTP.

Support levels: Extended features `HTTPRouteBackendProtocolH2C` and `HTTPRouteBackendProtocolWebSocket`; Standard channel since v1.2.0.

The HTTPRoute reference notes the same pattern in the Experimental "Backend Protocol" section: some implementations require the backendRef to be labelled with a protocol, which for Service backends is done with `appProtocol`.

Troubleshooting: if h2c or WebSocket traffic fails against a Service backend, first check the Service port `appProtocol`, then check that your implementation supports the matching extended feature.

## Checked

2026-11-08. Read in full: the Backend Protocol guide and the HTTPRoute reference page (raw markdown on GitHub). Confirmed: not all implementations select the protocol automatically, appProtocol on the ServicePort, the kubernetes.io/h2c and kubernetes.io/ws values with conformance tests, the Extended feature names HTTPRouteBackendProtocolH2C and HTTPRouteBackendProtocolWebSocket, Standard channel since v1.2.0, and the HTTPRoute Backend Protocol section (Experimental since v1.0.0). Removed: the supportedFeatures pointer and the Backend resource protocol sentence (page not cited). The troubleshooting order is a derived suggestion.

Method: documentation only; no commands were run.

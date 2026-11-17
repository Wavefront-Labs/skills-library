---
id: computing-software.cloud-infrastructure-engineering.istio.istio-serviceentry-external-services
name: istio-serviceentry-external-services
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, serviceentry, mesh-external, external-service]
level: practitioner
status: docs-checked
description: "Add external hosts to the mesh registry with ServiceEntry so they can be routed, timed out and observed, and avoid resolution NONE spoofing."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/egress/egress-control/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A ServiceEntry puts an external host into Istio's registry so traffic monitoring and control apply to it.

```yaml
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata: {name: httpbin-ext}
spec:
  hosts: [httpbin.org]
  location: MESH_EXTERNAL
  ports: [{number: 80, name: http, protocol: HTTP}]
  resolution: DNS
```

For an external HTTPS service the task uses a second entry with port `{number: 443, name: https, protocol: HTTPS}` (host `www.google.com`), also `resolution: DNS` and `location: MESH_EXTERNAL`.

Gotchas: avoid `resolution: NONE` for external hosts. The task explains that a malicious client could set the Host header to httpbin.org while connecting to a different IP, and the sidecar would trust the header; with DNS resolution the sidecar ignores the original destination IP and resolves the host itself. Routing rules work on external hosts: a VirtualService on `httpbin.org` with `timeout: 3s` made a 5 s upstream call fail with a 504 after 3 seconds. A ServiceEntry is what lets traffic through when `meshConfig.outboundTrafficPolicy.mode` is `REGISTRY_ONLY`; see the outbound-traffic-policy skill. Changes can take a few seconds to propagate.

## Checked

2026-11-03. Confirmed against the Istio Accessing External Services task: both ServiceEntry examples, the `resolution: NONE` warning, and the 3 s timeout result (504). Real error fixed: the draft's HTTPS port used `protocol: TLS`, while the task uses `HTTPS`. Removed: invented curl and `istioctl proxy-config` verify steps and the ownership/review-date process advice.
Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-request-mirroring
name: httproute-request-mirroring
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, requestmirror, mirroring, blue-green, httprouterequestmirror]
level: practitioner
status: docs-checked
description: "Mirror live HTTPRoute traffic to a second backend with the RequestMirror filter (extended HTTPRouteRequestMirror); responses from the mirror are ignored."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-request-mirroring.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/implementers-guide/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`RequestMirror` is an Extended filter (`HTTPRouteRequestMirror`). It copies requests to another backend, useful for testing a new service with production traffic and for blue-green deployments, because it can assess performance without affecting client responses.

Guide behaviour:

- A mirrored request goes to **one single destination endpoint** within the mirror backendRef.
- Responses from the mirror backend **MUST be ignored** by the gateway.

Example outcome: all requests are forwarded to Service `foo-v1` port 8080 and also forwarded to `foo-v2` port 8080; responses come only from `foo-v1`.

```yaml
rules:
- backendRefs:
  - name: foo-v1
    port: 8080
  filters:
  - type: RequestMirror
    requestMirror:
      backendRef:
        name: foo-v2
        port: 8080
```

(Filter field layout `requestMirror.backendRef` is the one referenced in the implementer guide as `httproute.spec.rules[].filters.requestMirror.backendRef`.)

Interaction with BackendTLSPolicy: it is a union feature, so an implementation that supports both must apply a BackendTLSPolicy when the mirror `backendRef` is a Service.

Do not mirror to a service that has side effects (writes, payments); mirrored traffic is real traffic to that backend.

## Checked

2026-11-08. Read in full: the HTTP request mirroring guide and the Implementer's Guide (raw markdown on GitHub). Confirmed: RequestMirror is Extended (HTTPRouteRequestMirror); mirrored requests go to a single endpoint of the mirror backendRef; mirror responses MUST be ignored; the foo-v1/foo-v2 outcome; the field path httproute.spec.rules[].filters.requestMirror.backendRef and the BackendTLSPolicy union-feature rule for Service backends. The final warning about side effects is operational guidance derived from the guide's description of mirrored traffic, not a quotation.

Method: documentation only; no commands were run.

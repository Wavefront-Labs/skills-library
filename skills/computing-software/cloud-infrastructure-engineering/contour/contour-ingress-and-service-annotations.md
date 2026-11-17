---
id: computing-software.cloud-infrastructure-engineering.contour.contour-ingress-and-service-annotations
name: contour-ingress-and-service-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [annotations, upstream-protocol, max-connections, retry-on, response-timeout, force-ssl-redirect, websocket-routes, per-host-max-connections]
level: practitioner
status: docs-checked
description: "Contour annotations for Ingress and Service: retries, timeouts, TLS versions, force-ssl-redirect, allow-http, websocket-routes, circuit breakers, upstream-protocol h2/h2c/tls."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/annotations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour annotations reference (Ingress and Service)

Ingress annotations:
- `ingress.kubernetes.io/force-ssl-redirect`: sets Envoy `require_tls` for the vhost; takes precedence over allow-http.
- `kubernetes.io/ingress.allow-http: "false"`: no HTTP route, HTTPS only. Other values ignored.
- `projectcontour.io/response-timeout`: Go duration; Envoy default 15s; `infinity` disables.
- `projectcontour.io/retry-on`, `projectcontour.io/num-retries` (-1 disables), `projectcontour.io/per-try-timeout`: retries apply only if `retry-on` is set.
- `projectcontour.io/tls-minimum-protocol-version` (`1.3`, `1.2` default) and `tls-maximum-protocol-version` (`1.2`, `1.3` default).
- `projectcontour.io/websocket-routes`: comma-separated route paths matching the Ingress paths.
- `projectcontour.io/tls-cert-namespace`: namespace of the TLS secrets, for delegation with Ingress v1.

Service annotations (a Service maps to an Envoy cluster):
- `projectcontour.io/max-connections`, `max-pending-requests`, `max-requests`: defaults 1024.
- `projectcontour.io/max-retries`: default 3, independent of the Ingress retry annotations.
- `projectcontour.io/per-host-max-connections`: per endpoint; unlimited by default.
- `projectcontour.io/upstream-protocol.{protocol}`: value is a comma-separated list of port names or numbers. Protocols: `tls` (HTTP/1.1 over TLS), `h2` (HTTP/2 over TLS), `h2c` (cleartext HTTP/2). The HTTPProxy `services[].protocol` field takes precedence over the annotation. Validating the upstream certificate additionally needs `validation`.

Example: `projectcontour.io/upstream-protocol.h2c: "9000"`.

Prefer first-class HTTPProxy fields over annotations where they exist.

## Checked

2026-11-04. Confirmed against the Contour annotations reference (config/annotations.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.

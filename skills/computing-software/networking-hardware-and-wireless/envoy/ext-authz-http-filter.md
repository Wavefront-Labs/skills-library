---
id: computing-software.networking-hardware-and-wireless.envoy.ext-authz-http-filter
name: ext-authz-http-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, ext-authz, external-authorization, grpc-service, check-request, route-cache-clearing, include-peer-certificate]
level: practitioner
status: docs-checked
description: "Delegate request authorisation to an external gRPC or HTTP service with the ext_authz filter and avoid the route cache clearing bypass."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/ext_authz_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ext authz http filter
The ext_authz HTTP filter calls an external gRPC or HTTP service to decide if a request is authorised; unauthorised requests get `403`. The authorisation request body is a `CheckRequest`. The service can also receive custom metadata and return metadata to propagate upstream or downstream.

```yaml
http_filters:
- name: envoy.filters.http.ext_authz
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
    grpc_service:
      envoy_grpc: { cluster_name: ext-authz }
      timeout: 0.5s
    include_peer_certificate: true
- name: envoy.filters.http.router
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```
The API reference gives the default timeout of the gRPC and HTTP service as 200 ms, so set `timeout` if the auth server needs longer.

Security gotcha from the docs (route cache clearing): with per-route ext_authz configuration, later filters in the chain may clear the route cache, so a request can be re-routed to a different route that has different authorisation requirements and bypass the checks. Keep ext_authz late enough to see the final route and avoid route-mutating filters after it; read the "Filter route mutation security considerations" section.

Also decide `failure_mode_allow` deliberately: when true, error responses from the auth service are allowed through, and the `failure_mode_allowed` counter records them. Check the filter's `ext_authz` stats.

## Checked

2026-11-03. Confirmed against: ext_authz_filter.rst and ext_authz.proto (200 ms default timeout, failure_mode_allow, include_peer_certificate, route cache clearing warning). Removed or corrected: the unconfirmed fail-closed default hedge.

Method: documentation only; no commands were run.

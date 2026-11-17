---
id: computing-software.networking-hardware-and-wireless.envoy.http-compressor-filter
name: http-compressor-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, compressor, gzip, brotli, zstd, content-length, compression, compressorperroute]
level: practitioner
status: docs-checked
description: "Compress responses in Envoy with the compressor filter and disable or override it per virtual host and route."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/compressor_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http compressor filter
The compressor filter compresses responses (and optionally requests) using a pluggable library (gzip, brotli, zstd extensions). Per-route config is `CompressorPerRoute`, which sets exactly one of `disabled` or `overrides`. This example disables it on a virtual host and re-enables response compression on a route:

```yaml
virtual_hosts:
- name: local_service
  domains: ["*"]
  typed_per_filter_config:
    envoy.filters.http.compressor:
      "@type": type.googleapis.com/envoy.extensions.filters.http.compressor.v3.CompressorPerRoute
      disabled: true
  routes:
  - match: { prefix: "/static" }
    route: { cluster: service }
    typed_per_filter_config:
      envoy.filters.http.compressor:
        "@type": type.googleapis.com/envoy.extensions.filters.http.compressor.v3.CompressorPerRoute
        overrides:
          response_direction_config: {}
```
The filter's `typed_config` takes a `compressor_library` (for example gzip).

Gotchas from the docs: response compression is on by default, request compression is off. A response is skipped when the request has no `accept-encoding` containing gzip or `*` (or gzip has q=0), when the response already has `content-encoding`, has `cache-control: no-transform`, has a content type outside the selected mime types (defaults include `application/json`, `text/html`, `text/plain`), has no `content-length` or `transfer-encoding`, or is smaller than 30 bytes when not chunked. `x-envoy-compression-status` can report why when `status_header_enabled` is set in `ResponseDirectionConfig`.

## Checked
2026-11-03. Confirmed against compressor_filter.rst and the compressor.proto reference. Removed or corrected: the claim that the per-route pattern is from the docs, the router-ordering claim, the chunked/Content-Length and double-encoding claims and the curl verify step.
Method: documentation only; no commands were run.

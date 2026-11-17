---
id: computing-software.software-engineering.api-design.grpc-web-for-browser-clients
name: grpc-web-for-browser-clients
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-web, browser-clients, envoy, streaming, proxy]
level: practitioner
status: docs-checked
description: "Call gRPC services from browsers with gRPC-Web: why a proxy is needed, Envoy filter config, supported streaming modes, wire format modes and interop proxies."
sources: ["https://grpc.io/docs/platforms/web/basics/", "https://github.com/grpc/grpc-web"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC-Web for browser clients

gRPC-Web is a JavaScript implementation of gRPC for browser clients. Browser clients connect to gRPC services through a special proxy; by default that is Envoy, which supports gRPC-Web out of the box. The generated stub talks to the proxy URL, and the proxy forwards to the backend gRPC server.

## Options
1. Envoy with the gRPC-Web HTTP filter, from the grpc.io tutorial (the upstream cluster must use HTTP/2):
```yaml
http_filters:
  - name: envoy.grpc_web
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.grpc_web.v3.GrpcWeb
  - name: envoy.filters.http.router
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```
2. Other proxies: the gRPC-web Go proxy, Apache APISIX and NGINX are listed in the README as supporting the protocol.
3. Server frameworks with built-in gRPC-Web support, which removes the proxy: Armeria (JVM) and Tonic (Rust) are listed in the README.

## Wire format modes
Set with `--grpc-web_out=import_style=...,mode=...` on `protoc` (plus `protoc-gen-grpc-web`):
- `mode=grpcwebtext` (default): `Content-Type: application/grpc-web-text`, base64-encoded payloads, unary and server-streaming calls.
- `mode=grpcweb`: `Content-Type: application/grpc-web+proto`, binary protobuf, unary calls only.
`import_style` can be `closure` (default), `commonjs`, `commonjs+dts` or `typescript`.

## Capabilities
Unary and server-streaming only; server streaming requires the `grpcwebtext` mode. Client-side and bidirectional streaming are not currently supported. Deadlines are set with a `deadline` header holding a Unix timestamp in milliseconds. The `UnaryInterceptor` works only with Promise clients; `StreamInterceptor` works with regular clients.

## Gotchas
- Cross-origin pages need CORS configured on the proxy; the tutorial says only that you may need to add it.
- Promise clients cannot access the `.on(...)` callbacks for metadata and status.
- The grpc-web runtime is on npm as `grpc-web`.

Verify: from a browser page call a unary method and check the DevTools network entry has the `content-type` for the mode you generated, and that a cross-origin preflight to the proxy succeeds.

## Checked
2026-11-08. Confirmed against the grpc.io gRPC-Web basics tutorial and the grpc-web README (proxies, modes, content types, streaming limits, import styles, deadline header, interceptors, Promise limits). Corrected: server streaming needs text mode (the draft said text mode was a fallback). Removed: the Connect protocol claims (the Connect page was not readable), the Envoy CORS filter snippet, the exposed-header list, the claim that browsers cannot read trailers, and the HTTP 200 error-mapping note.
Method: documentation only; no commands were run.

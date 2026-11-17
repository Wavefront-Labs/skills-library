---
id: computing-software.cloud-infrastructure-engineering.contour.contour-grpc-routing-and-grpc-web
name: contour-grpc-routing-and-grpc-web
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [grpc, h2c, upstream-protocol, grpcroute, grpc-web, streaming, timeouts]
level: practitioner
status: docs-checked
description: "Routing gRPC through Contour: HTTPProxy services[].protocol h2c or h2, Ingress upstream-protocol annotation, GRPCRoute method matches, streaming timeouts, gRPC-Web conversion."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/grpc.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# gRPC with Contour

HTTPProxy: set `protocol` on the service. `h2c` is plaintext HTTP/2, `h2` is TLS HTTP/2. Path prefixes can target a method.

```yaml
routes:
- conditions: [{prefix: /yages.Echo/Ping}]
  services: [{name: grpc-echo, port: 9000, protocol: h2c}]
- conditions: [{prefix: /}]
  services: [{name: grpc-echo, port: 9000, protocol: h2c}]
```

Test: `grpcurl -plaintext -authority=my-grpc-service.foo.com <lb ip:port> yages.Echo/Ping`.

Ingress v1: annotate the Service with `projectcontour.io/upstream-protocol.h2c: "9000"` (or `.h2`); value is a comma-separated list of port names or numbers matching the Service.

Gateway API: use `GRPCRoute` with `parentRefs`, `hostnames`, and `matches[].method` (`service`, `method`). Add the `grpc.reflection.v1alpha.ServerReflection` / `ServerReflectionInfo` match too if grpcurl relies on reflection. Annotate the Service with the upstream protocol as for Ingress.

Streaming RPCs: raise `routes[].timeoutPolicy.response` (default 15s), and review `timeouts.request-timeout` and `timeouts.max-connection-duration` in the Contour config file, otherwise streams are cut.

gRPC-Web: Envoy automatically converts HTTP/1 gRPC-Web requests (`Content-Type: application/grpc-web-text`, base64 body) into gRPC over HTTP/2 to the upstream. You must still declare the upstream protocol, and an upstream that does not speak gRPC may produce protocol errors.

## Checked

2026-11-04. Confirmed against the Contour gRPC guide (guides/grpc.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.

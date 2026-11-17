---
id: computing-software.software-engineering.api-design.grpc-health-checking-and-grpcurl
name: grpc-health-checking-and-grpcurl
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-health-checking, grpcurl, server-reflection, kubernetes-probes]
level: practitioner
status: docs-checked
description: "Implement the standard gRPC health checking service, wire it to Kubernetes gRPC probes, decide on server reflection, and exercise services from the shell with grpcurl."
sources: ["https://grpc.io/docs/guides/health-checking/", "https://github.com/fullstorydev/grpcurl", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-grpc-liveness-probe", "https://grpc.io/docs/guides/reflection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC health checking and grpcurl

## Standard health service
gRPC specifies a standard health service API (health/v1). You are responsible for updating the
status of your services. It supports two modes: unary `Check` calls (useful for central monitoring
or load balancing, but does not scale to a fleet of clients constantly checking) and streaming
`Watch` (used by the client-side health check feature).

- Create the service with the language's health library, add it to your server, and notify the
  library whenever a service's health changes.
- Statuses: `SERVING` (open for business) and `NOT_SERVING` (cannot accept requests now).
- The empty string `""` as service name represents the health of the whole server.
- Tell the health library about shutdown so it can notify all connected clients.

Set `NOT_SERVING` while warming up or when a hard dependency is down (for readiness only).

## Client-side health checking
Set the channel's service config (JSON):
```
{"healthCheckConfig": {"serviceName": "foo"}}
```
The client then calls `Watch` on connection, sends no requests until the service is healthy, and
stops sending to a backend that becomes unhealthy. A failed `Watch` is retried with backoff unless
it returns `UNIMPLEMENTED`, which disables health checking. Some load balancing policies disable
health checking (pick_first does).

## Kubernetes probes
Native gRPC probes use a `grpc` field with a `port` (and optional `service`) in the probe spec;
the feature is stable since Kubernetes v1.27, and the probe uses plaintext by default (TLS mode needs
the `GRPCContainerProbeTLS` feature gate and does not verify the server certificate). gRPC probes
do not support named ports.

## Reflection
Reflection lets tools such as grpcurl and Postman discover a server's protobuf APIs without .proto
files. It is not enabled automatically; the server author adds a reflection service. If your API
is reachable by public users, weigh exposing it (it reveals your API surface). When routing, send the
reflection service to the same backend as the main RPC service.

## grpcurl
```
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe my.pkg.MyService
grpcurl -plaintext -d '{"id": "o1"}' localhost:50051 my.pkg.MyService/Method
grpcurl -H 'header1:value1' -d '{"id": 1}' host:443 my.pkg.MyService/Method
```
- `-plaintext` means no TLS; without it grpcurl uses TLS. Headers/metadata go in with `-H name:value`.
- Without server reflection, supply `.proto` source files or `-protoset` files.

## Checked

Date: 2026-11-01. Confirmed against the gRPC health checking and reflection guides, the grpcurl
README and the Kubernetes probe task page. Removed unconfirmed Go snippets, default `Health`
package naming, `SERVICE_UNKNOWN`, `grpc_health_probe`, the `-insecure` and `-import-path` flags and
the 1.24 version claim.
Method: documentation only; no commands were run.

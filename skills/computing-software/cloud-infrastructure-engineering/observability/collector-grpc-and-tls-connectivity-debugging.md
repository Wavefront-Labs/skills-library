---
id: computing-software.cloud-infrastructure-engineering.observability.collector-grpc-and-tls-connectivity-debugging
name: collector-grpc-and-tls-connectivity-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [grpc-connectivity-debugging, collector-tls-errors, collector-troubleshooting, otel-collector, grpc]
level: advanced
status: docs-checked
description: "Debug collector gRPC and TLS failures: decoding Unavailable, DeadlineExceeded, Unimplemented and ResourceExhausted, message size limits, proxies, grpc logging and test tools."
sources: ["https://opentelemetry.io/docs/collector/troubleshooting/", "https://grpc.github.io/grpc/core/md_doc_statuscodes.html", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configgrpc/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC and TLS connectivity debugging

## Read the status code
| Error | Usual cause |
|---|---|
| `Unavailable ... connection refused` | wrong host/port, receiver not listening on 0.0.0.0, NetworkPolicy |
| `Unavailable ... connection reset` / `EOF` | TLS client to plaintext server or vice versa; proxy dropping HTTP/2 |
| `Unavailable ... transport is closing` | server restart, idle timeout at LB, server keepalive `max_connection_age` (retried) |
| `DeadlineExceeded` | backend slow, exporter `timeout` too short, network loss |
| `Unimplemented ... unknown service opentelemetry.proto.collector...` | endpoint is not an OTLP gRPC receiver (e.g. pointing at 4318, or a Jaeger port) |
| `ResourceExhausted: grpc: received message larger than max` | batch too big; raise receiver `max_recv_msg_size_mib` (default 4) or lower `send_batch_max_size` |
| `Unauthenticated` / `PermissionDenied` | missing auth header / token |
| HTTP `415` / `404` on 4318 | wrong path (per-signal endpoint missing `/v1/traces`) or JSON vs protobuf |

## Turn up logging
Collector: `service.telemetry.logs.level: debug`. gRPC internals (Go):
see the grpc-go logging docs for its environment variables. SDKs: `OTEL_LOG_LEVEL=debug`; `GRPC_TRACE` for C-core based SDKs
(gRPC environment variables doc).

## Test tools
```bash
# send synthetic data end to end
telemetrygen traces --otlp-endpoint gw:4317 --otlp-insecure --traces 1
# raw TCP / TLS
nc -vz gw 4317
openssl s_client -connect gw:4317 -alpn h2 -servername gw.example.com </dev/null
# HTTP path
curl -v -X POST http://gw:4318/v1/traces -H 'Content-Type: application/json' -d '{"resourceSpans":[]}'
```

## Proxies and load balancers
Every hop must speak HTTP/2 end to end for gRPC: configure each proxy or load balancer for gRPC per its own docs. Idle timeouts shorter than gRPC keepalive
cause periodic `transport is closing`; set exporter `keepalive: {time: 30s, timeout: 10s}`.

## TLS specifics
See the TLS/mTLS skill for config; check expiry with `openssl x509 -enddate -noout -in cert.pem` and that the
collector picked up renewed certs (`reload_interval`).

## Checked
- 2026-10-28. Checked against OpenTelemetry Collector docs (troubleshooting, configgrpc README, batchprocessor README), the gRPC status codes and environment variables docs, and telemetrygen README (collector-contrib main, 2026-10).
- Confirmed: `max_recv_msg_size_mib`, `send_batch_max_size`, `keepalive`, `max_connection_age`, `reload_interval`, `OTEL_LOG_LEVEL`, `GRPC_TRACE`, `--otlp-insecure`, gRPC status names.
- Removed (unconfirmed): `GRPC_GO_LOG_*` variables, Java `otel.javaagent.debug`, telemetrygen `--ca-cert`, the gRPC-reflection claim, NGINX/ALB/Envoy setting names.
Method: documentation only; no commands were run.

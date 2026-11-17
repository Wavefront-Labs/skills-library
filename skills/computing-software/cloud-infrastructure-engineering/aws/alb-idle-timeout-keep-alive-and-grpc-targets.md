---
id: computing-software.cloud-infrastructure-engineering.aws.alb-idle-timeout-keep-alive-and-grpc-targets
name: alb-idle-timeout-keep-alive-and-grpc-targets
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, alb, alb-idle-timeout, grpc-target, http2, keep-alive]
level: advanced
status: docs-checked
description: "Tune ALB idle timeout against backend keep-alive to stop 502s, and route gRPC and HTTP/2 to targets with GRPC protocol-version target groups and gRPC health checks."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-load-balancer-attributes.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/rule-action-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALB idle timeout, keep-alive and gRPC targets

## 1. Idle timeout vs backend keep-alive
```bash
aws elbv2 modify-load-balancer-attributes --load-balancer-arn <ALB_ARN> --attributes \
  Key=idle_timeout.timeout_seconds,Value=120 Key=client_keep_alive.seconds,Value=3600
```
- `idle_timeout` (default 60 s, 1-4000) closes front and back connections that are idle with no data in either direction for that long.
- `client_keep_alive.seconds` (default 3600, range 60-604800) is the maximum lifetime of a persistent client connection; after it elapses the ALB accepts one more request and then closes gracefully (`Connection: close` or an HTTP/2 GOAWAY).
- Backend keep-alive **must be longer** than the ALB idle timeout. Otherwise the target closes a pooled
  connection just as the ALB reuses it: the ALB returns intermittent HTTP 502 (`HTTPCode_ELB_502_Count`).
  nginx `keepalive_timeout 125s;`, Node `server.keepAliveTimeout = 125000; server.headersTimeout = 126000;`,
  gunicorn `--keep-alive 125`.
- Long requests (exports, uploads) need an idle timeout above the longest silent gap; send at least 1 byte of data before each idle period elapses.

## 2. gRPC / HTTP/2 to targets
```bash
aws elbv2 create-target-group --name grpc-tg --protocol HTTPS --port 50051 --protocol-version GRPC \
  --vpc-id vpc-0abc --target-type ip \
  --health-check-path /grpc.health.v1.Health/Check --matcher GrpcCode=0
```
- Listener must be HTTPS; clients speak HTTP/2.
- `--protocol-version HTTP2` for plain HTTP/2 targets; `HTTP1` is the default. For gRPC and HTTP/2 target groups the only
  supported listener rule action is forward (no redirect or fixed-response).
- gRPC health check matcher: codes 0-99 or a range such as `0-5`, default 12; the default path is `/AWS.ALB/healthcheck`,
  so set a real method path or accept the default code deliberately.
- Streaming RPCs are cut by the idle timeout if no data flows; the ALB does not support HTTP/2 PING frames and they do not
  reset the idle timeout, so send application messages (or raise the timeout).

## Verify
- [ ] 502 count drops to zero after aligning keep-alive.
- [ ] `grpcurl -d '{}' api.example.com:443 grpc.health.v1.Health/Check` returns `SERVING` through the ALB.

## Checked

Checked 2026-10-27 against the Elastic Load Balancing documentation for Application Load Balancers (load balancer attributes, health checks, rule action types, troubleshooting) and the botocore elbv2 model.
- Corrected: HTTP/2 PING frames do not reset the idle timeout (send data instead); gRPC and HTTP/2 target groups support only forward actions; `client_keep_alive.seconds` range 60-604800 (default 3600).
- Confirmed: idle timeout default 60 s with range 1-4000, 502 caused by a target keep-alive shorter than the ALB idle timeout, gRPC health check path default `/AWS.ALB/healthcheck`, matcher 0-99 with default 12.

Method: documentation only; no commands were run.

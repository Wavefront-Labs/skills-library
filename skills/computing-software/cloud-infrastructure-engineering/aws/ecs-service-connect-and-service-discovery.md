---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-service-connect-and-service-discovery
name: ecs-service-connect-and-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, service-connect, cloud-map, service-discovery, service-mesh, envoy, microservices]
level: practitioner
status: docs-checked
description: "Connect ECS services by name with Service Connect (Cloud Map namespaces, client/server config, retries, metrics, TLS) or plain Cloud Map DNS discovery, and pick between them."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect-concepts-deploy.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-discovery.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS Service Connect and service discovery

## 1. Options
| | Service Connect | Cloud Map DNS service discovery | Internal ALB |
|---|---|---|---|
| Client resolves | short name via local proxy (`http://orders:8080`) | `orders.prod.local` A/SRV records | ALB DNS |
| Load balancing | proxy (round robin, outlier detection) | client-side DNS (TTL caching issues) | ALB |
| Retries/timeouts | yes, in proxy (2 retries, 15 s default timeout) | no | limited |
| Metrics | per-service in CloudWatch/ECS console | none | ALB metrics |
| Cross-cluster | same namespace, same Region, across clusters | yes | yes |
Default for ECS-to-ECS traffic: **Service Connect**.

## 2. Service Connect setup
A Cloud Map namespace in the same Region (the namespace type does not matter to Service Connect), then per service:
```json
"serviceConnectConfiguration": {
  "enabled": true,
  "namespace": "prod",
  "services": [{
    "portName": "http",
    "discoveryName": "orders",
    "clientAliases": [{"port": 8080, "dnsName": "orders"}],
    "timeout": {"idleTimeoutSeconds": 300, "perRequestTimeoutSeconds": 30}
  }],
  "logConfiguration": {"logDriver": "awslogs", "options": {"awslogs-group": "/ecs/sc-proxy", "awslogs-region": "<REGION>", "awslogs-stream-prefix": "orders"}}
}
```
- Task definition `portMappings` need `name: "http"` and `appProtocol: "http"` (or `http2`, `grpc`).
- **Client-only** services (they call others but serve nothing) set `enabled: true` with no `services`.
- ECS adds a managed proxy sidecar container to each new task; it is not in your task definition. AWS recommends adding 256 CPU units and at least 64 MiB of memory to the task size for it (512 more CPU units above about 500 requests per second per task). The task must set a task-level memory limit.
- Timeouts default to 15 s per request; `idleTimeout` defaults to 5 minutes for HTTP/HTTP2/gRPC and 1 hour for TCP. `perRequestTimeout` only applies to HTTP, HTTP2 and gRPC.
- TLS between proxies uses an AWS Private CA and requires `awsvpc` network mode.

## 3. Cloud Map DNS discovery (for non-ECS clients or simple setups)
`serviceRegistries: [{"registryArn": "arn:aws:servicediscovery:...:service/srv-..."}]` on the
service; the console only registers into private DNS namespaces, and VPC DNS support must be enabled. awsvpc tasks can register `A` or `SRV` records (bridge and host mode only `SRV`). Use ECS-managed container health checks (`HealthCheckCustomConfig`) for the Cloud Map service. ECS does not support registering into shared Cloud Map namespaces, and Cloud Map resources must be cleaned up manually. Keep the TTL low and make clients re-resolve.

## Gotchas
- Service Connect names resolve only for tasks in the same namespace that have Service Connect
  enabled and started after the latest deployment; other applications (EC2 instances, Lambda) can't resolve the short names (use Cloud Map DNS/ALB for them).
- Adding Service Connect to an existing service creates a new deployment, and existing tasks cannot resolve new endpoints until redeployed.
- Not supported: Windows containers, standalone tasks, services using CodeDeploy blue/green or external deployments. Fargate needs Linux platform 1.4.0 or later.
- Security groups still apply: allow the client service SG to the server port.

## Verify
- [ ] From a client task (`ecs execute-command`), `curl http://orders:8080/health` returns 200.
- [ ] ECS console/CloudWatch shows Service Connect traffic metrics for `orders`.
- [ ] Killing one server task: client requests succeed (proxy retries/outlier detection).

## Checked
Checked 2026-10-24 against the ECS developer guide (Service Connect overview and components, service discovery).
Confirmed: namespace type irrelevant, proxy sidecar and its recommended extra CPU and memory, round-robin and outlier detection, 2 retries, 15 s default timeout and idleTimeout defaults (5 min HTTP-like, 1 h TCP), deployment on enabling, exclusions, Cloud Map A/SRV rules, custom health checks, shared-namespace limitation.
Corrected: idle timeout example changed to match the documented default; removed the claim that TLS uses short-lived certificate mode and the specific CloudWatch metric names, which the docs reviewed do not list.

Method: documentation only; no commands were run.

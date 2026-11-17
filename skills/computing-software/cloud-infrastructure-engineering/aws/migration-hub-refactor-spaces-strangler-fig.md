---
id: computing-software.cloud-infrastructure-engineering.aws.migration-hub-refactor-spaces-strangler-fig
name: migration-hub-refactor-spaces-strangler-fig
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, refactor-spaces, strangler-fig, incremental-refactoring, api-gateway-proxy, microservices-extraction, transit-gateway, route-traffic-shifting, modernization, monolith-decomposition]
level: advanced
status: docs-checked
description: "Decompose a monolith with the strangler fig pattern on AWS: a routing facade (Refactor Spaces or API Gateway/ALB), path routes to new services, data split, rollback."
sources: ["https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/userguide/what-is-mhub-refactor-spaces.html", "https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/APIReference/Welcome.html", "https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-aspnet-web-services/fig-pattern.html", "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strangler fig with Refactor Spaces (or your own facade)

**Goal:** carve features out of a monolith one route at a time: callers hit a stable
facade, new services take over specific paths, and the monolith keeps the rest.

## 0. Availability
AWS Prescriptive Guidance states that AWS Migration Hub Refactor Spaces is no longer open to new customers as of
November 7, 2025, and points to AWS Transform for similar capabilities. Existing customers can follow section 2; for
new projects build the same facade with your own routing layer.

## 1. The pattern
The strangler fig pattern migrates a monolith to microservices incrementally by gradually extracting features and
creating a new application around the existing system, which reduces the transformation risk of a big-bang migration.
1. **Facade** in front of the monolith: all traffic goes through it from day one, routes default to the monolith.
2. **Extract** a bounded context into a new service.
3. **Route** its paths (`/orders/*`) to the new service; monitor; keep the monolith code path until confident.
4. **Delete** the dead monolith code. Repeat.
You need access to the monolith's code base: as features move out you make small changes and add an **anti-corruption
layer** that routes monolith calls to the right migrated service (for example a service-specific facade or adapter
class inside the monolith), decommissioned once all dependent services have migrated.

## 2. Refactor Spaces (existing customers)
A Refactor Spaces environment provides infrastructure, multi-account networking and routing; an application models the
strangler fig pattern and orchestrates Amazon API Gateway, Network Load Balancer and resource-based IAM policies.
Orchestrated resources (for example Transit Gateway) are provisioned in your own account, so you pay for them as well
as for Refactor Spaces usage. Resources: environment, application (proxy), services (URL or Lambda endpoints), routes.
```bash
aws migration-hub-refactor-spaces create-environment --name shop --network-fabric-type TRANSIT_GATEWAY
aws migration-hub-refactor-spaces create-application --environment-identifier <ENV> --name storefront \
  --proxy-type API_GATEWAY --vpc-id vpc-monolith --api-gateway-proxy EndpointType=REGIONAL,StageName=prod
aws migration-hub-refactor-spaces create-service --environment-identifier <ENV> --application-identifier <APP> \
  --name monolith --endpoint-type URL --url-endpoint Url=http://monolith.internal:8080 --vpc-id vpc-monolith
aws migration-hub-refactor-spaces create-route --environment-identifier <ENV> --application-identifier <APP> \
  --service-identifier <MONOLITH_SVC> --route-type DEFAULT
aws migration-hub-refactor-spaces create-service ... --name orders --endpoint-type LAMBDA --lambda-endpoint Arn=<FN_ARN>
aws migration-hub-refactor-spaces create-route ... --service-identifier <ORDERS_SVC> --route-type URI_PATH \
  --uri-path-route SourcePath=/orders,ActivationState=ACTIVE,Methods=GET,POST,IncludeChildPaths=true
```
- `--network-fabric-type` takes `TRANSIT_GATEWAY` or `NONE`; `--route-type` takes `DEFAULT` or `URI_PATH`; a route's
  `ActivationState` is `ACTIVE` or `INACTIVE` (set it with `update-route`).
- Do not hand-edit the resources Refactor Spaces creates.

## 3. Data and cross-cutting concerns
- Define which system is the source of truth per entity at every stage; write it down.
- Auth: the new service must accept the monolith's session or token.
- Watch latency at the facade: every extra hop adds to it.

## Verify
- [ ] Facade routes 100% of traffic with default to the monolith before any extraction (baseline metrics).
- [ ] The `/orders` route points at the new service and the route can be set back to inactive.

## Checked

2026-10-28. Confirmed against the Refactor Spaces User Guide what-is page (environment, application orchestrating API Gateway/NLB/IAM, provisioned resources in your account), the AWS Prescriptive Guidance strangler fig and ASP.NET fig-pattern pages (availability note dated 7 November 2025, pattern description, anti-corruption layer), and the botocore migration-hub-refactor-spaces model (NetworkFabricType, RouteType, RouteActivationState, ProxyType enums).
Removed: the "closing Migration Hub capabilities" generalisation, ALB/API Gateway HTTP API/CloudFront facade recipes, DMS/Debezium change-data-capture advice, the rollback-in-seconds claim, "deleting the environment removes the resources", JWT authorizer and p99 advice, and the sub-minute rollback verification.
Method: documentation only; no commands were run.

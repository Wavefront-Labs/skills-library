---
id: computing-software.data-engineering.snowflake.snowpark-container-services
name: snowpark-container-services
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowpark-container-services, spcs, compute-pools, image-repository]
level: sme
status: docs-checked
description: "Run containers in Snowflake with Snowpark Container Services: image repositories, compute pools, service specs, endpoints, job services, logs, and cost control."
sources:
  - https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview
  - https://docs.snowflake.com/en/developer-guide/snowpark-container-services/specification-reference
  - https://docs.snowflake.com/en/sql-reference/sql/create-compute-pool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowpark Container Services (SPCS)

**Goal:** run custom OCI container images (ML serving/training, GPU work, long-running services, batch jobs) next to your data, using Snowflake's existing RBAC, network policies and event tables.

## Objects
- **Image repository**: OCIv2-compliant registry in your account, created with `CREATE IMAGE REPOSITORY`; Docker or another OCI client pushes images to it.
- **Compute pool**: one or more VM nodes (`CREATE COMPUTE POOL`).
- **Service**: long-running; Snowflake restarts a container that exits (`CREATE SERVICE`).
- **Job service**: finite, like a stored procedure; finished when all containers exit and never restarted (`EXECUTE JOB SERVICE`).

## Image platform
Container images must match the compute pool's CPU architecture: `linux/amd64` for x86 instance families, `linux/arm64` for ARM ones. A repository image is referenced in a spec by path, e.g. `/tutorial_db/data_schema/tutorial_repository/echo_service:dev`.

## Compute pool
```sql
CREATE COMPUTE POOL scorer_pool
  MIN_NODES = 1 MAX_NODES = 3 INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = TRUE AUTO_SUSPEND_SECS = 600;
```
- Required: MIN_NODES (must be greater than 0), MAX_NODES, INSTANCE_FAMILY. The family sets resources and therefore credits consumed while the pool runs; list families with `SHOW COMPUTE POOL INSTANCE FAMILIES`.
- AUTO_RESUME defaults to TRUE; AUTO_SUSPEND_SECS defaults to 3600 (0 disables auto-suspend). A pool is inactive when no service or job is active on any node.
- `INITIALLY_SUSPENDED = TRUE` provisions no nodes at creation; start it with `ALTER COMPUTE POOL ... RESUME`.
- `BACKUP_INSTANCE_FAMILIES = (...)` lists fallbacks tried in order on insufficient-capacity errors; Snowflake does not check workload compatibility (architecture, GPU class, memory).
- A pool made `FOR APPLICATION` becomes unusable if that app is dropped.
- Needs the account-level CREATE COMPUTE POOL privilege.

## Service spec (YAML)
Fields documented in the reference include `containers[].name`, `image`, `env`, `resources.requests/limits`, `endpoints[].name/port/public`, volumes, and readiness/liveness probes.
```yaml
spec:
  containers:
    - name: main
      image: /app_db/svc/images/scorer:1.0
      env: {MODEL_PATH: /models}
      resources:
        requests: {cpu: 1, memory: 2Gi}
        limits: {memory: 4Gi}
  endpoints:
    - name: api
      port: 8080
      public: true
```
- Memory needs a unit (M, Mi, G, Gi); `2G` is 2,000,000,000 bytes, `2Gi` is 2x1024^3. CPU is in vCPU units, fractions allowed (0.5 or 500m).
- Requests should be the average expected usage; Snowflake uses them for placement. If omitted, the memory request is 0.5 GiB or the memory limit, whichever is greater; limits default to node capacity.
- A container with no GPU request and limit cannot access any GPU.
- A `public: true` endpoint allows network ingress; all containers of one service instance run on one node.

## Using services
- Service function: a function over a service endpoint, so queries send batches of rows to your container (CREATE FUNCTION for Snowpark Container Services).
- Job service: `EXECUTE JOB SERVICE IN COMPUTE POOL ... FROM SPECIFICATION ...`.
- Logs: `SYSTEM$GET_SERVICE_LOGS`, plus table functions `SPCS_GET_LOGS`, `SPCS_GET_EVENTS`, `SPCS_GET_METRICS`; logs, metrics and events also flow to event tables.
- Network: ingress is governed by network policies; internet egress needs an external access integration.

## Gotchas
- Spec fields such as command, args and env can change container behaviour without rebuilding the image.
- A pool with nodes running keeps consuming credits until it suspends; set AUTO_SUSPEND_SECS deliberately.

## Verify
Service reaches a ready state, the endpoint responds, and any service function returns results in SQL.

## Checked
Method: docs-only read on 2026-11-09 of the three cited Snowflake pages (all read in full as text). Removed unstated details: the docker login registry host, GPU family names, SHOW ENDPOINTS and SYSTEM$GET_SERVICE_STATUS usage, MIN/MAX_INSTANCES, and the claim that images must always be linux/amd64 (the reference says amd64 for x86 families, arm64 for ARM).
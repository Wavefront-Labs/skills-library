---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.replatform-to-containers
name: replatform-to-containers
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, replatform-to-containers, containerisation, app-containerisation, kubernetes-migration]
level: practitioner
status: draft
description: "Replatform an existing application to containers: suitability check, Dockerfile and config externalisation, state handling, target runtime choice and rollout."
sources: ["https://learn.microsoft.com/azure/architecture/guide/technology-choices/compute-decision-tree", "https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-containerize-java/welcome.html", "https://12factor.net/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replatforming to containers

## Steps
1. **Suitability**: runs on Linux (or Windows containers with supported base images),
   no hard dependency on host-specific hardware or kernel modules, startup time acceptable,
   licence permits containers. Stateful local file writes and in-memory sessions need work.
2. **Externalise config and secrets**: environment variables or mounted files; secrets from a
   secret manager via CSI driver or runtime integration, never baked into images.
3. **Write the image**: official minimal base, multi-stage build, non-root user, explicit
   versions, health endpoint, logs to stdout/stderr. Tools like AWS App2Container or Azure
   Migrate app containerisation can generate a first draft for Java/.NET apps.
4. **Handle state**: sessions to Redis or a database; uploads to object storage; local
   caches made disposable; scheduled jobs to a scheduler (CronJob, EventBridge Scheduler).
5. **Choose runtime**: serverless containers (Cloud Run, Azure Container Apps, ECS Fargate)
   for most web apps; Kubernetes when you need its ecosystem or already run a platform.
6. **Rollout**: run in parallel behind the load balancer, shift traffic gradually, keep the VM
   deployment for rollback until stable.

## Gotchas
- JVMs before container-aware versions ignore cgroup memory limits; set heap explicitly or use modern JDKs.
- Containerising a monolith keeps its scaling and coupling problems; it is a platform change, not a re-architecture.

## Verify
- [ ] Image scanned, non-root, and rebuilt in CI on base-image updates.
- [ ] App survives pod/task restarts with no lost sessions or data.

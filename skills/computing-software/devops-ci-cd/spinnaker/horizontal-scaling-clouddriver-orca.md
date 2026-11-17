---
id: computing-software.devops-ci-cd.spinnaker.horizontal-scaling-clouddriver-orca
name: horizontal-scaling-clouddriver-orca
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [scaling, clouddriver, orca, horizontal-scaling, queue-ready-depth, queue-message-lag, caching-agents]
level: advanced
status: docs-checked
description: "Know when adding replicas helps: Clouddriver caching shards and slow infra calls, Orca queue.ready.depth and queue.message.lag, and why resource requests matter on Kubernetes."
sources:
  - https://spinnaker.io/docs/setup/productionize/scaling/horizontal-scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page assumes you can scale individual microservices and explains when extra replicas help. On Kubernetes you are more likely to benefit if you have already allocated resource requests and limits for the services being scaled.

**Clouddriver.** It caches and retrieves infrastructure and submits operations. If calls to load infrastructure (such as load balancers), update caches (force cache refresh) or search (`/search`) slow down, add replicas. Technically every copy tries on a fixed interval to acquire locks to cache as many shards of your infrastructure as possible; shard boundaries depend on the provider and are visible in logs, e.g. a GCE agent log line such as `GoogleInfrastructureProvider:my-google-account/europe-west1/GoogleRegionalAddressCachingAgent completed in 0.111s` shows an agent responsible for one account, region and resource type. More nodes also spread reads forwarded from Gate.

**Orca.** Orca runs pipelines through a message queue in Redis shared by all Orca nodes. Slow application creation, pipeline runs or ad-hoc operations (clone, resize, rollback) usually mean Orca cannot drain that queue.
- `queue.ready.depth`: messages ready to process but not yet handled; high values suggest overworked Orca nodes. Adding nodes is a quick remediation.
- `queue.message.lag`: time messages wait while ready; operators should track it, ideally averaging below a few hundred milliseconds.

The page covers only Clouddriver and Orca, and does not explain the mechanics of scaling a service.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Horizontally Scale Spinnaker Services page. Confirmed both services' symptoms, the Clouddriver locking explanation, the log example and the two Orca metrics with their target. Removed the component sizing cross-reference and the claim of further services on the page.

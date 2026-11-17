---
id: computing-software.database-administration.memcached.proxy-deployment-topologies
name: proxy-deployment-topologies
category: computing-software
field: database-administration
product: memcached
tags: [proxy-deployment, sidecar, middleware, l1-l2-cache, topology]
level: advanced
status: docs-checked
description: "Compare proxy deployments: middleware machines, application sidecars and layered caches, with their latency and bandwidth trade-offs."
sources:
  - https://docs.memcached.org/features/proxy/infrastructure/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Middleware (central proxy pool): centralises pool config and maintenance, thin clients, optional hot-key cache in the proxy. Cons: extra hops and latency; with a few proxies in front of many cache servers, bandwidth is limited by the proxies. Memcached's normal distributed direct-to-client design scales bandwidth linearly with servers.

Sidecar (a proxy per application host, by binary or container): scales like plain memcached, lets the proxy be updated without touching the app, simplified clients. Cons: deploy on every host, some CPU, extra syscalls; verify local connection overhead in container systems.

Cache layering: applications talk to a local pool, which falls through to remote pools on miss (L1/L2).

Mixing is fine: use sidecars for high-bandwidth apps and a central pool for light users.

Decide by measuring added latency per request. See the examples page for configs: basic consistent hashing, replication, prefix routers.

## Checked

Confirmed 2026-11-09: middleware, sidecar and cache layering architectures with the pros and cons listed, bandwidth limited by the proxies when few proxies front many cache servers, linear bandwidth scaling of direct-to-client memcached, mixing approaches, container overhead needing verification, and the example configurations (basic consistent hashing, replication, prefix router) on the Configuration Examples page. Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Infrastructure examples and Configuration Examples pages

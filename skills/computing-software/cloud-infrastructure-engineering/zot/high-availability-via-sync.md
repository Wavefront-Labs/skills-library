---
id: computing-software.cloud-infrastructure-engineering.zot.high-availability-via-sync
name: high-availability-via-sync
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, high-availability, active-standby, active-active, haproxy, failover]
level: advanced
status: docs-checked
description: "Build an HA Zot registry from independent instances using sync: active/standby and active/active layouts, load balancer choices and the data-loss window."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/high-availability.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zot HA uses the `sync` feature rather than shared storage. Each instance is a standalone registry with its own storage, which adds a layer of safety versus shared-storage clustering.

Active/standby:
- Enable `sync` on the standby so it mirrors the active instance.
- Put a load balancer such as HAProxy in active/passive mode in front; requests go to the active instance and fall to the standby on failure.
- The standby synchronises periodically.

Active/active:
- Configure `sync` on each instance to point at the other.
- Spread requests with a load balancer such as HAProxy, or DNS-based routing (the article links CoreDNS's loadbalance plugin).
- Path-based routing is required, per the article.

Failure window: an image pushed after the last sync is absent from the other instance if the first one fails. Keep the synchronisation period as small as practical.

The article gives no config snippets; use the mirroring guidance for the `sync` settings.

Do not confuse with scale-out clustering, where an instance or storage going offline does affect availability.

## Checked

2026-11-04. Read against the zot high availability article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.

---
id: computing-software.networking-hardware-and-wireless.envoy.initialization-sequence
name: initialization-sequence
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, initialization, init-manager, warming, cluster-manager, init-dump, initial-fetch-timeout]
level: practitioner
status: docs-checked
description: "The Envoy startup order: static and DNS clusters, EDS, CDS, one health-check round, RDS and LDS, and why listeners open last."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/operations/init.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# initialization sequence
Everything below happens before any listener accepts a connection:
1. The cluster manager initialises static and DNS clusters, then predefined EDS clusters.
2. CDS is initialised, waiting for one response or failure for a bounded time (`initial_fetch_timeout`), then its clusters get the same primary then secondary initialisation.
3. If clusters use active health checking, Envoy runs one health check round first.
4. RDS and LDS initialise; the server waits a bounded time for at least one response or failure before accepting connections.
5. If LDS returns a listener that needs RDS, Envoy waits again (bounded), and this recurs for every later listener added via LDS. This is listener warming.
6. Listeners then start accepting.

Because the flow completes before accepting, a hot-restarted new process is fully capable before the old process starts draining.

```yaml
dynamic_resources:
  cds_config:
    initial_fetch_timeout: 5s
```
Gotchas: Envoy is guaranteed to initialize within `initial_fetch_timeout`, with a best effort to obtain the full xDS configuration within it, depending on management server availability. Admin `GET /init_dump` dumps unready targets, and `GET /ready` returns 200 for the LIVE state and 503 otherwise.

## Checked
2026-11-03. Confirmed against init.rst and the admin /init_dump and /ready entries. Removed or corrected: the 'timeout 0 waits forever' claim, the missing-RDS claim and the server.state gauge.
Method: documentation only; no commands were run.

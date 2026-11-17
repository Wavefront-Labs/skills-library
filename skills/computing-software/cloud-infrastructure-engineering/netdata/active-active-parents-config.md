---
id: computing-software.cloud-infrastructure-engineering.netdata.active-active-parents-config
name: active-active-parents-config
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, active-active, destination-list, stream-conf]
level: advanced
status: docs-checked
description: "Wire two Netdata Parents to stream to each other and give Children a space-separated destination list for failover, with the one-Parent-at-a-time rule."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/deployment-guides/deployment-strategies.md
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements from the docs:
- Each Parent streams to the other: each needs an outgoing `[stream]` destination and an incoming `[API_KEY]` section in `stream.conf`.
- Children list both Parents in `destination`, separated by spaces.

Parent A `stream.conf` (Parent B mirrors it):

```
[stream]
    enabled = yes
    destination = PARENT_B:19999
    api key = <key>

[<key>]
    enabled = yes
```

Child `stream.conf`:

```
[stream]
    enabled = yes
    destination = PARENT_A:19999 PARENT_B:19999
    api key = <key>
```

Generate keys with `uuidgen`. Restart every node after editing.

Rules and gotchas:
- A Child connects to one Parent at a time and falls back to the next only on failure.
- Cluster Parents sit at the top level of a hierarchy; every Parent receives all Children's metrics.
- The Netdata FAQ recommends against a TCP load balancer in front of the Parents.

## Checked

2026-11-04. Confirmed against the Netdata Deployment Strategies and Metrics Centralization Points pages: the Active-Active Parents requirements, the Parent 1, Parent 2 and Children stream.conf shapes, space-separated destinations, one-Parent-at-a-time with fallback, the top-level cluster rule, and the load balancer advice from the FAQ. Removed the unstated retention-consistency rule, the HTTP proxy claim and the closing Verify step.

Method: documentation only; no commands were run.

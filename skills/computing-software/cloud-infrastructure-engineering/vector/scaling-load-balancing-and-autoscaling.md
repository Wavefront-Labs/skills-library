---
id: computing-software.cloud-infrastructure-engineering.vector.scaling-load-balancing-and-autoscaling
name: scaling-load-balancing-and-autoscaling
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [scaling, load-balancer, autoscaling, hot-spots, stateful-transforms, health-endpoint, vector]
level: advanced
status: docs-checked
description: "Scale aggregators horizontally behind a load balancer and autoscale on CPU."
sources:
  - https://vector.dev/docs/setup/going-to-prod/sizing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Vertical:** Vector's concurrency model uses all vCPUs with no configuration. Cap an instance at no more than 33% of total volume so a node failure is survivable.

**Horizontal:** front instances with a load balancer. Use the one you can run highly available; a managed one such as AWS ALB is the docs' default suggestion.

Load balancer settings:

- Use a protocol supporting even balancing and application-level acknowledgement, such as HTTP.
- Enable keep-alive on clients and servers.
- With stateful transforms such as `aggregate` or `dedupe`, route a client consistently to one server (HAProxy `source` algorithm). Otherwise distribute evenly (`roundrobin`).
- Health-check Vector's `/health` API endpoint to eject unresponsive servers.
- Register new targets automatically as aggregators scale.

Hot spots: connections differ in volume. Prefer HTTP over plain TCP, spread data over several connections, size instances for your largest connection, and avoid stateful aggregation so fairer algorithms are possible.

Autoscaling: base it on average CPU, because Vector is almost always CPU constrained and CPU gives few false positives. Docs defaults: average CPU over 5 minutes, 85% target, 5 minute stabilisation for scaling up and down.

Capacity example: 12 vCPUs at 10 MiB/s each is about 10.4 TiB/day.

## Checked

Method: docs-checked 2026-11-09 against the full Vector sizing and capacity planning page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced verification line.

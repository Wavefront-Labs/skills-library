---
id: computing-software.cloud-infrastructure-engineering.knative.target-burst-capacity
name: target-burst-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [target-burst-capacity, activator-capacity, burst-capacity, load-balancing]
level: advanced
status: docs-checked
description: "Control when the activator stays in the request path and how many requests each activator handles."
sources:
  - https://knative.dev/docs/serving/load-balancing/target-burst-capacity/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide when the activator buffers traffic and how much it can hold.

Target burst capacity (TBC) controls whether the activator stays in the request path to absorb bursts.
- Global key: `target-burst-capacity` in the `config-autoscaler` ConfigMap.
- Per-revision annotation: `autoscaling.knative.dev/target-burst-capacity`.
- Values: float. `0` means the activator is in the path only when the Revision is scaled to zero. `-1` means the activator is always in the path.
- Default: `200`.

Values other than `0` and `-1`: the activator may be in the path, depending on the Revision's scale and load.

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/target-burst-capacity: "200"
```

The activator receives and buffers requests for inactive Revisions or oversized bursts, can quickly spin up additional pods, and can throttle how fast requests reach pods. TBC is configured together with the Revision's concurrency limits and target utilization settings.

With `0`, the activator is added only on scale from zero and ingress load balancing applies. Load balancing through the ingress gateway needs additional configuration; see the Serving API documentation.

## Checked

2026-11-03. Confirmed on the Knative Serving load-balancing/target-burst-capacity page: the TBC key, annotation, values 0/-1, default 200 and ingress-gateway note. Removed: the activator-capacity key and the current_demand formula (not on the page).
Method: documentation only; no commands were run.

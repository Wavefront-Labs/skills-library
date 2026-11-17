---
id: computing-software.cloud-infrastructure-engineering.knative.concurrency-limits
name: concurrency-limits
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [concurrency, container-concurrency, soft-limit, hard-limit, target-utilization-percentage]
level: practitioner
status: docs-checked
description: "Set soft concurrency targets and the hard containerConcurrency limit."
sources:
  - https://knative.dev/docs/serving/autoscaling/concurrency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control simultaneous requests per replica.

Concurrency is the number of simultaneous requests each replica processes at a time.

Soft limit: a target, not a strict bound, and a burst can exceed it. Configure both `autoscaling.knative.dev/metric` and `autoscaling.knative.dev/target`. Global key `container-concurrency-target-default`, default `"100"`.

Hard limit: an enforced upper bound set per Revision with the `containerConcurrency` field on the Revision spec (not an annotation). When reached, surplus requests are buffered until capacity frees up. There is no autoscaling ConfigMap key for it, because it affects buffering and queuing; a default can be set with `container-concurrency` in `config-defaults`, default `0` meaning no limit.

```yaml
spec:
  template:
    spec:
      containerConcurrency: 50
```

If both limits are set, the smaller value is used, so the autoscaler never targets more than the hard limit allows.

Warning: use a hard limit only with a clear use case. A low value can hurt throughput and latency and cause extra cold starts.

Target utilization adjusts the soft target: with `containerConcurrency` 10 and utilization 70 (default), a new replica starts at an average of 7 concurrent requests, so capacity is added before the hard limit is hit.

## Checked

2026-11-03. Confirmed on the Knative Serving autoscaling/concurrency page: soft and hard limits, keys, defaults, smaller-value rule, warning and target utilization example. Removed: nothing.
Method: documentation only; no commands were run.

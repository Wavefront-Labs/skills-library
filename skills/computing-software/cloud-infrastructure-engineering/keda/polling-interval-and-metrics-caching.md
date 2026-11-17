---
id: computing-software.cloud-infrastructure-engineering.keda.polling-interval-and-metrics-caching
name: polling-interval-and-metrics-caching
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [pollinginterval, usecachedmetrics, hpa-sync-period, metrics-caching, scaler-load]
level: practitioner
status: docs-checked
description: "Tune how often KEDA queries scalers, why the HPA sync period also matters, and when useCachedMetrics reduces load on the event source."
sources:
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
  - https://keda.sh/docs/2.17/concepts/scaling-deployments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two clocks poll your event source. `spec.pollingInterval` (default 30 seconds) is how often KEDA checks each trigger on every ScaledObject, and it is the only clock that matters while replicas are at 0, deciding when 0 to 1 happens. Once the workload runs between 1 and N replicas, the Kubernetes HPA also asks for metrics every `--horizontal-pod-autoscaler-sync-period` of the kube-controller-manager (default 15 seconds). Setting that flag to 30 makes the HPA poll every 30 seconds in that range.

By default each HPA request is routed to the KEDA metrics server, which queries the scaler live, so the source can be queried at the HPA's rate rather than at `pollingInterval`. Setting `useCachedMetrics: true` on a trigger changes this: the metrics server tries the cache first, and the cache is updated periodically during the polling interval. This respects the polling interval and can significantly reduce load on the scaler service.

Restrictions: caching is a per-trigger field (default `false`) and is not supported for the `cpu`, `memory` or `cron` scalers.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledObject specification and Scaling Deployments pages: pollingInterval 30, HPA sync period 15, useCachedMetrics and unsupported scalers. Reworded cache refresh and load statements to match the page.

Method: documentation only; no commands were run.

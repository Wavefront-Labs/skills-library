---
id: computing-software.cloud-infrastructure-engineering.crossplane.circuit-breaker
name: circuit-breaker
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [circuit-breaker, thrashing, responsive, helm-args, metrics]
level: advanced
status: docs-checked
description: "Detect and tune the per-XR reconciliation circuit breaker and find the cause of thrashing."
sources:
  - https://docs.crossplane.io/latest/guides/troubleshoot-crossplane/
  - https://docs.crossplane.io/latest/guides/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each XR has a token-bucket circuit breaker against reconciliation thrashing from excessive watch events. Defaults: burst 100, refill 1 event per second, cooldown 5 minutes. When exceeded it opens and blocks most reconciles, allowing periodic probe events.

Detect it in the XR condition:

```yaml
conditions:
- type: Responsive
  status: "False"
  reason: WatchCircuitOpen
  message: "Too many watch events from ConfigMap/my-config (default). Allowing events periodically."
```

The message names the noisy resource. Watch it with:

```shell
kubectl get <resource-kind> <resource-name> -n <namespace> --output-watch-events --watch-only
```

Common causes: patch feedback loops, other controllers fighting Crossplane over the same resource, and frequent connection detail updates. Fix the cause before changing thresholds.

Tune with Helm:

```shell
helm install crossplane --namespace crossplane-system --create-namespace crossplane-stable/crossplane \
  --set args='{"--circuit-breaker-burst=500.0","--circuit-breaker-refill-rate=5.0","--circuit-breaker-cooldown=1m"}'
```

Metrics: `circuit_breaker_opens_total`, `circuit_breaker_closes_total`, and `circuit_breaker_events_total` with `result` of `Allowed`, `Dropped` or `HalfOpenAllowed`, all labelled `controller` as `composite/<plural>.<group>`. Alert when the dropped share exceeds 20 percent for 5 minutes.

## Checked

Defaults, probe behaviour, condition, causes, Helm arguments and flag names confirmed on the Troubleshoot Crossplane page. Metric names, result values, controller label and the 20 percent alert threshold confirmed on the Metrics page. The documented probe rate is one request every 30 seconds while open.

Method: docs-checked 2026-11-09 against the raw Troubleshoot Crossplane page (read in full) and the Metrics page (circuit breaker section), docs repo, current content folder.

---
id: computing-software.cloud-infrastructure-engineering.istio.istio-outlier-detection
name: istio-outlier-detection
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, outlier-detection, ejection, passive-health]
level: practitioner
status: docs-checked
description: "Configure passive health checking in a DestinationRule to eject endpoints that return consecutive 5xx, and tune ejection percentage safely."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/circuit-breaking/", "https://istio.io/latest/docs/reference/config/networking/destination-rule/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Outlier detection ejects individual pods that return errors, so a single bad replica stops receiving traffic.

```yaml
trafficPolicy:
  outlierDetection:
    consecutive5xxErrors: 5
    interval: 10s
    baseEjectionTime: 30s
    maxEjectionPercent: 50
```

Defaults from the DestinationRule reference: `baseEjectionTime` 30s and `maxEjectionPercent` 10%. A host stays ejected for `baseEjectionTime` multiplied by the number of times it has been ejected, so repeat offenders stay out longer.

Gotchas: `maxEjectionPercent: 100` (used in the circuit-breaking task) lets every endpoint be ejected, so cap it in production. `consecutive5xxErrors: 1` is the task's demonstration value. Istio's default mesh configuration enables locality load balancing, so configuring outlierDetection also activates locality-aware failover; set `localityLbSetting.enabled: false` in the DestinationRule's load balancer settings to suppress that.

## Checked

2026-11-03. Confirmed against the DestinationRule reference (OutlierDetection field descriptions and defaults, the locality failover note, the example with `consecutive5xxErrors: 5` and `baseEjectionTime: 30s`) and the Circuit Breaking task. Removed: the unsourced `ejections_active` stats check, readiness-probe and alerting advice.
Method: documentation only; no commands were run.

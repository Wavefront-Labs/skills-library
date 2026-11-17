---
id: computing-software.cloud-infrastructure-engineering.istio.istio-locality-load-balancing
name: istio-locality-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, locality-load-balancing, locality-failover, load-balancer]
level: practitioner
status: docs-checked
description: "Prefer same-zone endpoints and fail over by region with localityLbSetting and outlier detection, which is required for failover to activate."
sources: ["https://istio.io/latest/docs/reference/config/networking/destination-rule/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Locality load balancing keeps traffic near the caller and fails over when local endpoints are unhealthy.

```yaml
trafficPolicy:
  loadBalancer:
    localityLbSetting:
      enabled: true
      failover:
      - {from: us-east, to: us-west}
  outlierDetection:
    consecutive5xxErrors: 5
    interval: 10s
    baseEjectionTime: 30s
```

Gotchas: `failover` should be used together with `outlierDetection` to detect unhealthy endpoints, otherwise it has no effect. Only one of `distribute`, `failover` or `failoverPriority` can be set. Istio's default mesh configuration enables locality load balancing (`localityLbSetting.enabled: true`), so configuring OutlierDetection in a DestinationRule activates locality-aware failover automatically; set `localityLbSetting.enabled: false` to suppress it. A DestinationRule-level `localityLbSetting` overrides the mesh-wide settings in entirety, with no merging. Zone and sub-zone failover is supported by default; `failover` only needs to be specified for regions when you want to constrain cross-region failover.

Verify: break or remove the local endpoints and watch requests move to the failover region.

## Checked

2026-11-03. Confirmed in the DestinationRule reference: `localityLbSetting`, `failover` with `from`/`to` regions, the requirement for OutlierDetection, `enabled` semantics, the mesh default of enabled, the one-of rule and override behaviour. Removed: the topology-label remark, `istioctl proxy-config endpoint` priorities, and the replica-balance and failure-drill advice (not on the page).

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.istio.istio-outbound-traffic-policy
name: istio-outbound-traffic-policy
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, outbound-traffic-policy, registry-only, egress-control]
level: practitioner
status: docs-checked
description: "Set meshConfig.outboundTrafficPolicy to REGISTRY_ONLY so unregistered external hosts are blocked, and understand why it is not secure egress control."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/egress/egress-control/", "https://istio.io/latest/docs/reference/config/networking/sidecar/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`meshConfig.outboundTrafficPolicy.mode` has two values: `ALLOW_ANY` (the default; outbound traffic to unknown destinations is allowed) and `REGISTRY_ONLY` (only hosts in the service registry, such as those with a ServiceEntry, are reachable).

```sh
istioctl install <flags-you-used-to-install-Istio> \
  --set meshConfig.outboundTrafficPolicy.mode=REGISTRY_ONLY
```

The task also shows the same setting as `meshConfig.outboundTrafficPolicy.mode: REGISTRY_ONLY` in an IstioOperator spec. Rerun your original install command with `ALLOW_ANY` to switch back. The task suggests starting in `ALLOW_ANY`, adding ServiceEntries for the services you use, then switching to `REGISTRY_ONLY` to block unintentional access.

Gotchas: the setting takes a while to propagate, so early requests may still succeed. It is enforced by the sidecar only: the Istio task states its examples do not enable secure egress control, because a malicious application can bypass the sidecar and reach any external service; for secure control it directs egress traffic through an egress gateway. Excluding IP ranges from the proxy (the task's `includeIPRanges` bypass) also skips Istio monitoring and policy for that traffic. The Sidecar resource also has an `outboundTrafficPolicy` field (default mode `ALLOW_ANY`) for per-workload behaviour.

## Checked

2026-11-03. Confirmed against the Istio Accessing External Services task (modes, install flag, propagation delay, secure egress caveat, bypass) and the Sidecar reference (`outboundTrafficPolicy`, default `ALLOW_ANY`). Removed: the `excludeOutboundIPRanges` annotation, `BlackHoleCluster`, 502 and `istioctl proxy-config` claims, the `sleep` curl example, and rollout advice, none of which the pages cover.
Method: documentation only; no commands were run.

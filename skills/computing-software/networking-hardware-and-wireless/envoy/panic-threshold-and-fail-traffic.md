---
id: computing-software.networking-hardware-and-wireless.envoy.panic-threshold-and-fail-traffic
name: panic-threshold-and-fail-traffic
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, panic-threshold, healthy-panic-threshold, fail-traffic-on-panic, load-balancing, cascading-failure]
level: practitioner
status: docs-checked
description: "Understand Envoy's 50 percent panic threshold, when it disables health filtering, and the fail-traffic-on-panic option."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/load_balancing/panic_threshold.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# panic threshold and fail traffic
Envoy normally balances only among available (healthy or degraded) hosts. If the percentage of available hosts falls below the panic threshold (default 50 percent), Envoy ignores health status and balances among all hosts, or among none. The goal is to stop host failures cascading through the cluster as load rises.

Configure in the cluster's common LB config:

```yaml
common_lb_config:
  healthy_panic_threshold: { value: 50.0 }
  zone_aware_lb_config:
    fail_traffic_on_panic: true
```
(The panic threshold is also settable via runtime as `upstream.healthy_panic_threshold`. `fail_traffic_on_panic` is a field of `ZoneAwareLbConfig`.)

Trade-off: failing traffic during panic reduces load on a sick upstream and cuts requests off faster, which suits all-or-nothing services. It removes any chance of partial success, so skip it for services that keep serving some requests when degraded.

Priorities interact: if the available fraction in one priority falls, Envoy first shifts traffic to lower priorities. Only if normalised availability across all priorities is below the threshold does panic apply, and Envoy disregards panic when it finds enough healthy hosts in lower priorities.

Gotcha: in panic mode Envoy sends traffic to all hosts, or to no hosts when `fail_traffic_on_panic` is true, which then always fail. Verify with the cluster `lb_healthy_panic` stat.

## Checked

2026-11-03. Confirmed against: panic_threshold.rst, cluster_runtime.rst, cluster_stats.rst and cluster.proto (50 percent default, healthy_panic_threshold, ZoneAwareLbConfig.fail_traffic_on_panic, lb_healthy_panic). Removed or corrected: the claim that a zero threshold disables panic mode and the version hedges.

Method: documentation only; no commands were run.

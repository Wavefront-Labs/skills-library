---
id: computing-software.networking-hardware-and-wireless.envoy.slow-start-mode
name: slow-start-mode
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, slow-start, slow-start-config, slow-start-window, aggression, min-weight-percent, warm-up]
level: practitioner
status: docs-checked
description: "Ramp traffic to new Envoy endpoints with slow start, including the window, aggression and minimum weight parameters."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/load_balancing/slow_start.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slow start mode
Slow start progressively increases traffic to newly added endpoints so services that need warm-up do not time out under full load. It is a per-cluster setting that scales an endpoint's load balancing weight with time. Supported in round robin, least request and client-side weighted round robin through `SlowStartConfig`.

```yaml
lb_policy: ROUND_ROBIN
round_robin_lb_config:
  slow_start_config:
    slow_start_window: 60s
    aggression: { default_value: 1.0 }
    min_weight_percent: { value: 10 }
```
Formula from the docs: `NewWeight = Weight * max(MinWeightPercent, TimeFactor^(1/Aggression))`, where `TimeFactor = max(TimeSinceStartInSeconds, 1) / SlowStartWindowInSeconds`. `min_weight_percent` (default 10 percent) keeps the EDF scheduler's deadline sensible. Aggression non-linearly sets the speed of ramp-up (polynomial or exponential shapes). After the window an endpoint takes its normal share.

Gotcha: it works best when few endpoints are new (a scale-out event). When all endpoints are new (a fresh deployment) it has little effect because all are scaled equally. Verify by scaling up and watching per-host `rq_total` in `GET /clusters` grow over the window.

## Checked

2026-11-03. Confirmed against: slow_start.rst (formula, window, aggression, 10 percent default min weight, most effective with few new endpoints) and cluster.proto (slow_start_config). Removed or corrected: the invented runtime key and the claim about which aggression values ramp faster.

Method: documentation only; no commands were run.

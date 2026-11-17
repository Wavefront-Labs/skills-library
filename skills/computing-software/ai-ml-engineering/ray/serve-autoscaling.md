---
id: computing-software.ai-ml-engineering.ray.serve-autoscaling
name: serve-autoscaling
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, autoscaling-config, target-ongoing-requests, min-replicas, serve-autoscale]
level: practitioner
status: docs-checked
description: "Autoscale Ray Serve replicas with autoscaling_config (min/max replicas, target_ongoing_requests, delays and look-back window)."
sources:
  - https://docs.ray.io/en/latest/serve/autoscaling-guide.html
  - https://docs.ray.io/en/latest/serve/advanced-guides/advanced-autoscaling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serve autoscaling

```python
@serve.deployment(
    autoscaling_config={
        "min_replicas": 1, "max_replicas": 20, "initial_replicas": 2,
        "target_ongoing_requests": 5,   # average ongoing requests per replica Serve aims for
        "upscale_delay_s": 10, "downscale_delay_s": 300,
        "metrics_interval_s": 10, "look_back_period_s": 30,
    },
    max_ongoing_requests=7)
class Model: ...
```
`num_replicas="auto"` applies a default autoscaling config. Setting `min_replicas` to 0 suits long idle periods when extra tail latency during upscale is acceptable.

## Parameters (from the guides)
- `target_ongoing_requests`: shorter latency goal or longer requests means a smaller value.
- `max_ongoing_requests`: default 5 (changed from 100 in Ray 2.32.0). Set it about 20 to 50% higher than `target_ongoing_requests`; too low and requests queue at the proxy and throttle throughput.
- `max_replicas`: set about 20% above what peak traffic needs. With `num_replicas="auto"` the default is 100; configuring autoscaling manually without it defaults `max_replicas` to 1, so nothing scales until you raise it.
- `initial_replicas` defaults to `min_replicas`; `upscale_delay_s` defaults to 30; `downscale_delay_s` to 600; `metrics_interval_s` to 10; `look_back_period_s` to 30 (window for the average).
- `downscale_to_zero_delay_s` (optional) sets a separate wait for the 1 to 0 transition when `min_replicas` is 0.
- Do not set `metrics_interval_s` very low (the guide warns 0.1 can overload the controller on the head node).
- Slow initialisation: raise `downscale_delay_s` to avoid paying reinitialisation cost when load returns.

## Verify
Run a load test and watch the replica count in `serve status` rise and later fall.

## Checked
2026-11-03. Confirmed in the Ray repo docs `serve/autoscaling-guide.md` and `serve/advanced-guides/advanced-autoscaling.md`: parameter meanings, the defaults above, the 2.32.0 default change and the max_ongoing_requests guidance. Removed: old parameter name claim, cluster autoscaler interplay and `ray status` statement, `hey` command, p95 advice, a claim that `num_replicas` and `autoscaling_config` are mutually exclusive (not stated), GPU-replica latency claims.
Method: documentation only; no commands were run.

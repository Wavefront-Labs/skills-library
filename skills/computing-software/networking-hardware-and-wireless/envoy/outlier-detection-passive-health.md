---
id: computing-software.networking-hardware-and-wireless.envoy.outlier-detection-passive-health
name: outlier-detection-passive-health
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, outlier-detection, passive-health-check, consecutive-5xx, success-rate, ejection, split-external-local-origin-errors]
level: practitioner
status: docs-checked
description: "Use Envoy outlier detection to eject misbehaving hosts and understand how local versus external errors are counted per filter."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/outlier.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# outlier detection passive health
Outlier detection is passive health checking: hosts performing unlike their peers (consecutive failures, success rate, latency) are removed from the healthy load balancing set. It lives in cluster config and can run alongside active health checks. It depends on the filter reporting results; the HTTP router, TCP proxy, Redis proxy and Thrift proxy do.

```yaml
outlier_detection:
  consecutive_5xx: 5
  interval: 10s
  base_ejection_time: 30s
  max_ejection_percent: 10
```
How errors are bucketed:
- Externally originated errors are transaction-specific (an HTTP 500, a bad Redis payload). Locally originated errors are Envoy-side events such as timeouts and TCP resets.
- The HTTP router sees both; the TCP proxy understands nothing above TCP and reports only local errors.
- By default (`split_external_local_origin_errors: false`) everything lands in one bucket compared against `consecutive_5xx`, `consecutive_gateway_failure` and `success_rate_stdev_factor`. Two timeouts then a 500 count as 3 errors.
- For TCP traffic, `consecutive_5xx` is the right knob and maps to connection failures.

Gotcha: setting the split flag to true moves local errors to separate counters and thresholds, and consecutive gateway failure then counts only 502, 503 and 504 from the HTTP router. Errors from the TCP and Redis proxies are mapped internally to HTTP 5xx. Admin `GET /clusters` shows the cluster's success rate average and ejection threshold when a detector is installed.

## Checked
2026-11-03. Confirmed against outlier.rst and the OutlierDetection reference. Removed or corrected: the 'confirm field names' note and the outlier.* verify step.
Method: documentation only; no commands were run.

---
id: computing-software.networking-hardware-and-wireless.envoy.admission-control-filter
name: admission-control-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, admission-control, sr-threshold, aggression, sampling-window, load-shedding, success-criteria]
level: practitioner
status: docs-checked
description: "Shed load adaptively with the Envoy admission control filter based on a rolling success rate, with aggression and RPS threshold tuning."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/admission_control_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# admission control filter
The admission control filter probabilistically rejects requests when the recent success rate of a service drops, giving a struggling upstream room to recover. A configuration matching the documented example (60s window, 95 percent threshold, RPS floor of 1, rejection capped at 95 percent):

```yaml
http_filters:
- name: envoy.filters.http.admission_control
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.admission_control.v3.AdmissionControl
    enabled: { default_value: true, runtime_key: admission_control.enabled }
    sampling_window: 60s
    sr_threshold: { default_value: { value: 95.0 }, runtime_key: admission_control.sr_threshold }
    aggression: { default_value: 1.0, runtime_key: admission_control.aggression }
    rps_threshold: { default_value: 1, runtime_key: admission_control.rps_threshold }
    max_rejection_probability: { default_value: { value: 95.0 }, runtime_key: admission_control.max_rejection_probability }
    success_criteria:
      http_criteria:
        http_success_status: [ { start: 100, end: 400 }, { start: 404, end: 405 } ]
```
Key knobs: `sampling_window` (history used), `sr_threshold` (success rate percent above which nothing is rejected), `aggression` (how hard rejection grows as success falls), `rps_threshold` (minimum request rate before the filter acts) and `max_rejection_probability` (cap so some requests always pass).

Gotchas from the docs: success rate is computed per worker thread, so rejection probability can differ between workers; health check traffic is not counted; only non-route-specific virtual host configuration is supported. HTTP 1xx, 2xx, 3xx and 404 count as success in the example, gRPC OK and CANCELLED likewise. Stats are `http.<stat_prefix>.admission_control.rq_rejected`, `rq_success` and `rq_failure`.

## Checked
2026-11-03. Confirmed against admission_control_filter.rst and the admission_control.proto reference. Removed or corrected: the claim that the YAML is the docs example (the page includes it from a file), the low-traffic and runtime advice, and rewrote the gotchas from the page.
Method: documentation only; no commands were run.

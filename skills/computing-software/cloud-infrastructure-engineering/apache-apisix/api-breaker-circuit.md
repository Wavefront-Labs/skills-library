---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.api-breaker-circuit
name: api-breaker-circuit
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, api-breaker, circuit-breaker, unhealthy, break-response-code, plugin]
level: practitioner
status: docs-checked
description: "Add a circuit breaker to an APISIX route with api-breaker: unhealthy and healthy status lists, failure thresholds, break_response_code and exponential retry up to max_breaker_sec."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/api-breaker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# api-breaker circuit

Attributes:
- `break_response_code` (required): 200-599, returned while open.
- `break_response_body`, `break_response_headers` (headers need a body; values can use APISIX variables).
- `max_breaker_sec`: 300, minimum 3.
- `unhealthy.http_statuses` `[500]`, `unhealthy.failures` 3.
- `healthy.http_statuses` `[200]`, `healthy.successes` 3.

```json
{
  "api-breaker": {
    "break_response_code": 503,
    "break_response_body": "Service temporarily unavailable",
    "max_breaker_sec": 120,
    "unhealthy": { "http_statuses": [500, 502], "failures": 5 },
    "healthy": { "http_statuses": [200, 204], "successes": 2 }
  }
}
```

States:
- Closed: requests flow and failures are counted.
- Open: after `unhealthy.failures` matching responses, APISIX returns `break_response_code` without calling the upstream.
- Probing: retries after 2, 4, 8, 16 seconds and so on, capped at `max_breaker_sec`.
- Recovery: after `healthy.successes` consecutive healthy responses the upstream is healthy again.

## Checked

2026-11-04. Confirmed against the APISIX api-breaker plugin page: break_response_code range, body and headers rule, max_breaker_sec default and minimum, unhealthy and healthy defaults, the 2, 4, 8, 16 second retry schedule, recovery after healthy.successes. Nothing removed.

Method: documentation only; no commands were run.

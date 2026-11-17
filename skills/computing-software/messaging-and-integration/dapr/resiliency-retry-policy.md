---
id: computing-software.messaging-and-integration.dapr.resiliency-retry-policy
name: resiliency-retry-policy
category: computing-software
field: messaging-and-integration
product: dapr
tags: [resiliency, retries, exponential-backoff, constant, maxretries, maxinterval, pubsub]
level: practitioner
status: docs-checked
description: "Define Dapr retry policies: constant versus exponential, duration, maxInterval, maxRetries (-1 unlimited, 0 off), the backoff formula, and pub/sub built-in retries."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/policies/retries/retries-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Retries are named templates under `spec.policies.retries`, instantiated per operation:

```yaml
spec:
  policies:
    retries:
      pubsubRetry:
        policy: constant
        duration: 5s
        maxRetries: 10
      retryForever:
        policy: exponential
        maxInterval: 15s
        maxRetries: -1 # Retry indefinitely
```

Options and defaults:

- `policy`: `constant` (default) or `exponential`.
- `duration`: interval between retries, constant only, forms like `200ms`, `15s`, `2m`; default `5s`.
- `maxInterval`: ceiling the exponential backoff can grow to; later retries always wait `maxInterval`; default `60s`.
- `maxRetries`: `-1` unlimited (default), `0` means no retry, as if no policy was set.
- `matching.httpStatusCodes` / `matching.gRPCStatusCodes`: optional filters (see the status code filter skill).

Exponential back-off formula from the page:

```
BackOffDuration = PreviousBackOffDuration * (Random value from 0.5 to 1.5) * 1.5
if BackOffDuration > maxInterval {
  BackoffDuration = maxInterval
}
```

Retries pair with timeouts: timeouts fail fast, retries recover from transient glitches. They can also re-send to a different instance. Dapr also ships default policies that you can override.

Important for pub/sub: each pub/sub component has its own built-in retry behaviour. A Resiliency policy does not replace it, it augments it, so total attempts can exceed what the policy alone suggests. Retries only take effect once a policy is attached to a target (app, component or actor) in `spec.targets`.

## Checked

2026-11-04. Retry options, defaults, backoff formula and the pub/sub warning confirmed on the Retry resiliency policies page.

Method: documentation only; no commands were run.

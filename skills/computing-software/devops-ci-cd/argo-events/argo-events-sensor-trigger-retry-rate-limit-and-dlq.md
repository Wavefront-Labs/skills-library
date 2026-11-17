---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-trigger-retry-rate-limit-and-dlq
name: argo-events-sensor-trigger-retry-rate-limit-and-dlq
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, retrystrategy, ratelimit, dlqtrigger, atleastonce, revisionhistorylimit, trigger]
level: advanced
status: docs-checked
description: "Add retries, rate limits and a dead letter trigger to Sensor triggers, noting that triggers do not retry by default."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/more-about-sensors-and-triggers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor trigger retry rate limit and dlq

By default a trigger is not retried, because the Sensor cannot know whether a retry would have unexpected results. Add `retryStrategy`:

```yaml
triggers:
  - template:
      name: http-trigger
      http:
        url: https://xxxxx.com/
        method: GET
    retryStrategy:
      steps: 3          # give up after this many attempts
      duration: 2s      # initial wait
      factor: 2.0       # multiplier per retry (default 1.0)
      jitter: 2         # random extra up to jitter * duration (default 1)
```

Rate limit: none unless configured.

```yaml
triggers:
  - rateLimit:
      unit: Second      # Second, Minute or Hour; default Second
      requestsPerUnit: 20
```

Dead letter queue: once retries are exhausted, an optional `dlqTrigger` (any trigger type) can run so the message is not lost. Both the main trigger and the dlqTrigger need `atLeastOnce: true`, and the dlqTrigger can have its own `retryStrategy` (for example 5 steps). It works only at the top level: a dlqTrigger cannot itself contain a dlqTrigger.

Sensor spec also accepts an optional `revisionHistoryLimit`, for example `3`.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/more-about-sensors-and-triggers.md. Confirmed: no default retry, retryStrategy steps/duration/factor/jitter and their defaults, rateLimit unit and requestsPerUnit, revisionHistoryLimit, dlqTrigger with atLeastOnce and top-level-only note. Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.

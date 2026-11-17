---
id: computing-software.messaging-and-integration.dapr.resiliency-timeout-policy
name: resiliency-timeout-policy
category: computing-software
field: messaging-and-integration
product: dapr
tags: [resiliency, timeouts, time-parseduration, general, important, largeresponse]
level: practitioner
status: docs-checked
description: "Define named Dapr timeout policies as Go durations (general, important, largeResponse), what happens when one fires, and the behaviour when no timeout is specified."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/policies/timeouts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Timeouts cut off unresponsive calls so resources are freed for new work. They are optional. When a timeout is exceeded, the operation in progress is terminated if possible and an error is returned. Choose values reflecting real production response times.

```yaml
spec:
  policies:
    # Timeouts are simple named durations.
    timeouts:
      timeoutName: timeout1
      general: 5s
      important: 60s
      largeResponse: 10s
```

Each value uses Go `time.ParseDuration` format with no set maximum, for example `15s`, `2m`, `1h30m`. `general`, `important` and `largeResponse` are the example's timeout names (for timeouts marked general, important, or awaiting a large response); `timeoutName` is the policy name field.

If you do not specify a timeout, the policy enforces nothing and behaviour falls back to whatever the request client is configured with.

Timeouts and retries work together: timeouts ensure the system fails fast, and retries recover from temporary glitches. Attach policies to apps, actors or components in the spec's `targets` section.

## Checked

2026-11-04. Timeout YAML, duration format and no-timeout behaviour confirmed on the Timeout resiliency policies page.

Method: documentation only; no commands were run.

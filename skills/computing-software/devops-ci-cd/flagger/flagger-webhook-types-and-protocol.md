---
id: computing-software.devops-ci-cd.flagger.flagger-webhook-types-and-protocol
name: flagger-webhook-types-and-protocol
category: computing-software
field: devops-ci-cd
product: flagger
tags: [webhooks, confirm-rollout, hooks, loadtester]
level: practitioner
status: docs-checked
description: "Choose among Flagger webhook types and understand the payload, status code rules, retries and timeout budget."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/webhooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flagger calls each webhook URL and treats HTTP 2xx as success. Types:
- `confirm-rollout`: before scaling up the canary; manual approval.
- `pre-rollout`: before routing traffic to the canary; failures count toward the threshold.
- `rollout`: every iteration before the metric checks.
- `confirm-traffic-increase`: right before the canary weight is increased; halts until HTTP 200.
- `confirm-promotion`: before promotion; metrics and rollout hooks keep running while paused.
- `post-rollout`: after promotion or rollback; failures are only logged.
- `rollback`: during Progressing or Waiting; a success stops the analysis and fails the canary.
- `event`: on every Kubernetes event Flagger emits, sent as a JSON POST.

```yaml
webhooks:
  - name: "load test"
    type: rollout
    url: http://flagger-loadtester.test/
    timeout: 15s
    retries: 3
    metadata:
      cmd: "hey -z 1m -q 5 -c 2 http://podinfo-canary.test:9898/"
```

The sum of all rollout webhook timeouts must be lower than the analysis interval. The POST body has `name`, `namespace`, `phase`, `checksum` (hash of tracked configs and last applied spec) and `metadata`. Status 200-202 advances; a timeout or non-2xx halts and increments failed checks, with the response body added to logs and events. `retries` helps with transient network failures, and `disableTLS: true` skips TLS verification for self-signed targets.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/webhooks.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.

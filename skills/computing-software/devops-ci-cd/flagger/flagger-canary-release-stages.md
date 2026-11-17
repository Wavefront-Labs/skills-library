---
id: computing-software.devops-ci-cd.flagger.flagger-canary-release-stages
name: flagger-canary-release-stages
category: computing-software
field: devops-ci-cd
product: flagger
tags: [canary-release, rollout, webhooks, promotion]
level: advanced
status: docs-checked
description: "Follow the gated promotion sequence of a Flagger canary release, from confirm-rollout hooks through metric checks to promotion and rollback."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flagger runs a control loop. The sequence per change:

1. Check primary and canary deployment status; halt if a rolling update is underway or pods are unhealthy.
2. Call `confirm-rollout` webhooks, then `pre-rollout` webhooks. A non-2xx result halts (pre-rollout also increments the failed checks counter).
3. Raise canary weight by `stepWeight`, call `rollout` webhooks and check metrics. Advancement halts while success rate is under threshold, P99 duration is over threshold, a custom metric fails, a webhook fails, pods become unhealthy, or the HPA is scaling the canary.
4. If failed checks reach `threshold`: route all traffic to primary, scale canary to zero, mark failed, call `post-rollout` webhooks, post to Slack, and wait for the next change.
5. After `maxWeight`, call `confirm-promotion` webhooks, copy ConfigMaps, Secrets and the deployment spec to the primary, wait for the primary rollout, route all traffic to primary, scale the canary to zero, call `post-rollout` hooks and notify.

Emergency shortcut: `spec.skipAnalysis: true` deploys straight to production without metric and webhook checks.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.

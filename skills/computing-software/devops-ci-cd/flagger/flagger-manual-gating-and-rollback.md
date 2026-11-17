---
id: computing-software.devops-ci-cd.flagger.flagger-manual-gating-and-rollback
name: flagger-manual-gating-and-rollback
category: computing-software
field: devops-ci-cd
product: flagger
tags: [manual-gating, approval, rollback, confirm-promotion]
level: practitioner
status: docs-checked
description: "Gate Flagger canary rollouts for manual approval with confirm hooks and the loadtester gate API, and trigger manual rollback."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/webhooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `confirm-rollout`, `confirm-traffic-increase` and `confirm-promotion` to halt until the hook returns HTTP 200; confirm-rollout runs before pre-rollout hooks. The tester's `/gate/halt` returns 403 (blocking), `/gate/approve` returns 200.

```yaml
webhooks:
  - name: "gate"
    type: confirm-rollout
    url: http://flagger-loadtester.test/gate/check
```

With `/gate/check` the gate is closed by default. Open or close it from inside the tester pod:

```bash
curl -d '{"name": "podinfo","namespace":"test"}' http://localhost:8080/gate/open
curl -d '{"name": "podinfo","namespace":"test"}' http://localhost:8080/gate/close
```

A paused canary shows status `Waiting`. Notifications on waiting-for-approval can be silenced with `muteAlert: true` on the webhook.

Manual rollback uses a `rollback` webhook pointing at `/rollback/check`; it is closed by default, and `/rollback/open` makes Flagger shift all traffic to primary and fail the canary (`/rollback/close` resets). Notifications are posted to Slack or MS Teams when a canary is rolled back.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/webhooks.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.

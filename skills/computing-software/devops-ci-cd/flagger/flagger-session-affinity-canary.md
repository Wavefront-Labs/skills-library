---
id: computing-software.devops-ci-cd.flagger.flagger-session-affinity-canary
name: flagger-session-affinity-canary
category: computing-software
field: devops-ci-cd
product: flagger
tags: [session-affinity, cookies, stickiness, gateway-api]
level: advanced
status: docs-checked
description: "Keep users on the new version during a Flagger weighted canary with sessionAffinity cookies, including primary stickiness; supported on Istio and Gateway API."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Weight-based routing can send a user back to the old version after they saw the new one. `analysis.sessionAffinity` adds cookie routing so once exposed to the canary, a user always stays on it.

```yaml
analysis:
  interval: 1m
  threshold: 10
  maxWeight: 50
  stepWeight: 2
  sessionAffinity:
    cookieName: flagger-cookie
    maxAge: 21600
```

Canary-routed responses set `Set-Cookie: flagger-cookie=<random id>; Max-Age=21600`. After the run, responses set `Max-Age=-1` so clients delete the cookie; a new run issues a new cookie.

Over time this skews traffic toward the canary. For fair distribution, add `primaryCookieName: primary-flagger-cookie`; responses from the primary then also set a cookie whose age equals the analysis interval. Currently supported only for the Gateway API and Istio providers.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.

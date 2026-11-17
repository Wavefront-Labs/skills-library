---
id: computing-software.devops-ci-cd.spinnaker.gate-api-rate-limiting
name: gate-api-rate-limiting
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [rate-limiting, gate, redis, api, learning-mode, throttling, headers]
level: advanced
status: docs-checked
description: "Enable Gate's API rate limiter: learning versus enforcing mode, capacity and window per principal, the four X-RateLimit headers, anonymous buckets and the metrics to watch."
sources:
  - https://spinnaker.io/docs/guides/runbooks/api-rate-limiting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The rate limiter protects Spinnaker from traffic spikes and rogue API clients. It limits individual authenticated and anonymous principals in windows refreshed each interval, with capacity and window size configurable globally and per principal, and a global and per-principal **learning mode**. It requires Redis for Gate. On failure (Redis unavailable) or a config error (a principal in both the enforcing and ignoring lists), a request falls back to learning mode.

**gate.yml:**

```yaml
rateLimit:
  enabled: true
  learning: true
  redis:
    enabled: true
  rateSeconds: 10
  capacity: 500
  capacityByPrincipal:
  - principal: anonymous
    override: 1000
  rateSecondsByPrincipal:
  - principal: anonymous
    override: 5
  enforcing:
  - example@example.com
  ignoring:
  - unmetered-example@example.com
```

`enforcing` helps roll out incrementally; `ignoring` puts principals in learning mode permanently (the page says to reconsider that).

**Client headers:** `X-RateLimit-Capacity`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `X-RateLimit-Learning`.

**Anonymous clients** share one bucket by default; a client can send `X-RateLimit-App` with its application name to get its own.

**Metrics:** `rateLimit.throttling`, `rateLimit.throttlingLearning`, `rateLimit.principal.throttled` and `rateLimit.principal.remaining` (tagged by `principal`), read together with `controller.invocations`.

**Dynamic configuration.** Redis can override the static configuration, so Gate need not be redeployed. Key patterns: `rateLimit:learning` (global learning flag), `rateLimit:enforcing` (set of enforced principals), `rateLimit:ignoring` (principals in learning mode), `rateLimit:capacity:*` and `rateLimit:rateSeconds:*` (per principal). Examples from the page: `set rateLimit:capacity:chaosmonkey@example.com 2000` and `sadd rateLimit:enforcing chaosmonkey@example.com`.

## Checked

2026-11-04. Behaviour, the YAML block, headers, anonymous bucket header and metrics were confirmed on the API Rate Limiting page. The dynamic configuration key patterns and examples were confirmed on the same page.

Method: documentation only; no commands were run.

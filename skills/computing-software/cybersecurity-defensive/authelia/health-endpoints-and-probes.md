---
id: computing-software.cybersecurity-defensive.authelia.health-endpoints-and-probes
name: health-endpoints-and-probes
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, health-check, readiness-probe, liveness-probe, kubernetes, monitoring]
level: practitioner
status: docs-checked
description: "Use Authelia's plain and verbose health endpoints for liveness and readiness probes, with provider selection, caching and the detailed-output risk."
sources:
  - https://www.authelia.com/configuration/miscellaneous/server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia exposes health endpoints under `server.endpoints.health`.

```yaml
server:
  endpoints:
    health:
      verbose: true
      detailed: false
      providers:
        - 'storage'
        - 'session'
        - 'user'
      cache: '10 seconds'
```

How each endpoint behaves:

- `/api/health` is unaffected by any option here. It answers `200` whenever the server accepts requests, so it suits a liveness probe and existing container health checks keep working.
- `verbose: true` enables `/api/health/verbose`. It probes each configured provider and answers `200` if all pass or `503` if any fails. That makes it a readiness probe, or a load balancer check that stops routing to an instance whose database or authentication backend has gone away.
- The JSON response names each provider with its probe time. The overall `status` is `ok` when every provider passes, `degraded` when some fail and `error` when all fail.
- `providers` selects what the verbose endpoint probes, in the order given. The default is `storage`, `session` and `user`; the other values are `notification`, `ntp`, `expressions` and `webauthn-metadata`. Probing `notification` opens a connection to the SMTP server and `ntp` contacts an external NTP server, so neither is a default.
- `cache` (default 10 seconds) is how long a result is reused before providers are probed again; `0` probes on every request.
- `detailed` (default false) adds the provider error message as an `error` member. Without it a failing provider shows only `"status": "error"` and the message goes to the log.

The docs warn that provider error messages can contain connection strings, host names and directory base DNs, and that the verbose endpoint does not require authentication, so enabling `detailed` publishes them to anyone who can reach it. Enable it while diagnosing and turn it off afterwards.

Check: stop the database and confirm `/api/health/verbose` returns `503` while `/api/health` still returns `200`.

## Checked

2026-11-08. Read the full Authelia Server page. Confirmed the /api/health and /api/health/verbose behaviour, status values, the provider list and default, cache default and the detailed security note. Corrected the provider list (seven possible values, not three) and the detailed advice.

Method: documentation only; no commands were run.

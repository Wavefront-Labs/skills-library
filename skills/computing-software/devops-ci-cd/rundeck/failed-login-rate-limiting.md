---
id: computing-software.devops-ci-cd.rundeck.failed-login-rate-limiting
name: failed-login-rate-limiting
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, login-rate-limiting, brute-force, auth-rate-limiting, refill-window]
level: practitioner
status: docs-checked
description: "Enable failed-login lockout in Enterprise Rundeck with rundeck.authRateLimiting settings to resist brute-force attempts."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/security/ratelimiting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Failed Login Rate Limiting (Enterprise) protects against brute force login attempts. It is off by default on new installs but recommended in production.

Set it in Configuration Management or `rundeck-config.properties`:

```properties
rundeck.authRateLimiting.enabled=true
rundeck.authRateLimiting.rate=5
rundeck.authRateLimiting.refillWindowInSeconds=60
```

- `enabled`: true or false, whether failed logins are checked for lockout.
- `rate`: failed attempts allowed within the refill window before the account is locked.
- `refillWindowInSeconds`: window length. The bucket refills only when the window reopens; if a user keeps submitting during the window, further requests are rejected until the next one opens.

Gotcha: there is no way to clear a lockout except waiting for the refill window to expire without further failed attempts.

Verify by submitting more bad logins than `rate` within the window and confirming the account is rejected.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Rate Limiting (Commercial), Failed Login section: off by default on new installs but recommended in production, rundeck.authRateLimiting.enabled/rate/refillWindowInSeconds example values and meanings, and the note that a lockout cannot be cleared except by waiting. Nothing removed.

Method: documentation only; no commands were run.

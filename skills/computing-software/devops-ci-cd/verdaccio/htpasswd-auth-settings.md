---
id: computing-software.devops-ci-cd.verdaccio.htpasswd-auth-settings
name: htpasswd-auth-settings
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [htpasswd, bcrypt, max-users, htpasswd-file, verify-cache-ms, slow-verify-ms, algorithm]
level: practitioner
status: docs-checked
description: "Configure the built-in htpasswd auth plugin: file, max_users, bcrypt rounds, slow_verify_ms and the 7.x verify_cache_ms cache for repeated password checks."
sources:
  - https://verdaccio.org/docs/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
auth:
  htpasswd:
    file: ./htpasswd
    max_users: 1000      # -1 disables self-registration
    algorithm: bcrypt
    rounds: 10
    slow_verify_ms: 200
    verify_cache_ms: 0   # 7.x
```
- `file` is required. `max_users` defaults to unlimited; `-1` disables registration.
- `algorithm` defaults to bcrypt with 10 rounds on 6.x and 7.x. `md5`, `sha1`, `crypt` exist only to read old files and are rehashed on password change; an unknown value falls back to bcrypt with a warning.
- `slow_verify_ms` only logs a warning when verification is slow (0 means default 200); it is not a timeout.
- `verify_cache_ms` (7.x, default 0 = off): caches successful verifications (max 1000 entries, keyed by HMAC) and shares identical in-flight checks. Failures are not cached. Keep it short: someone with process-memory access could test guesses faster than bcrypt allows.

Why: Basic auth sends the password on each request, so parallel downloads can repeat expensive bcrypt checks; higher `rounds` raises that cost.

## Checked

2026-11-04. Confirmed against the Verdaccio Authentication page (htpasswd properties, bcrypt default with 10 rounds on 6.x and 7.x, legacy algorithms, slow_verify_ms, verify_cache_ms cache details and risk). Removed: the claim that -1 also stops npm adduser and the closing Verify tip.
Method: documentation only; no commands were run.

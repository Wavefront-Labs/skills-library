---
id: computing-software.cybersecurity-defensive.authelia.session-timeouts-and-remember-me
name: session-timeouts-and-remember-me
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, session, inactivity, expiration, remember-me, passkey, session-secret]
level: practitioner
status: docs-checked
description: "Set Authelia session inactivity, expiration and remember_me timers, including defaults, the -1 disable value and the passkey login dependency."
sources:
  - https://www.authelia.com/configuration/session/introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three timers control how long a session lives, and each is set both at the top of `session` (as the default for every cookie entry) and inside a `cookies` entry.

```yaml
session:
  secret: '<SESSION_SECRET>'
  inactivity: '5m'
  expiration: '1h'
  remember_me: '1M'
```

- `inactivity` (default 5 minutes): how long a user may be inactive before the session is destroyed. Useful for long sessions that should still drop unused devices.
- `expiration` (default 1 hour): the absolute lifetime before the cookie expires and the session is destroyed.
- `remember_me` (default 1 month): the lifetime when the user ticks the remember-me box. It overrides `expiration` in that case. Setting it to `-1` disables the feature for that cookie domain.

Durations use the documented common duration syntax (the examples use `5m`, `1h`, `1d` and `1M`).

Two further points:

- Passkey login currently requires remembered sessions when it is enabled, because the WebAuthn dialog disrupts the UI flow. The docs say control of the remembered state in this scenario will change in future.
- `session.secret` encrypts session data held in Redis. The docs strongly recommend a random alphanumeric string of 64 or more characters, and defining it as a secret rather than inline, especially for containers.

Per-cookie values override these defaults, so a stricter `inactivity` can apply to one domain only.

Check: wait out `inactivity` on a test account and confirm the next request redirects to the portal.

## Checked

2026-11-08. Read the full Authelia Session configuration page (authelia.com/configuration/session/introduction). Confirmed the inactivity, expiration and remember_me defaults (5 minutes, 1 hour, 1 month), the -1 value, the passkey login note and the session secret guidance. Removed the unconfirmed claim about integer-second durations and the secrets-file or environment-variable wording.

Method: documentation only; no commands were run.

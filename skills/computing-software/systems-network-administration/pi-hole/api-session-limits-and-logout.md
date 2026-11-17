---
id: computing-software.systems-network-administration.pi-hole.api-session-limits-and-logout
name: api-session-limits-and-logout
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [api-sessions, session-timeout, rate-limiting-login]
level: advanced
status: docs-checked
description: "Avoid API lockouts by understanding session limits, timeouts, IP binding, rate limiting and proper logout."
sources: ["https://docs.pi-hole.net/api/auth/", "https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# API session limits

**Limits**

- `webserver.api.max_sessions` (default `16`) caps concurrent sessions. At the cap, new logins can be denied until sessions expire or log out. It is irrelevant when authentication is disabled.
- `webserver.session.timeout` (default `1800` seconds) ends inactive sessions. Raising it, for example to `86400`, keeps logins long but consumes session slots.
- `webserver.session.restore` (default `true`) restores sessions from the database after a restart.
- Login attempts are rate limited; excess returns `429 Too Many Requests`.

**Security properties**

- Sessions are bound to the client IP address, so a change of address (for example a different Wi-Fi network) invalidates it.
- The session cookie is `HttpOnly`, and CSRF tokens or `SameSite` protect against forged requests.
- Session IDs come from a cryptographically secure random generator and are never reused.

**Good scripting practice**

```bash
curl -k -X DELETE "https://pi.hole/api/auth" -H "X-FTL-SID: <sid>"
```

A successful logout returns `204 No Content` and frees a slot immediately. Unused sessions are terminated automatically after a time, but do not rely on that.

**Checklist**

1. Log out in every script, including failure paths.
2. Reuse one session for several calls.
3. Raise `max_sessions` only if many clients legitimately log in.
4. Use HTTPS.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: API Authentication (api/auth); FTL Configuration Reference (ftldns/configfile). Nothing needed removing.
Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.pi-hole.api-authentication-sid
name: api-authentication-sid
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [api-sid, x-ftl-sid, api-login]
level: practitioner
status: docs-checked
description: "Log in to the Pi-hole API with POST /api/auth and present the session ID by URL, body, header or cookie."
sources: ["https://docs.pi-hole.net/api/auth/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# API authentication with a session ID

Pi-hole uses sessions, not static tokens. Post your password, or an application password, to `/api/auth`:

```bash
curl -k -X POST "https://pi.hole/api/auth" --data '{"password":"your-password"}'
```

A successful reply contains:

```json
{"session": {"valid": true, "totp": false, "sid": "...", "csrf": "...", "validity": 300}}
```

`validity` is seconds until expiry.

**Present the SID in one of four ways**

1. Query string: `?sid=<url-encoded-sid>`
2. JSON payload: `{"sid":"..."}`
3. Header: `X-FTL-SID: <sid>`
4. Cookie: `sid=<sid>`

With the cookie, also send the `X-FTL-CSRF` header carrying the `csrf` value from login.

**Errors on login**

- `400`: invalid JSON or missing `password`
- `401`: wrong password
- `500`: server-side problem such as out of memory

**Expiry.** Each successful request extends the session; long inactivity expires it and you log in again. The timeout is a config setting.

**Logout:** `DELETE /api/auth` with the SID, which returns `204`.

**Checklist**

1. Use HTTPS; `-k` is only for the self-signed certificate.
2. Prefer the header over the query string.
3. Log out when scripts finish.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: API Authentication (api/auth). Nothing needed removing.
Method: documentation only; no commands were run.

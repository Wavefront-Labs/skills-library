---
id: computing-software.cybersecurity-defensive.authelia.endpoint-rate-limits
name: endpoint-rate-limits
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, rate-limiting, token-bucket, brute-force, reset-password, openid-connect, totp]
level: advanced
status: docs-checked
description: "Tune Authelia's per-endpoint token-bucket rate limits for password reset, TOTP, Duo, session elevation and OpenID Connect endpoints, and tell them apart from regulation."
sources:
  - https://www.authelia.com/configuration/miscellaneous/server-endpoint-rate-limits/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia rate limits specific endpoints by default to stop faulty clients or brute force from consuming resources. This is separate from regulation, which silently bans users from the username and password form.

Each limiter has `enable` (true by default) and a list of `buckets`, every bucket being a `period` and a `requests` count:

```yaml
server:
  endpoints:
    rate_limits:
      second_factor_totp:
        enable: true
        buckets:
          - period: '1 minute'
            requests: 30
          - period: '10 minutes'
            requests: 50
```

Available limiters: `reset_password_start`, `reset_password_finish`, `second_factor_totp`, `second_factor_duo`, `session_elevation_start`, `session_elevation_finish`, and the OpenID Connect set `openid_connect_token`, `openid_connect_pushed_authorization_request`, `openid_connect_userinfo`, `openid_connect_introspection` and `openid_connect_revocation`.

The page's example configuration shows these values (the page says the limiters are enabled by default but does not label the numbers as defaults): reset start allows 5 requests per 10 minutes, 10 per 15 and 15 per 30; session elevation start allows 3 per 5 minutes, 5 per 10 and 15 per hour; the OpenID Connect endpoints allow 30 per minute, 40 per 2 minutes, 50 per 10 minutes and 100 per hour.

If `buckets` is set while `enable` is true, both `period` and `requests` are required in every bucket.

Check: exceed a bucket in a test environment and confirm further requests are refused until the period passes.

## Checked

2026-11-08. Read the full Authelia Server Endpoint Rate Limits page. Confirmed the limiter names, enable default true, bucket period and requests fields and their conditional requirement, and the distinction from regulation. The bucket figures are the page's example configuration and are now labelled as such. Removed unsourced advice about raising limits for machine clients.

Method: documentation only; no commands were run.

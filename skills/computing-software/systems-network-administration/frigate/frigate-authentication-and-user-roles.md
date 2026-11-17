---
id: computing-software.systems-network-administration.frigate.frigate-authentication-and-user-roles
name: frigate-authentication-and-user-roles
category: computing-software
field: systems-network-administration
product: frigate
tags: [authentication, admin-password-reset, login-rate-limit, trusted-proxies, session-length, jwt-secret, proxy-auth, role-map]
level: advanced
status: docs-checked
description: "Configure Frigate's built-in users, rate limiting, session length and JWT secret, or hand authentication to an upstream proxy with header and role mapping."
sources: ["https://docs.frigate.video/configuration/authentication/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Frigate authentication, JWT secret and proxy auth

Users are stored in the database with PBKDF2-SHA256 hashes (600,000 iterations); login issues a JWT cookie. Manage users under Settings, Users. Port `8971` is the authenticated UI and API (reverse proxies should use it); `5000` is unauthenticated and should be limited to the Docker network.

Onboarding: on first start an admin user and password are printed in the logs; change the password after logging in. Passwords need at least 12 characters. If locked out, set `auth.reset_admin_password: true` and read the new password from the logs on next startup.

Rate limiting: `auth.failed_login_rate_limit: "1/second;5/minute;20/hour"` (SlowApi notation) limits failing logins; restarting resets it. Behind a proxy set `auth.trusted_proxies` to the proxy's CIDR (for example the Compose network `172.18.0.0/16`), otherwise limits apply to the proxy IP and a brute-force attempt could lock out everyone.

`auth.session_length` is in seconds; default `86400` (24 hours), `0` forces login each access, `604800` is seven days without refresh.

JWT secret: anyone with it can mint valid tokens. Generate with `python3 -c 'import secrets; print(secrets.token_hex(64))'`. Frigate searches, in order, the `FRIGATE_JWT_SECRET` environment variable, a file of that name in `CREDENTIALS_DIRECTORY` (default `/run/secrets/`), the Home Assistant App `jwt_secret` option, then `.jwt_secret` in the config directory; if none exist it generates one. Changing it invalidates tokens.

Proxy authentication (Authelia, Authentik, oauth2_proxy, traefik-forward-auth): Frigate has no native OIDC, SAML or LDAP. Set `auth.enabled: False` and `proxy.auth_secret` to a long random string so only your proxy is trusted. `proxy.header_map` names the user header (`x-forwarded-user`) and role header (`x-forwarded-groups`); `proxy.separator` defaults to a comma (Authentik uses `|`). Roles are `admin`, `viewer` and custom roles; `proxy.default_role` sets the fallback when no role header is present, and it is also used when no `role_map` entry matches. `role_map` translates upstream group names (for example `sysadmins` to `admin`).

## Checked

2026-11-04. Confirmed against the Authentication page: PBKDF2-SHA256 with 600,000 iterations, ports 8971 and 5000, onboarding, admin password reset, 12-character minimum, rate limit notation and restart reset, trusted proxies, session length values, JWT secret lookup order, proxy auth keys, header mapping, separator, role_map and default role. Removed the claim that `none` returns 403 for unmapped users (not on the page).
Method: documentation only; no commands were run.

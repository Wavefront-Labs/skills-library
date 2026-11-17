---
id: computing-software.cybersecurity-defensive.zitadel.login-client-service-account
name: login-client-service-account
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, login-v2, service-account, pat, session-cookie, iam-login-client]
level: advanced
status: docs-checked
description: "Give a self-hosted ZITADEL Login UI its IAM_LOGIN_CLIENT credential and understand the session cookie signing fallback."
sources:
  - https://zitadel.com/docs/self-hosting/manage/login-client
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A self-hosted Login UI needs a token for a user with the IAM_LOGIN_CLIENT role (Instance Login Client). Place that service account in the dedicated administrator organization.

New installations can write a personal access token for the login client automatically during setup, as the deployment examples show. For an existing installation moving to a self-hosted v2 login, the setup job does not do this, so create it manually:

1. Create a service account in the console.
2. Create a PAT for it.
3. Save the PAT to a file such as `/path/on/your/host/login-client.pat`.
4. Make sure the user holds the Instance Login Client role at the instance administrators page.

Give the Login UI the token through the environment variable `ZITADEL_SERVICE_USER_TOKEN`, or mount the file and set `ZITADEL_SERVICE_USER_TOKEN_FILE`:

```bash
docker run -p 3000:3000 -v /path/on/your/host/login-client.pat:/path/in/container/login-client.pat:ro -e ZITADEL_SERVICE_USER_TOKEN_FILE=/path/in/container/login-client.pat ghcr.io/zitadel/zitadel-login:latest
```

The Login UI stores browser sessions in an httpOnly cookie and signs each entry. Without a dedicated secret it derives the key from the API credential, a deprecated fallback that logs a warning. Rotating that credential, for example creating a new PAT, then invalidates all existing session cookies and users must sign in again; application sessions and tokens are unaffected.

Set a dedicated secret with `ZITADEL_SESSION_COOKIE_SECRET` instead (at least 32 characters; a shorter value makes the Login UI log an error and report not ready on `/ready`). It accepts a comma-separated list: the first value signs, all values verify, which allows rotation without signing users out. All Login UI replicas must share the same secret.

To switch all users to the new Login UI, enable the `Login V2` feature flag on the instance and enter the Login UI base URI. Keep a PAT for an instance Owner user (`IAM_OWNER`) first so you can revert if you lock yourself out.

## Checked

2026-11-08. Read the login client page in full; added the dedicated session cookie secret and Login V2 enablement.

Method: documentation only; no commands were run.

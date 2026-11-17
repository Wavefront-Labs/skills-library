---
id: computing-software.systems-network-administration.netbird.selfhosted-automated-setup
name: selfhosted-automated-setup
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, self-hosted, api-setup, setup-pat, nb-setup-pat-enabled]
level: advanced
status: docs-checked
description: "Bootstrap a self-hosted NetBird owner and a personal access token via POST /api/setup with NB_SETUP_PAT_ENABLED, including request fields and security cautions."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/selfhosted/automated-setup.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For a self-hosted deployment using the embedded IdP/local user flow, with no existing owner (the setup endpoint works only while setup is required).

1. Set `NB_SETUP_PAT_ENABLED=true` on the Management container (the `netbird-server` service in the combined deployment, `management` in older multi-container ones) and run `docker compose up -d`.
2. Create the owner and PAT:
```
curl -fsS -X POST "${NETBIRD_URL}/api/setup" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","name":"Admin User","password":"<long-random>","create_pat":true,"pat_expire_in":7}'
```
The response has `user_id`, `email`, `personal_access_token`, shown once and sent with `Cache-Control: no-store`; do not log it in CI.
3. Use it: `Authorization: Token ${NETBIRD_PAT}`.

Fields: `email`, `name`, `password` required; `create_pat` ignored unless the env var is set; `pat_expire_in` is 1 to 365 days, default 1.

Troubleshooting: no token returned means the variable is unset, service not restarted, or `create_pat` not true; "setup already completed" means use an existing admin; a failure after owner creation rolls back, so fix and retry.

Security: the endpoint is unauthenticated while setup is pending. Enable only for controlled bootstrap, then disable the variable. For long-running automation create a service user and PAT, and delete the setup PAT.

## Checked

2026-11-04: read the automated setup page in full. Confirmed the env var and its placement, the request and response fields, the 1 to 365 day range with default 1, the no-store header, the troubleshooting cases and the security warning. Nothing removed.

Method: documentation only; no commands were run.

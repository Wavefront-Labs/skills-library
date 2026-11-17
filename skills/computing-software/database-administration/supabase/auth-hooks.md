---
id: computing-software.database-administration.supabase.auth-hooks
name: auth-hooks
category: computing-software
field: database-administration
product: supabase
tags: [auth-hooks, custom-access-token, send-email, send-sms, config-toml]
level: advanced
status: docs-checked
description: "Configure Supabase Auth hooks: hook list, config.toml keys, Postgres vs HTTP hooks, timeouts, retries, payload limit and required grants."
sources:
  - https://supabase.com/docs/guides/auth/auth-hooks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: customise Auth behaviour with SQL or HTTP hooks.

Hooks: Before User Created, Custom Access Token, Send SMS, Send Email, MFA Verification Attempt and Password Verification Attempt (the last two Teams and Enterprise only). Suggested function names: `custom_access_token`, `send_sms`, `send_email`, `mfa_verification_attempt`, `password_verification_attempt`.

Local config in `config.toml` under `[auth.hook.<hook_name>]` with `enabled = true` and `uri`. SQL hooks use `uri = "pg-functions://..."`. HTTP hooks use an HTTP URI plus `secrets`, e.g. `"env(SEND_SMS_HOOK_SECRETS)"`, in the format `v1,whsec_<base64-secret>` stored in `supabase/functions/.env`. Serve locally with `--no-verify-jwt`.

Limits:
- Postgres hooks: 2 seconds.
- HTTP hooks: 5 seconds for the whole invocation including retries; up to three retries with a two-second back-off.
- Payload: 20KB, sent uncompressed.

Rules:
- Custom Access Token, MFA Verification Attempt and Password Verification Attempt do not support a `204` return.
- Retryable statuses are 429 and 503, with a non-empty `retry-after` header. 400 and 403 are treated as 500.
- Responses need `Content-Type: application/json`. Postgres hook errors are not retryable.
- Grant `execute` on the function and `usage` on the schema to `supabase_auth_admin`; revoke execute from `authenticated`, `anon` and `public`; avoid `security definer`.
- HTTP hooks follow Standard Webhooks and verify `webhook-id`, `webhook-timestamp` and `webhook-signature`.
- Save hooks as migrations (`supabase migration new`).

## Checked

2026-11-04: Read the Auth Hooks guide in full, including the SQL and HTTP tab content (taken from the page's Markdown source on GitHub, because the rendered fetch drops the HTTP tab). Confirmed the hook list and plans, `config.toml` keys, `v1,whsec_<base64-secret>` secret format, `--no-verify-jwt`, 20KB uncompressed payload, 2 s and 5 s timeouts, retry rules, the 204 exclusions, the `Content-Type` requirement and the grants. Nothing removed.
Method: documentation only; no commands were run.

---
id: computing-software.database-administration.supabase.cli-config-auth
name: cli-config-auth
category: computing-software
field: database-administration
product: supabase
tags: [config-toml, auth-config, rate-limit, mfa, webauthn]
level: practitioner
status: docs-checked
description: "Supabase config.toml auth section defaults: site_url, jwt_expiry, rate limits, email, SMS, external providers, hooks, MFA, passkeys and sessions."
sources:
  - https://supabase.com/docs/guides/local-development/cli/config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set Auth behaviour for the locally running stack from `supabase/config.toml`; restart with `supabase stop` then `supabase start` for changes to take effect.

Core `[auth]` defaults:

```toml
[auth]
enabled = true
site_url = "http://localhost:3000"
additional_redirect_urls = ["https://localhost:3000"]
jwt_expiry = 3600
enable_manual_linking = false
enable_refresh_token_rotation = true
refresh_token_reuse_interval = 10
enable_signup = true
enable_anonymous_sign_ins = false
```

`[auth.rate_limit]` defaults: `email_sent = 2`, `sms_sent = 30`, `anonymous_users = 30`, `token_refresh = 150`, `sign_in_sign_ups = 30`, `token_verifications = 30`.

`[auth.email]`: `enable_signup = true`, `double_confirm_changes = true`, `enable_confirmations = false`, `max_frequency = "1m"`, `otp_length = 6`, `otp_expiry = 3600`. `[auth.email.smtp]` has `port = 2500` and `admin_email`; host, user, pass and sender_name default to none.

`[auth.sms]`: `enable_signup = true`, `enable_confirmations = false`, `test_otp` none; providers under `[auth.sms.<provider>]`.

External providers `[auth.external.<provider>]`: `enabled = false`, `client_id` (required), `secret` as `env(SUPABASE_AUTH_EXTERNAL_<PROVIDER>_SECRET)`, `url`, `redirect_uri`, `skip_nonce_check`.

Hooks `[auth.hook.<hook_name>]`: `enabled = false`, `uri`, `secrets`.

MFA: `[auth.mfa]` `max_enrolled_factors = 10`; `[auth.mfa.totp]`, `[auth.mfa.phone]` (`otp_length = 6`, `max_frequency = "10s"`) and `[auth.mfa.web_authn]` each have `enroll_enabled = false` and `verify_enabled = false`.

Also `[auth.passkey] enabled = false`, `[auth.webauthn]` (`rp_display_name`, `rp_id`, `rp_origins = []`; all three are required when `auth.passkey.enabled` is true), and `[auth.sessions]` `timebox` and `inactivity_timeout`, both none (sample values `'50m'`, `'20h'`).

Notes from the page: `auth.email.otp_length` must be between 6 and 10; `auth.rate_limit.anonymous_users` requires `enable_anonymous_sign_ins = true`; do not commit provider secrets, use `env(...)` substitution.

## Checked

2026-11-04: Read the Supabase CLI config reference (Auth section) in full and compared every key and default in the skill. All confirmed. Replaced "linked projects" in the goal, which the page does not state (it describes the locally running project), and added the passkey and OTP notes.
Method: documentation only; no commands were run.

---
id: computing-software.database-administration.supabase.passwordless-magic-link-otp
name: passwordless-magic-link-otp
category: computing-software
field: database-administration
product: supabase
tags: [magic-link, email-otp, passwordless, verify-otp, token-hash]
level: practitioner
status: docs-checked
description: "Supabase passwordless email sign-in: magic links and six-digit OTP codes, rate limits, expiry, shouldCreateUser, and the PKCE token_hash template."
sources:
  - https://supabase.com/docs/guides/auth/auth-email-passwordless
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: sign users in by email without a password.

Magic link: enabled by default; only the Site URL and configured redirect URLs are valid destinations (set on the URL Configuration page for hosted projects, in `config.toml` locally, or in the `.env` file when self-hosting). Call `signInWithOtp` with `email` (despite the name it sends a magic link by default). Auto sign-up is on; set `shouldCreateUser: false` to disable. `emailRedirectTo` sets the post-click destination. Rate limit one request per 60 seconds; links expire after 1 hour and work once.

PKCE flow: edit the Magic Link template to link to `{{ .SiteURL }}/auth/confirm` with `token_hash={{ .TokenHash }}` and `type=email`, then call `verifyOtp` with `token_hash` and `type: 'email'`.

Email OTP: enabled by default and shares the Magic Link template; add `{{ .Token }}` to the template to send a six-digit code. Same one-per-60-seconds limit.

Step 1, send: `signInWithOtp({ email, options: { shouldCreateUser: false } })`. On success `error` is null and both `user` and `session` in `data` are null.
Step 2, verify: `verifyOtp` with `email`, `token` and `type: 'email'`; success returns a session.

Expiry: default 1 hour, set under Authentication > Sign In / Providers > Auth Providers > Email > Email OTP expiration. Above 86,400 seconds is strongly discouraged and settable only through the Management API. This one setting also governs confirmation, password recovery, email change and invitation links.

## Checked

2026-11-04: Read the Passwordless email sign-in guide in full, with option names confirmed against the Markdown source on GitHub (the rendered text strips them). Confirmed defaults, rate limit, expiry, `shouldCreateUser`, `emailRedirectTo`, the PKCE template and `verifyOtp` parameters. Added where the redirect URLs are configured.
Method: documentation only; no commands were run.

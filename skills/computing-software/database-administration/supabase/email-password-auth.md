---
id: computing-software.database-administration.supabase.email-password-auth
name: email-password-auth
category: computing-software
field: database-administration
product: supabase
tags: [auth, email-password, sign-up, password-reset, phone-password]
level: intro
status: docs-checked
description: "Supabase Auth email and password sign-up, sign-in, reset, confirmation defaults, PKCE vs implicit flow, and phone and password with SMS."
sources:
  - https://supabase.com/docs/guides/auth/passwords
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: implement password sign-in correctly.

Email:
- Email auth is on by default. Hosted projects require confirmation by default; self-hosted and local projects do not. Toggle on the Auth Providers page (hosted) or with `auth.email.enable_confirmations` in the configuration file (self-hosted).
- `supabase.auth.signUp({ email, password })`; optional `emailRedirectTo` must be an allowed Redirect URL, otherwise users land on the site URL (default `localhost:3000`).
- `signInWithPassword()` signs in. `resetPasswordForEmail()` does not reveal whether an account exists; set the new password with `updateUser({ password })`.
- `current_password` can verify the old password before a change (supabase-js v2.102.0+, supabase-kt 3.5.0+).
- Flow: implicit is the default in JavaScript and Dart, PKCE in Swift, and SSR uses PKCE. PKCE confirmation emails link to `{{ .SiteURL }}/auth/confirm` with a `token_hash`, then call `verifyOtp`.
- The default email service allows 2 emails per hour and is best effort; use custom SMTP in production. Locally the CLI captures mail in Mailpit.

Phone:
- Enable on the Auth Providers page, or `auth.sms.enable_signup` when self-hosting. An SMS provider is required: MessageBird, Twilio, Vonage or TextLocal (community-supported).
- Users get a 6-digit PIN to verify within 60 seconds with `verifyOtp` type `sms`.
- `signUp({ phone, password })`, `signInWithPassword({ phone, password })`.
- Phone numbers get recycled, so the page discourages the method; enable MFA, tune rate limits and use CAPTCHA to control SMS cost.

Endpoints (the page's cURL examples): `POST /auth/v1/signup`, `POST /auth/v1/verify`, `POST /auth/v1/token?grant_type=password`.

## Checked

2026-11-04: Read the Password-based Auth guide in full (rendered text omits the PKCE and cURL tabs, so the Markdown source on GitHub was read too). Confirmed confirmation defaults, flow defaults, the PKCE email link and `verifyOtp`, the 2 emails per hour limit, the `current_password` versions, phone steps and the three endpoints. Named where each toggle lives.
Method: documentation only; no commands were run.

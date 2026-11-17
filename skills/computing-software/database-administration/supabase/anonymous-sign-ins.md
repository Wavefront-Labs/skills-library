---
id: computing-software.database-administration.supabase.anonymous-sign-ins
name: anonymous-sign-ins
category: computing-software
field: database-administration
product: supabase
tags: [anonymous, sign-in-anonymously, link-identity, is-anonymous, rls]
level: practitioner
status: docs-checked
description: "Supabase anonymous sign-ins: creating guest users, converting them to permanent accounts, RLS checks on is_anonymous, rate limits and cleanup SQL."
sources:
  - https://supabase.com/docs/guides/auth/auth-anonymous
  - https://supabase.com/docs/guides/local-development/cli/config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let visitors use the app before registering, then keep their data.

Calls (JavaScript):
- `supabase.auth.signInAnonymously()` creates the user.
- `supabase.auth.updateUser({ email })` links an email identity; the email or phone must be verified (link or 6-digit OTP) before `updateUser({ password })` adds a password.
- `supabase.auth.linkIdentity({ provider: 'google' })` links OAuth.
- `getSession()` lets you check `session.user.is_anonymous`.
- If the email belongs to an existing user, `updateUser` returns an error; the page's approach is `signInWithPassword({ email, password })` to the existing account, then reassign the anonymous user's rows and resolve conflicts yourself (overwrite, keep, or merge).

Settings: enabling anonymous sign-ins and manual linking is required to convert users; the page recommends invisible CAPTCHA or Cloudflare Turnstile against abuse. Locally, `auth.enable_anonymous_sign_ins` defaults to `false` in `config.toml`.

RLS: anonymous users use the `authenticated` role, so review existing policies. Check the claim with `(select (auth.jwt()->>'is_anonymous')::boolean) is false`. Use a restrictive policy for this and pair it with a permissive one (such as `using (true)`), because a single restrictive policy alone fails; policies are permissive by default and combine with OR. The `anon` API key does not create a user and uses the `anonymous` Postgres role.

Limits: an IP-based rate limit of 30 requests per hour, modifiable in the dashboard (`auth.rate_limit.anonymous_users`, default 30 per hour per IP, locally). Automatic cleanup is not available; delete old users yourself:

```sql
delete from auth.users where is_anonymous is true and created_at < now() - interval '30 days';
```

Next.js: the Supabase team has had reports of user metadata cached across anonymous users under static rendering; use dynamic rendering.

## Checked

2026-11-04: Read the Anonymous Sign-Ins guide and the CLI config reference in full. Confirmed the calls, RLS example, restrictive-policy note, 30 per hour limit, cleanup SQL and the `auth.enable_anonymous_sign_ins` default. Removed the unstated "dashboard auth providers" location.
Method: documentation only; no commands were run.

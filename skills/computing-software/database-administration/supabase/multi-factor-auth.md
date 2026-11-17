---
id: computing-software.database-administration.supabase.multi-factor-auth
name: multi-factor-auth
category: computing-software
field: database-administration
product: supabase
tags: [mfa, aal2, totp, restrictive-policy, factors]
level: practitioner
status: docs-checked
description: "Supabase MFA: assurance levels aal1 and aal2, factor APIs, enforcement options, restrictive RLS policies and downgrade timing after unenrolling."
sources:
  - https://supabase.com/docs/guides/auth/auth-mfa
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: require a second factor and enforce it in the database.

Assurance levels:
- `aal1`: conventional sign-in (password, magic link, OTP, phone or social). A JWT without an `aal` claim counts as `aal1`.
- `aal2`: sign-in plus at least one second factor (TOTP or one-time code).

API calls:
- `supabase.auth.mfa.listFactors()`: factors grouped into `totp` and `phone`.
- `supabase.auth.mfa.getAuthenticatorAssuranceLevel()`: the session's AAL.
- `supabase.auth.mfa.unenroll({ factorId })`: remove a factor.
- `refreshSession()`: unenrolling downgrades `aal2` to `aal1` only after the refresh interval lapses; call `refreshSession()` for an immediate downgrade (the page's sentence says "after enrolling", in the unenroll section). Users can only unenroll after completing enrollment and obtaining an `aal2` claim.
- REST: `https://<project-ref>.supabase.co/rest/v1/auth/factors` to check whether a user has enrolled factors; act only on `verified` factors.

Settings: the Dashboard option "Verification Disabled" turns off both the Challenge and Verify APIs; the Dashboard also controls the Enrollment API.

Enforcement choices:
- All users, new and existing.
- New users only (the page's cutoff is `2022-12-12T00:00:00Z`).
- Only users who opted in, meaning at least one `verified` factor.

Use `as restrictive` in every MFA RLS policy and do not omit it: a restrictive policy restricts all commands on the table regardless of other policies. The all-users template is `as restrictive to authenticated using ((select auth.jwt()->>'aal') = 'aal2')`; the other two cases compare the claim with `<@` against `array['aal2']` or `array['aal1','aal2']` chosen by `auth.users.created_at` or by a count of `verified` rows in `auth.mfa_factors`.

Server-side rendering: create a new Supabase client per request. A different AAL on the server is not necessarily a security problem (for example an abandoned MFA step), so the page recommends redirecting users to authenticate with the additional factor instead of returning 401 or 403.

Authentication methods in `amr` (an array of objects with `method` and `timestamp`, most recent first; `$.amr[0]` is the latest): `oauth`, `password`, `otp` (email code, SMS code, magic link), `totp`, `sso/saml`, `anonymous`; with PKCE also `invite`, `magiclink`, `email/signup`, `email_change`.

## Checked

2026-11-04: Read the MFA guide in full, including the FAQ accordion from the Markdown source on GitHub (the rendered text omits it). Confirmed assurance levels, APIs, Dashboard setting, the three enforcement choices, the policy templates and the `amr` methods. Reworded the unenroll downgrade note, replaced an unstated claim about permissive policies with the page's wording, and added the `amr` ordering and SSR advice.
Method: documentation only; no commands were run.

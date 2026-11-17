---
id: computing-software.database-administration.supabase.auth-sessions
name: auth-sessions
category: computing-software
field: database-administration
product: supabase
tags: [sessions, refresh-token, jwt-expiry, timebox, inactivity-timeout]
level: practitioner
status: docs-checked
description: "How Supabase Auth sessions work: access and refresh tokens, JWT expiry, session limits, reuse detection and detecting sign-out."
sources:
  - https://supabase.com/docs/guides/auth/sessions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune session lifetime and understand refresh behaviour.

A session is created at sign-in and by default lasts indefinitely; users can hold unlimited sessions across devices. It consists of an access token (a JWT) and a refresh token (a unique string). Access tokens are short-lived, typically 5 minutes to 1 hour. Refresh tokens never expire but are single-use: each yields a new access and refresh pair.

Sessions end on sign-out, password change or other security-sensitive action, inactivity timeout, maximum lifetime, or sign-in on another device. Each access token carries a `session_id` claim matching the primary key of `auth.sessions`; if no row exists, the user signed out.

Limits (Pro plan and above):
- Time-box user sessions: sessions end after a fixed duration (set a positive value in Auth settings).
- Inactivity timeout: sessions end if not refreshed within the timeout (positive duration in Auth settings).
- Single session per user: the session from the most recent sign-in stays active and the rest are terminated.
Sessions are not destroyed when you change these settings; the check runs at the next refresh, so effective duration is the configured timeout plus JWT expiry. Expired sessions are progressively deleted 24 hours after they expire.

JWT expiry defaults to 1 hour. Above 1 hour is discouraged; below 5 minutes (especially below 2) is generally avoided because of server load, clock skew and refresh timing.

Reuse detection: a refresh token may be reused within a 10-second default interval (not recommended to change). Reuse is also tolerated if the parent of the active token is used, returning the active token. Any other reuse ends the session and revokes all its refresh tokens. It can be disabled in Advanced Settings but generally should not be.

Cookies: HTTP-only cookies work only for traditional server-only web apps; with client-side JavaScript the browser cannot read or refresh the tokens. Set `Expires` or `Max-Age` far in the future so Auth controls validity.

## Checked

2026-11-04: Read the User sessions guide in full. Confirmed session lifetime, token behaviour, the three limits and Pro-plan requirement, the 24-hour cleanup, JWT expiry advice, reuse-detection exceptions, the `session_id` check and the cookie advice. Replaced the invented `timebox` and `inactivity_timeout` names with the Auth settings option names.
Method: documentation only; no commands were run.

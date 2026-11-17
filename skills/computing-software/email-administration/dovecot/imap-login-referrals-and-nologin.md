---
id: computing-software.email-administration.dovecot.imap-login-referrals-and-nologin
name: imap-login-referrals-and-nologin
category: computing-software
field: email-administration
product: dovecot
tags: [login-referrals, imap-referral, nologin, destuser, reason, rfc-2221]
level: intro
status: docs-checked
description: "Redirect IMAP clients to another server with login referrals, either as a suggestion or as a requirement, using passdb fields."
sources:
  - https://doc.dovecot.org/main/core/config/proxy/referrals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Login referrals (RFC 2221) redirect IMAP clients to a different server after hardware failure or organizational change, transparently and without client action. They are practically unused, so the page exists mostly for history. Dovecot does not use them by default. The `host` field is shared with proxying, and referrals apply only if the `proxy` field is unset.

Security caution: a man-in-the-middle can use referrals to send clients to a rogue password-collecting server. Enforcing TLS avoids this, and many clients do not support referrals anyway; Outlook does (but not Outlook Express).

Fields:
- `host` (required): destination hostname.
- `port`: default 143.
- `destuser`: tell the client to use a different username.
- `reason`: reply text. The default for a suggestion is "Logged in, but you should use this server instead."

Two modes:
- Suggest: return only the fields above; the client is logged in anyway.
- Require: also return `nologin`, with an optional reason (default "Try this server instead."). The user may not log in locally.

SQL examples: select `password, host, 'Y' as nologin` to forward a user after successful authentication. To send everyone away without authenticating, return `NULL AS password`, `'Y' AS nopassword`, the host, a reason such as "This server is down, try another one.", `'Y' AS nologin` and `'Y' AS nodelay`. Test with the clients you actually support before rollout.

## Checked

2026-11-03. Confirmed on the Login Referrals page: RFC 2221, rarely used, not on by default, the man-in-the-middle warning and TLS mitigation, the host field shared with proxying (referrals only without proxy), the host, port (default 143), destuser and reason fields with the default suggestion text, the nologin require mode with default "Try this server instead.", Outlook (not Express) support, and the two SQL examples. Nothing removed.

Method: documentation only; no commands were run.

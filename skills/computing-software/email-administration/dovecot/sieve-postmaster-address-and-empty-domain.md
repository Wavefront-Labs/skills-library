---
id: computing-software.email-administration.dovecot.sieve-postmaster-address-and-empty-domain
name: sieve-postmaster-address-and-empty-domain
category: computing-software
field: email-administration
product: dovecot
tags: [postmaster-address, empty-domain, auth-username-format, submission-host, sendmail-path, username-domain]
level: practitioner
status: docs-checked
description: "Configure the sender for Sieve rejects, vacations and forwards, and fix the common cause of an empty user domain."
sources:
  - https://doc.dovecot.org/main/core/config/sieve/submission.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sieve rejections, forwards and vacation replies need a sender and an outgoing path. `postmaster_address` is the From address for rejections; a value like `postmaster@%{user | domain}` uses the recipient domain. Mail is sent through the SMTP server named by `submission_host` (for example `smtp-out.example.com:25`), or alternatively through the sendmail binary named by `sendmail_path`.

If `%{user | domain}` is empty, remember that IMAP and POP3 have no domain concept. The domain comes from a `user@domain` login, and if the name has no `@domain` the domain is empty unless `auth_default_domain` is set. If you log in as `user@domain` and the domain is still empty, something in the configuration changed the username into a plain name. Dovecot does not track the domain separately. With `auth_debug = yes` the loss shows in logs as `username changed user@domain.org -> user`.

Common causes:
- `auth_username_format` used globally changes the username permanently; inside a passdb or userdb it changes it only for that lookup.
- An SQL passdb that selects `username AS user` drops the domain. Instead return `concat(username, '@', domain) AS user`, or return `username` and `domain` as separate fields and let Dovecot merge them into one user.

When filtering on separate columns, use `%{user | username}` and `%{user | domain}` in the WHERE clause, as the example does. Fix the username source, then retest bounces and vacation messages.

## Checked

2026-11-08. Read the Configuring Sieve and Submission page in full. Added the submission_host example, the sendmail binary wording and the auth_debug log line.

Method: documentation only; no commands were run.

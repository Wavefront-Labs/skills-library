---
id: computing-software.email-administration.dovecot.multiple-passdbs-and-userdbs-fallback
name: multiple-passdbs-and-userdbs-fallback
category: computing-software
field: email-administration
product: dovecot
tags: [multiple-passdb, passdb-fallback, system-and-virtual-users, home-directory, mail-path, auth-order]
level: practitioner
status: docs-checked
description: "Chain several passdbs or userdbs so system and virtual users share one server, including the PLAIN-only fallback limit and per-user mail paths."
sources:
  - https://doc.dovecot.org/main/core/config/auth/multiple.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot can list several authentication databases. If the password does not match in the first passdb, it tries the next. A typical use is supporting both local system users from /etc/passwd and virtual users.

Limits and behaviour:
- The fallback works only with the PLAIN authentication mechanism.

Mail location differs between system and virtual users. The cleanest solution is to always store mail under the home directory: have both userdbs return a home (virtual users get something like `/var/vmail/%{user | domain}/%{user | username}`) and set `mail_path = ~/Maildir`.

If virtual users cannot have a home directory (avoid this if possible), point all databases at the system users' mail location and let the virtual userdb override it by returning a mail location extra field.

The documented example sets `mail_driver = maildir` and `mail_path = ~/Maildir` for both populations, then chains:
- `passdb sql` first (query returns `userid AS user, password` from the users table), with `passdb pam` as the fallback;
- `userdb sql` first (query returns `uid`, `gid` and a `home` built from the user's domain and username parts), looked up even if authentication was done through PAM, with `userdb passwd` as the fallback for users not found in SQL.

Order the databases accordingly: the first one that matches wins, and later ones are only tried when the earlier one does not match the password or the user.

## Checked

2026-11-08. Read the Multiple Databases page in full. Replaced a paraphrase of the SQL example with what it actually shows (SQL then PAM passdb, SQL then passwd userdb) and corrected the ordering advice.

Method: documentation only; no commands were run.

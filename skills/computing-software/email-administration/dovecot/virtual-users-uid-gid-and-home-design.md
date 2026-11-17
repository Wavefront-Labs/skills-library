---
id: computing-software.email-administration.dovecot.virtual-users-uid-gid-and-home-design
name: virtual-users-uid-gid-and-home-design
category: computing-software
field: email-administration
product: dovecot
tags: [virtual-users, home-directory, vmail-user, uid-gid, mail-directory, userdb-fields]
level: practitioner
status: docs-checked
description: "Design virtual users: databases to use, a vmail UID rather than the dovecot user, a unique absolute home per user and how home differs from the mail directory."
sources:
  - https://doc.dovecot.org/main/core/config/auth/users/virtual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From Dovecot's view there is little difference between system and virtual users: if a passwd lookup and an SQL lookup return the same userdb data, behaviour is identical. Common backends are LDAP, SQL and passwd-file. They normally supply the password, UID and primary GID, and a home directory and/or mail location.

Domains: IMAP and POP3 have no concept of domain. `%{user | username}` and `%{user | domain}` merely help with `user@domain` names, and `domain%user` names work too. Some mechanisms use realms, which makes the username `user@realm`.

Dovecot does not tell you the password format; set a default scheme or prefix each password with `{scheme}`.

Important rules:
- Dovecot does not access mail as the `dovecot` user. Do not put `dovecot` in the mail group or make mail owned by it. Use one `vmail` user that owns all mail, or a UID per user.
- GIDs rarely matter unless you use shared mailboxes with several UIDs.
- The home directory is the user's private state directory, unrelated to system home directories. Never return the same home for multiple users. It must be an absolute path.

Home holds Sieve scripts, the duplicate-check database (vacation suppression fails without a home) and core files from crashes.

Keep home and mail directory separate for mbox and Maildir, because non-mailbox files may appear as mailboxes and names like `dovecot.sieve` conflict. With dbox sharing is fine. The preferred layout puts the mail directory under home.

## Checked
2026-11-09. Read the Dovecot Virtual Users page (main documentation, marked pre-release) in full, through the home
directory layouts. Confirmed each statement: system versus virtual users, databases, domains and realms, password
scheme prefixes, the vmail UID rule, GIDs, home directory rules and uses, and the home versus mail directory advice.
Nothing removed.
Method: documentation only; no commands were run.

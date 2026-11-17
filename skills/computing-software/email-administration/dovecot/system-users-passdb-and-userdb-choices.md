---
id: computing-software.email-administration.dovecot.system-users-passdb-and-userdb-choices
name: system-users-passdb-and-userdb-choices
category: computing-software
field: email-administration
product: dovecot
tags: [system-users, pam, passwd-userdb, nss, userdb-use-worker, mail-spool]
level: intro
status: docs-checked
description: "Serve system users: which passdb to pick (PAM, BSD, passwd or others), the passwd userdb, NSS with LDAP, and mail storage choices."
sources:
  - https://doc.dovecot.org/main/core/config/auth/users/system.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
System users usually come from /etc/passwd, but NSS can fetch them elsewhere such as LDAP. The userdb for system users is always the passwd authentication database. With nss_ldap you must set `userdb_use_worker = yes`.

Separate UIDs are good security: the kernel stops users reading each other's mail. But if users have direct write access to mail files (shell access), they can corrupt mailboxes and trigger confusing errors in Dovecot's logs. When other software also touches mailboxes, accesses must be compatible; with mbox this mainly means all programs use the same locking methods in the same order.

Passwords: admins often want IMAP and POP3 passwords different from SSH, since mail clients commonly send passwords with little protection. Dovecot supports non-system passwords for system users.

For system passwords use one of:
- PAM, most common on Linux and BSD.
- BSD authentication, used on OpenBSD.
- The passwd database, mainly some BSDs.

For separate passwords choose almost any passdb; passwd-file suits simple installs.

Mail storage: UNIX defaults deliver to /var/mail/username or /var/spool/mail/username in mbox. You can keep that or move to Maildir or dbox. Always set the mail location explicitly, so new users without an existing mailbox behave correctly. For mbox, /var/mail/username is the INBOX, and other mailboxes go in a directory like ~/mail or ~/Mail. Do not put the INBOX path inside the `mail_path` root.

## Checked
2026-11-09. Read the Dovecot System Users page (main documentation, marked pre-release) in full. Confirmed each
statement: NSS and `userdb_use_worker`, UID separation, direct-write corruption, mbox locking compatibility, the three
system-password passdbs, separate passwords, mail location defaults and the mbox INBOX/`mail_path` rule. Nothing removed.
Method: documentation only; no commands were run.

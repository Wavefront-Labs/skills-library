---
id: computing-software.email-administration.dovecot.doveadm-purge-and-force-resync-repair
name: doveadm-purge-and-force-resync-repair
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-purge, refcount, force-resync, mdbox-repair, sdbox, mailbox-repair]
level: advanced
status: docs-checked
description: "Reclaim space from refcount-zero messages with doveadm purge and repair stuck mailboxes with force-resync."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-purge.1.html
  - https://doc.dovecot.org/main/core/man/doveadm-force-resync.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm purge` removes messages whose refcount is 0 from a user's storage. A message's refcount reaches 0 when the user or an administration tool has expunged every instance of it from all mailboxes. The manual describes it as removing refcount=0 messages from mdbox files, so it matters for dbox storage where expunged mail is not freed immediately. It accepts the usual user selectors: `-A` for all users, `-F file`, `-u user` with wildcards, or `USER` with `--no-userdb-lookup`; `-S` runs it through a socket.

`doveadm force-resync` handles cases where Dovecot cannot solve mailbox problems automatically. It tries to fix every problem it can. For sdbox and mdbox, the storage files are also checked. You give it a user selector and a mailbox name, for example `doveadm force-resync -u bob INBOX`; with mdbox all of the mailboxes are fixed, so any mailbox name such as INBOX works.

Operational notes:
- Run `force-resync` for one user first and check the logs for errors.
- It is for mailbox problems Dovecot cannot fix on its own, not for routine maintenance.
- With `-A` and an SQL or LDAP userdb, the iterate query or fields must match your schema.

The same global options apply as for other doveadm commands, such as `-o` overrides and output formatters.

## Checked

2026-11-08. Read doveadm-purge(1) and doveadm-force-resync(1) in full. Removed unsourced NFS and scheduling advice and an invented wildcard mailbox name for force-resync (the page uses INBOX); added the documented example.

Method: documentation only; no commands were run.

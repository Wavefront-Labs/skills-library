---
id: computing-software.email-administration.dovecot.doveadm-acl-rights-and-identifiers
name: doveadm-acl-rights-and-identifiers
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-acl, acl-rights, group-override, acl-debug, lookup-read-write, acl-identifiers]
level: advanced
status: docs-checked
description: "Manage mailbox ACLs from the command line: identifier types and precedence, Dovecot right names, group-override and acl debug."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-acl.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm acl` handles Access Control List actions. An identifier is one of `group-override=name`, `user=name`, `owner`, `group=name`, `authenticated`, `anyone`, or `anonymous` (an alias for anyone). ACLs are processed in that order of precedence, so you can give a group read access and then remove it for specific users inside the group.

Group-override overrides users' ACLs, so it can temporarily disable someone. With `user=timo rw` and a `group-override=tempdisabled` entry carrying no rights, timo has no access while he is a member of `tempdisabled`; an ordinary group entry could not do this, because `user=timo` would win.

Dovecot right names (IMAP ACL letters are not supported directly):
- l lookup: visible in lists, can be subscribed.
- r read: can be opened.
- w write: change flags and keywords except \Seen and \Deleted.
- s write-seen, t write-deleted.
- i insert: messages can be written or copied in.
- p post: dovecot-lda may deliver, for example from Sieve.
- e expunge.
- k create: create or rename directly under this mailbox (renaming also needs delete).
- x delete.
- a admin: change ACLs.

Subcommands include `acl add mailbox id right ...` (existing rights for that id are preserved), `acl set` (replaces existing rights), `acl remove` (removing every right leaves an empty entry), `acl delete mailbox id` (removes the whole entry), `acl get`, `acl rights`, `acl recalc` (fixes the user's shared mailboxes in acl_sharing_map), and `acl debug mailbox`, which lists exactly why a shared mailbox is inaccessible to a user. Mailbox names accept `*` and `?` wildcards. Start with `acl debug` for any "shared folder missing" report.

## Checked

2026-11-08. Read doveadm-acl(1) in full. Corrected the identifier list and precedence order (group-override first, anonymous as alias for anyone), made the group-override example match the source, and added the set, remove, get, rights and recalc subcommands.

Method: documentation only; no commands were run.

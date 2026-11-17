---
id: computing-software.email-administration.dovecot.shared-public-mailboxes-namespace
name: shared-public-mailboxes-namespace
category: computing-software
field: email-administration
product: dovecot
tags: [public-namespace, shared-mailboxes, mail-index-private-path, subscriptions, maildir-layout, acl-sharing]
level: practitioner
status: docs-checked
description: "Create public shared mailboxes with a public namespace, per-user flags via private indexes, subscriptions and the ACL requirement."
sources:
  - https://doc.dovecot.org/main/core/config/shared_mailboxes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot supports sharing in a single-backend setup in three ways: public shared mailboxes made by administrators, user-to-user sharing, and symlinks as a quick hack. Sharing across several backends needs Dovecot Pro. Filesystem permission problems matter only when a shared filesystem is used.

Public mailboxes live under a public namespace. For Maildir public folders, define the namespace with a mail path such as `/var/mail/public/` and create Maildir folders in it. Maildir++ layout requires folder names to begin with `.` or Dovecot ignores them; the `fs` layout gives plain directories.

Per-user read flags: create private indexes with `mail_index_private_path`. This writes `dovecot.index.pvt[.log]` files holding only message UIDs and private flags; the private flag list is currently hardcoded to \Seen. Do not use a per-user `mail_control_path`, since then `dovecot-keywords` is not shared and keyword mapping breaks.

Subscriptions: set `subscriptions=no` on the public namespace so each user's subscriptions come from the parent namespace file. Ensure an empty-prefix namespace exists, otherwise create one with `alias_for` naming the INBOX namespace.

Read-only trees need index and control files elsewhere. With several namespaces, control and index paths must differ per namespace, or identically named mailboxes collide. If control files are per-user, index files must be as well.

Grant rights using an `acl` block per folder in dovecot.conf or a `dovecot-acl` file in each folder (for example `user=someone lr`). The namespace type must be `public` whatever its prefix, and `acl_sharing_map` is irrelevant here.

## Checked

2026-11-03. Confirmed on the Shared Mailboxes page: the three sharing kinds and Dovecot Pro for multi-backend sharing, the public namespace and Maildir++ dot-prefix rule versus the fs layout, mail_index_private_path creating dovecot.index.pvt[.log], the per-user mail_control_path keyword warning, subscriptions = no with an empty-prefix alias_for namespace, read-only Maildir/mbox path rules, per-namespace control/index paths, and public-namespace ACLs (namespace type public, dovecot-acl, acl_sharing_map not relevant). Added the \Seen-only private flag detail.

Method: documentation only; no commands were run.

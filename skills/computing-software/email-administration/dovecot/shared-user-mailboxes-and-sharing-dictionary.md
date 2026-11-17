---
id: computing-software.email-administration.dovecot.shared-user-mailboxes-and-sharing-dictionary
name: shared-user-mailboxes-and-sharing-dictionary
category: computing-software
field: email-administration
product: dovecot
tags: [shared-namespace, acl-sharing-map, namespace-list, owner-home, dict, user-shared]
level: advanced
status: docs-checked
description: "Let users share mailboxes through a shared namespace, owner variables, the dictionary that makes them visible and dbox index warnings."
sources:
  - https://doc.dovecot.org/main/core/config/shared_mailboxes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
User-to-user sharing needs a shared namespace plus the ACL plugin. A `shared/` namespace holds each sharing user's mailboxes. With multiple domains, put the owner into the prefix, as in `shared/$domain/$username/`, or use `$user`. Since 2.4.0 the template variables are `$user`, `$username` and `$domain`, replacing the old `%%u`, `%%n` and `%%d`.

The page's example namespace is `type = shared`, `prefix = shared/$user/`, `mail_path = %{owner_home}/Maildir`, `subscriptions = no`, `list = children`, with `acl = yes` in `mail_plugins`, `imap_acl = yes` under `protocol imap`, and `acl_driver = vfile`. The page says `list = children` hides the `shared` directory from LIST when nobody shares with the user; setting it to yes always shows it.

The owner is reachable as `%{owner_user}`, `%{owner_username}` and `%{owner_domain}`, and the owner's home through the userdb as `%{owner_home}`. Use these in the mail location. If mailboxes can be found from a template, avoid `%{owner_home}` as it is slightly more efficient.

dbox warning. Index files are essential in dbox, so never move `mail_index_path` to a per-user location; this corrupts mailboxes. `mail_index_private_path` is allowed.

Visibility. With only the namespace configured, you can open a shared mailbox by name but it will not appear in the mailbox list, because Dovecot cannot know who shared with whom, and scanning every user's directories would be too slow. A dictionary stores which users share to which, configured through `acl_sharing_map` (for example `dict file { path = /var/lib/dovecot/db/shared-mailboxes.db }`, or SQL via a dict proxy). Users missing from the dictionary have invisible shares. IMAP processes must be able to write to the dictionary directory. There is no way to rebuild the dictionary automatically, so keep it from being lost; if it is, each sharing user must run IMAP `SETACL` (or `doveadm acl`) again to repopulate their entries. That is the only way to update the shared mailbox list dictionary.

## Checked
2026-11-09. Read the whole Dovecot "Shared Mailboxes" page (doc.dovecot.org/main/core/config/shared_mailboxes.html) and confirmed each statement above. Replaced the vague "ACL tools or your own scripts" claim with the page's SETACL / doveadm acl rebuild rule; used the page's `list = children` setting name.

Method: documentation only; no commands were run.

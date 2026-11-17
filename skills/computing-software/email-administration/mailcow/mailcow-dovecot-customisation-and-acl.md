---
id: computing-software.email-administration.mailcow.mailcow-dovecot-customisation-and-acl
name: mailcow-dovecot-customisation-and-acl
category: computing-software
field: email-administration
product: mailcow
tags: [dovecot-extra-conf, public-folders, shared-acl, acl-anyone, mail-crypt, very-dirty-syncs, maildir-encryption]
level: advanced
status: docs-checked
description: "Customise mailcow's Dovecot safely through extra.conf, including a public namespace with ACLs, the ACL_ANYONE switch, maildir_very_dirty_syncs and the mail-crypt storage format."
sources: ["https://docs.mailcow.email/manual-guides/Dovecot/u_e-dovecot-extra_conf/", "https://docs.mailcow.email/manual-guides/Dovecot/u_e-dovecot-public_folder/", "https://docs.mailcow.email/manual-guides/Dovecot/u_e-dovecot-any_acl/", "https://docs.mailcow.email/manual-guides/Dovecot/u_e-dovecot-performance/", "https://docs.mailcow.email/manual-guides/Dovecot/u_e-dovecot-mail-crypt/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customising Dovecot in mailcow

Put your own settings in `data/conf/dovecot/extra.conf` (create it if missing) and restart `dovecot-mailcow`. Changes to the stock `dovecot.conf` can be overwritten by an update.

Public folder: define a namespace in `extra.conf` with `type = public`, `separator = /`, `prefix = Public/`, `location = maildir:/var/vmail/public:INDEXPVT=~/public`, `subscriptions = yes` and a `mailbox "Develcow" { auto = subscribe }` block (drop `:INDEXPVT=` if per-user seen flags are not wanted). Grant access with `doveadm acl set -A "Public/Develcow" "authenticated" lookup read write write-seen write-deleted insert post delete expunge create`. For the whole namespace, create a `dovecot-acl` file in the namespace root containing `authenticated kxeilprwts`. Limit single users with `doveadm acl set -u user@domain ...`.

Since 17 August sharing with "any" or all authenticated users is disabled; re-enable with `ACL_ANYONE=allow` in `mailcow.conf` and apply with `docker compose up -d`.

Performance: `maildir_very_dirty_syncs` has been on by default since release 2023-05. It avoids rescanning the whole `cur` directory when loading mail and is safe unless something other than IMAP modifies files under `cur`. If third-party tools edit the maildir directly, set `maildir_very_dirty_syncs=no` in `extra.conf`.

Storage: mail is stored lz4-compressed and encrypted, with the key pair in `crypt-vol-1`. The docs include a risky loop using `doveadm fs get` and `doveadm fs put` to decrypt or encrypt existing maildir files; use at your own risk.

## Checked

2026-11-04. Confirmed on the extra.conf, Public folders, any ACL, Performance and Mail crypt pages: data/conf/dovecot/extra.conf and the dovecot-mailcow restart, the public namespace block and INDEXPVT note, the doveadm acl set command, the dovecot-acl file content kxeilprwts, ACL_ANYONE=allow (disabled on 17 August), maildir_very_dirty_syncs default since 2023-05 and its disable setting, and lz4 compression plus encryption with keys in crypt-vol-1 and the at-your-own-risk script. Fixed: applying ACL_ANYONE uses docker compose up -d.

Method: documentation only; no commands were run.

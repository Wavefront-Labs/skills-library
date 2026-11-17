---
id: computing-software.email-administration.dovecot.doveadm-mailbox-create-delete-list
name: doveadm-mailbox-create-delete-list
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-mailbox, mailbox-create, mailbox-delete, mailbox-list, subscriptions, mutf7]
level: practitioner
status: docs-checked
description: "Create, list and delete mailboxes in bulk with doveadm mailbox, including subscription, recursion, emptiness checks and UTF encoding options."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-mailbox.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`doveadm mailbox` queries and modifies mailboxes. A mailbox name is as IMAP clients see it, but in UTF-8. The hierarchy separator is commonly `/` or `.` depending on mailbox format and namespace configuration. Users are selected with `-A`, `-u`, `-F` or `--no-userdb-lookup`.

- `create [-g guid] [-s] mailbox...`: creates one or more mailboxes, in the format given by `mail_driver` or the userdb `mail` field. `-g` assigns a specific GUID. `-s` also subscribes the user.
- `delete [-s] [-r] [-e] [-Z] mailbox...`: deletes a mailbox and expunges its messages. Children survive unless `-r` is given. `-e` requires the mailbox to be empty first. `-Z` is the fastest delete but may leave the user in an inconsistent state, with quota wrong for example; it is mainly for removing a whole user. `-s` also unsubscribes.
- `list [-7 | -8] [-s] [mailbox ...]`: lists mailboxes with wildcards. `-7` prints mUTF-7, `-8` prints UTF-8. `-s` lists only subscribed ones, which can include already deleted mailboxes.

There is also `mailbox cryptokey` for the mail crypt plugin keys.

Other subcommands on the page: `rename old new` (`-s` unsubscribes the old name and subscribes the new one), `subscribe` and `unsubscribe`, `status [-t] fields mailbox...` (fields include guid, highestmodseq, messages, deleted, recent, uidnext, uidvalidity, unseen, vsize, firstsaved; quote several; `-t` sums messages, recent, unseen and vsize), `path [-t type]` (index is the default location type), `mutf7 [-7|-8] name...` (converts names; default converts UTF-8 to mUTF-7), `metadata list|get|set|unset`, `update` (UID validity and similar values; only for migration or disaster recovery, highly discouraged and not supported by all backends), and `cache purge|decision|remove` (`cache remove` can erase all cached data and slow the system). Check each one's options before scripting, and run against a single test user first.

Use `list` to audit what a user really has when a client shows a different view, since doveadm shows the server's list regardless of subscriptions unless `-s` is used.

## Checked

2026-11-08. Read doveadm-mailbox(1) in full. Create, delete and list details were accurate; replaced a vague line with the remaining subcommands (rename, status, path, mutf7, metadata, update, cache) and their documented cautions.

Method: documentation only; no commands were run.

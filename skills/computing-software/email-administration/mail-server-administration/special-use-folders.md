---
id: computing-software.email-administration.mail-server-administration.special-use-folders
name: special-use-folders
category: computing-software
field: email-administration
product: mail-server-administration
tags: [special-use-folders, special-use, autocreate, namespace-inbox]
level: practitioner
status: docs-checked
description: "Configure Dovecot special-use mailboxes (Sent, Drafts, Trash, Junk) with auto-create so clients find them."
sources:
  - https://doc.dovecot.org/2.3/configuration_manual/namespace/
  - https://doc.dovecot.org/2.3/settings/core/
  - https://doc.dovecot.org/main/core/man/doveadm-mailbox.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Special use folders

**Goal:** consistent folders across clients.
## Steps
1. In the `namespace inbox` block add:
```
mailbox Drafts {
  special_use = \Drafts
  auto = subscribe
}
mailbox Sent {
  special_use = \Sent
  auto = subscribe
}
mailbox Trash {
  special_use = \Trash
  auto = subscribe
}
mailbox Junk {
  special_use = \Junk
  auto = subscribe
}
```
`auto = subscribe` creates and subscribes the mailbox.
2. Reload: `doveadm reload`.
3. Sieve file-into rules can then use `Junk`.
## Failure modes
- `special_use` values are not validated; use only the RFC 6154 flags (`\Drafts`, `\Sent`, `\Trash`, `\Junk`).
## Verify
- `doveadm mailbox list -s -u alice@example.com` shows the special folders subscribed.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 Namespace page and settings reference (`mailbox` blocks with `special_use` and `auto = subscribe`, no validity check on special_use values) and the doveadm-mailbox man page (`mailbox list -s`). Reformatted the blocks to the multi-line form the docs use. Removed the unsourced remark about client-created folders and the RFC 3501/9051 sources (not relevant here).

Method: documentation only; no commands were run.

---
id: computing-software.email-administration.mailcow.mailcow-mailbox-features-spam-filter-tags-aliases
name: mailcow-mailbox-features-spam-filter-tags-aliases
category: computing-software
field: email-administration
product: mailcow
tags: [user-spam-filter, domain-blacklist, global-filter-maps, ui-tags, sub-addressing, temporary-aliases, forgot-password]
level: practitioner
status: docs-checked
description: "Use mailcow's per-user spam filter, domain and global black/whitelists, UI tags, plus-addressing actions, temporary aliases and the forgot-password flow."
sources: ["https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-spamfilter/", "https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-bl_wl/", "https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-tags/", "https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-sub_addressing/", "https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-spamalias/", "https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-forgot_password/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow mailbox features: filters, tags, aliases

Spam filtering at three levels: a mailbox user adjusts their own score and black/whitelist on the Spam filter tab; a domain administrator edits the domain-wide list under Configuration, Email Setup, Domains, Edit Domain, Spam Filter (a user's own lists can override it); and the server-wide regex maps are under Configuration and Details, Global filter maps. Global thresholds are set in Rspamd files.

UI tags (mailcow 2022-05 or newer) label domains and mailboxes so you can sort and search by tag in the Domain and Mailbox lists. They are not the same as sub-addressing.

Sub-addressing (RFC 5233, plus addressing) lets users receive at `me+facebook@example.org`. Under Mailbox, Settings the user chooses to move the message to a subfolder named after the tag (created in lower case if missing) and/or prepend `[tag]` to the subject. Tags are lowercased except the first letter; to keep case, remove the `:lower :upperfirst` modifiers in `data/conf/dovecot/global_sieve_after` and restart.

Temporary email aliases (spam aliases) for addresses you give out but want no ongoing mail from are created, deleted or extended by the mailbox user on the Temporary email aliases tab.

Forgot password (mailcow 2024-08 or newer): the admin configures a sender address (its domain must be fully set up) and subject; the user needs a backup email address, different from the account, ideally at another provider, and must read it before the link expires.

## Checked

2026-11-09. Confirmed on the six UI pages (spam filter, black and whitelist, tags, sub-addressing, spam alias, forgot password): per-user spam tab, domain-wide path and user override, global filter maps, tags from 2022-05, plus addressing actions and the global_sieve_after lowercase modifiers, temporary alias tab, and the 2024-08 forgot-password requirements. No changes needed.

Method: docs-checked 2026-11-09 against all six cited pages (raw markdown in mailcow-dockerized-docs).

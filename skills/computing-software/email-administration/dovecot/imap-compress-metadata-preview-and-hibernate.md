---
id: computing-software.email-administration.dovecot.imap-compress-metadata-preview-and-hibernate
name: imap-compress-metadata-preview-and-hibernate
category: computing-software
field: email-administration
product: dovecot
tags: [imap-compress, imap-metadata, imap-hibernate, special-use, preview, full-text-search]
level: practitioner
status: docs-checked
description: "Configure IMAP extensions: COMPRESS and proxy handling, METADATA in SQL, special-use mailboxes, PREVIEW and imap-hibernate."
sources:
  - https://doc.dovecot.org/main/core/config/imap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot was optimized for IMAP from the start and supports many extensions.

- COMPRESS (RFC 4978): clients can enable stream compression dynamically. It is on by default with the default level for each mechanism. Behind a Dovecot proxy, compression is handled by the proxy rather than the backend imap process (`imap_compress_on_proxy`).
- SEARCH: part of core IMAP, so activate a full text search driver to make server-side searches fast.
- METADATA (RFC 5464): per-mailbox, per-user data via IMAP. Configure it with `imap_metadata`. Metadata can be stored in an SQL dictionary using a dedicated table. The username column is a primary key and must have a value: empty means the entry applies to keys with the `shared/` prefix, while `priv/` keys need a non-empty username.
- Special-use mailboxes: none configured by default. Use the `@mailbox_defaults` group to include the recommended defaults with special-use flags, or configure mailbox settings explicitly.
- PREVIEW (RFC 8970): fetched with FETCH, enabled by default. Preview text is generated at delivery and stored in the index files.
- Hibernation: connections that issue IDLE move to a holding process, `imap-hibernate`, which keeps them until a command needs a full imap process again. Since 2.4.6, connections that are not in IDLE but have no command running can also hibernate. `imap_hibernate_timeout` sets the delay before the move and requires IPC between imap and imap-hibernate. Hibernation is not supported on kqueue-based systems such as FreeBSD.

Hibernation saves memory and CPU because one imap-hibernate process holds all the idle connections.

## Checked

2026-11-03. Confirmed on the IMAP Configuration page: COMPRESS (RFC 4978) on by default and handled by the proxy (imap_compress_on_proxy), SEARCH needing an FTS driver, METADATA (RFC 5464) with imap_metadata and the SQL dict table rules for the username column, special-use via @mailbox_defaults or mailbox_special_use, PREVIEW (RFC 8970) enabled by default and stored at delivery, imap-hibernate with imap_hibernate_timeout (non-IDLE hibernation added 2.4.6). Fixed: the kqueue/FreeBSD limitation applies to hibernation, not PREVIEW; removed the unconfirmed "mobile clients" memory claim.

Method: documentation only; no commands were run.

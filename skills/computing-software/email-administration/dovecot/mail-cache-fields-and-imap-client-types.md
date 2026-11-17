---
id: computing-software.email-administration.dovecot.mail-cache-fields-and-imap-client-types
name: mail-cache-fields-and-imap-client-types
category: computing-software
field: email-administration
product: dovecot
tags: [mail-cache, mail-cache-fields, mail-always-cache-fields, mail-never-cache-fields, dovecot-index-cache, imap-envelope]
level: advanced
status: docs-checked
description: "Seed and pin dovecot.index.cache fields for new users, migrations and webmail with mail_cache_fields, always and never lists."
sources:
  - https://doc.dovecot.org/main/core/config/mail_cache.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot writes headers and other fields into `dovecot.index.cache` automatically, per folder, based on what the IMAP client uses. This works for new folders but poorly during migration, because Dovecot does not yet know what to cache; it also matters when someone who usually uses a phone logs into webmail occasionally and the webmail fields would otherwise be dropped.

Settings:
- `mail_cache_fields`: fields initially cached for newly created users; afterwards decisions follow access patterns. INBOX caching decisions are copied to new folders.
- `mail_always_cache_fields`: always cached for everyone and never dropped.
- `mail_never_cache_fields`: never cached; normally only `imap.envelope`, since it can be generated from cached header fields.

Common field names: `flags`, `date.received`, `date.sent`, `size.physical`, `imap.bodystructure` (cached instead of `imap.body`), `mime.parts`, `body.snippet`, `pop3.uidl`, `pop3.order`, `binary.parts`, and individual headers as `hdr.from`, `hdr.subject` and similar. The IMAP ENVELOPE needs `hdr.date`, `hdr.subject`, `hdr.from`, `hdr.sender`, `hdr.reply-to`, `hdr.to`, `hdr.cc`, `hdr.bcc`, `hdr.in-reply-to`, `hdr.message-id`.

Three client types exist: those downloading all metadata locally (no benefit from the cache afterward), those that download partially and search server-side (such as iOS Mail), and those with little or no local cache (webmail), which gain most. Since clients do not advertise this, Dovecot infers it dynamically, so seed the cache for the webmail you expect.

## Checked

2026-11-03. Confirmed on the Mail Cache Configuration page: per-folder dovecot.index.cache, the roles of mail_cache_fields, mail_always_cache_fields and mail_never_cache_fields (imap.envelope), INBOX decisions copied to new folders, the field names and descriptions (flags, date.sent, date.received, size.physical, imap.bodystructure versus imap.body, mime.parts, body.snippet, pop3.uidl, pop3.order, binary.parts, hdr.*), the IMAP ENVELOPE header list, and the three client types with Dovecot inferring behaviour dynamically. Nothing removed.

Method: documentation only; no commands were run.

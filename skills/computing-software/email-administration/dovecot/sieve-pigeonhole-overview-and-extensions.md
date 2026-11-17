---
id: computing-software.email-administration.dovecot.sieve-pigeonhole-overview-and-extensions
name: sieve-pigeonhole-overview-and-extensions
category: computing-software
field: email-administration
product: dovecot
tags: [sieve, pigeonhole, sieve-extensions, fileinto, vacation, sieve-interpreter]
level: practitioner
status: docs-checked
description: "Understand Pigeonhole Sieve for LDA and LMTP, which extensions are enabled by default, and which need plugins or explicit enabling."
sources:
  - https://doc.dovecot.org/main/core/config/sieve/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sieve support comes from Pigeonhole, a plugin for the LDA and LMTP services. It implements a Sieve interpreter (RFC 5228) that runs a user-provided script to decide how incoming messages are handled, for example delivering to a specific folder. Standard Sieve cannot run external programs, but Dovecot adds limited non-standard extensions that can.

Enabled by default: body, copy, date, duplicate, encoded-character, enotify (mailto only), envelope, environment, extracttext, fileinto, foreverypart, ihave, imap4flags, include, index, mailbox, mime, regex, reject, relational, subaddress, vacation and variables.

Not enabled by default (set in the extension settings): editheader, extlists, mboxmetadata, servermetadata, spamtest, virustest, vacation-seconds, and the Dovecot-specific `vnd.dovecot.environment` and `vnd.dovecot.report` (MARF reports).

Provided by separate plugins:
- imapsieve, via the imap-sieve plugin (runs at IMAP events).
- `vnd.dovecot.execute`, `vnd.dovecot.filter` and `vnd.dovecot.pipe`, through the sieve-extprograms plugin, which run pre-defined external programs.

Obsolete extensions have been removed. Choose extensions deliberately: editheader and external programs widen what a user script can do, so enable them only where users are trusted or sandboxed. Details for enotify, vacation, duplicate, variables, extlists and others are on their own pages.

## Checked

2026-11-03. Confirmed on the Sieve overview page: Pigeonhole as a plugin for LDA and LMTP, RFC 5228, the non-standard external-program extensions, the full default-enabled extension table, the not-enabled list (editheader, extlists, mboxmetadata, servermetadata, spamtest, virustest, vacation-seconds, vnd.dovecot.environment, vnd.dovecot.report), imapsieve via the imap-sieve plugin, vnd.dovecot.execute/filter/pipe via sieve-extprograms, and the removal of the obsolete imapflags and notify extensions (2.4.0). Nothing removed.

Method: documentation only; no commands were run.

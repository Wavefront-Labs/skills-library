---
id: computing-software.email-administration.dovecot.lda-dovecot-lda-delivery-setup
name: lda-dovecot-lda-delivery-setup
category: computing-software
field: email-administration
product: dovecot
tags: [dovecot-lda, lda, auth-userdb-socket, mailbox-indexing, forward-file, mda]
level: practitioner
status: docs-checked
description: "Run dovecot-lda as an MDA: the userdb socket, destination username, system user .forward usage, UID rules, logging and Postfix size limits."
sources:
  - https://doc.dovecot.org/main/core/config/delivery/lda.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The LDA (dovecot-lda) is an MDA that takes mail from an MTA and delivers it into a mailbox while keeping index files up to date. Most installs should use the LMTP server instead, which is easier to configure (especially permissions) and faster. LDA advantages are index update on delivery and quota enforcement through the quota plugin.

Config must be world readable for the unprivileged LDA; keep password settings in a separate `!include_try` file, which LDA skips.

For a few system users, call `dovecot-lda` in each user's `~/.forward`; it runs as that user and needs no auth socket. Otherwise pass the destination username with `-d`, for example `dovecot-lda -f $FROM_ENVELOPE -d $DEST_USERNAME`, and set up an auth-userdb socket via `auth_socket_path` so it can find the user's UID, GID and home. If you already know the home, run it without the socket, but verify the user exists first, or mail goes to nonexistent users.

Rules and traps:
- You must be running as the right UID before the call. LDA cannot run as root without `-d`.
- Several UIDs plus an MTA that will not run LDA as root: use LMTP. Do not make the binary setuid-root or run it via sudo.
- With the prefetch passdb, `-d` fails because no password query is made.
- LDA does not log through the root log process, so logging needs special configuration; if it cannot write its log it exits with a temporary failure.
- Postfix `mailbox_size_limit` covers every file written, logs included.

## Checked

2026-11-03. Confirmed on the Dovecot LDA page: LMTP preferred as easier and faster, indexing at delivery and quota plugin, world-readable config with !include_try, ~/.forward use for system users without the auth socket, -d with an auth-userdb socket via auth_socket_path, running without lookup using HOME and verifying the user, the root restriction, the multiple-UID advice (LMTP; no setuid-root or sudo), the prefetch passdb problem, logging through its own process and temporary failure on log write errors, and the Postfix mailbox_size_limit note. Nothing removed.

Method: documentation only; no commands were run.

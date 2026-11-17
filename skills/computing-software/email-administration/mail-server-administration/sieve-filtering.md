---
id: computing-software.email-administration.mail-server-administration.sieve-filtering
name: sieve-filtering
category: computing-software
field: email-administration
product: mail-server-administration
tags: [sieve-filtering, sieve, fileinto, sievec]
level: practitioner
status: docs-checked
description: "Enable the Dovecot Sieve plugin for per-user filters: fileinto, vacation, spam routing, and compile with sievec."
sources:
  - https://doc.dovecot.org/2.3/configuration_manual/sieve/configuration/
  - https://doc.dovecot.org/2.3/configuration_manual/sieve/examples/
  - https://doc.dovecot.org/2.3/configuration_manual/sieve/usage/
  - https://doc.dovecot.org/2.3/configuration_manual/sieve/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sieve filtering

**Goal:** server-side mail rules.
## Steps
1. `protocol lmtp { mail_plugins = $mail_plugins sieve }` (and the same in `protocol lda` if you deliver with the LDA).
2. Per-user scripts: the default `sieve = file:~/sieve;active=~/.dovecot.sieve` puts scripts in `~/sieve` with the active one at `~/.dovecot.sieve`; global rules run via `sieve_before` and `sieve_after`.
3. Example: `require "fileinto"; if header :contains "X-Spam-Flag" "YES" { fileinto "Junk"; }` (SpamAssassin header form from the docs examples).
4. Compile test: `sievec file.sieve`; pre-compile global scripts with `sievec` so they are not recompiled for every message.
## Failure modes
- A script that cannot be compiled or run logs an error; the user log defaults to `~/.dovecot.sieve.log` for a file-based script.
- Missing Junk folder: use `fileinto :create "Junk"`, which needs `require ["fileinto", "mailbox"]` (the mailbox extension, RFC 5490).
## Verify
- Deliver a message with the matching header and check the destination folder.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 Sieve pages: configuration (plugin in lda and lmtp, `sieve` default location, `sieve_before`, `sievec` precompile, user log), examples (X-Spam-Flag rule, `fileinto :create` via the mailbox extension) and troubleshooting (errors are logged). Fixed: the script path `~/sieve/.dovecot.sieve` (the active script is `~/.dovecot.sieve`) and the invented X-Spam header. Removed the claim that failed scripts deliver to INBOX.

Method: documentation only; no commands were run.

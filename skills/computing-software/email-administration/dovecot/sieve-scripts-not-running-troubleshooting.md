---
id: computing-software.email-administration.dovecot.sieve-scripts-not-running-troubleshooting
name: sieve-scripts-not-running-troubleshooting
category: computing-software
field: email-administration
product: dovecot
tags: [sieve-troubleshooting, log-debug, mail-plugins, utf-7-mailbox, lda-lmtp-check, sieve-plugin]
level: practitioner
status: docs-checked
description: "Diagnose Sieve scripts that never run: MTA not using LDA or LMTP, sieve missing from mail_plugins, compile errors and UTF-8 versus UTF-7 folder names."
sources:
  - https://doc.dovecot.org/main/core/config/sieve/troubleshooting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sieve runs only inside the Dovecot LDA and LMTP services. Typical causes when scripts are ignored:

1. The MTA is not using Dovecot for local delivery. Most MTAs have their own local delivery agent, and without explicit configuration that is what runs, so Sieve is skipped. Set `log_debug = category=sieve` and check the logs. A working LDA delivery logs that the sieve plugin module (`lib90_sieve_plugin.so`) loaded, followed by the effective uid, gid and home and the INBOX namespace line. LMTP logs similar lines. If you see none, the MTA is probably not calling Dovecot; running `dovecot-lda` manually verifies that Dovecot itself works.

2. The plugin is not enabled. Sieve is a plugin added to `mail_plugins` in the `protocol lda` block for LDA and the `protocol lmtp` block for LMTP. Without that, scripts are ignored. Check without delivering anything: `doveconf -f service=lda mail_plugins` should include sieve.

3. Misconfiguration or script errors. A script that fails to compile always logs an error.

4. Non-ASCII folder names. Sieve expects UTF-8 mailbox names and converts them to Dovecot's internal form. If an author writes the name in modified UTF-7 as IMAP uses, the `&` is escaped to `&-`, and delivery fails with an error like Mailbox doesn't exist for a name containing `&APY-` where the UTF-8 character should have been (for example, an o with umlaut). Fix the script to use UTF-8. The old CMUSieve plugin used UTF-7 folder names, so this often appears after migrating from CMUSieve to Pigeonhole.

## Checked

2026-11-08. Read the Sieve Troubleshooting page in full. Softened the MTA conclusion as the page does, and added the manual dovecot-lda check and the CMUSieve migration note.

Method: documentation only; no commands were run.

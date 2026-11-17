---
id: computing-software.email-administration.dovecot.spam-reporting-with-imap-sieve-spam-folder
name: spam-reporting-with-imap-sieve-spam-folder
category: computing-software
field: email-administration
product: dovecot
tags: [spam-reporting, imap-sieve, junk-special-use, sieve-pipe-bin-dir, sa-learn, report-extension]
level: advanced
status: docs-checked
description: "Report spam and ham when users move mail in or out of the Spam folder using imap-sieve, the report extension and piped learn scripts."
sources:
  - https://doc.dovecot.org/main/core/config/spam_reporting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The recommended design makes spam or ham reporting a user action: moving a message into or out of a defined Spam mailbox. The imap-sieve plugin catches these moves with a global script. The Spam mailbox is advertised through the `\Junk` special-use flag.

Two modes:
- External report: the script uses the `report` extension (RFC 5965 format) to send the message to a reporting address, for example `report "abuse" "User added this message to the Spam folder." "spam-report@example.com"`. A `not-spam` report is sent when a message leaves Spam; the ham script uses `environment "imap.mailbox"` to `stop` when the target is Trash (putting spam in Trash is not significant) or Spam (copying inside Spam). Sending to an external server also needs `submission_host` (the page uses `127.0.0.1:587`), `vnd.dovecot.report` in `sieve_global_extensions` and `sieve_imapsieve` in `sieve_plugins`.
- Local classification: the script pipes the message to local binaries, such as a learner.

Pitfalls:
- Scripts can only run from `sieve_pipe_bin_dir`. You cannot call /usr/local/bin/my-script.sh; put it in that directory and refer to the bare name.
- imap-sieve applies only to IMAP, not LDA or LMTP. Use normal Sieve there.
- Learning per message slows large moves; consider piping into a FIFO or using a socket-based worker.
- With SpamAssassin through Amavis and virtual users, use a MySQL or PostgreSQL backend for SpamAssassin to avoid permission and lock-file trouble. The `-u` parameter to the learner and related sieve variables then become obsolete.
- Reloading Dovecot does not activate changes in this configuration; do a full restart.
- The INBOX name is case-sensitive.
- To debug a script, import the `vnd.dovecot.debug` extension and use `debug_log "something"`.

## Checked
2026-11-09. Read the whole Dovecot "Spam Reporting" page (doc.dovecot.org/main/core/config/spam_reporting.html) and confirmed each statement above. Corrected the Trash/Spam handling description; added the submission_host requirement, case-sensitivity note and debugging hint from the page. The page says the spamc scripts are untested; none are reproduced here.

Method: documentation only; no commands were run.

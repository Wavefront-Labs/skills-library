---
id: computing-software.email-administration.dovecot.lmtp-server-delivery-configuration
name: lmtp-server-delivery-configuration
category: computing-software
field: email-administration
product: dovecot
tags: [lmtp, lmtp-proxy, lmtp-rcpt-check-quota, recipient-delimiter, mail-delivery, listener]
level: practitioner
status: docs-checked
description: "Configure the Dovecot LMTP server: listeners, privileges, proxying, quota checks at RCPT TO, logging and address extension variables."
sources:
  - https://doc.dovecot.org/main/core/config/delivery/lmtp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
LMTP (RFC 2033) is a network delivery service. Unlike the LDA, a short-lived binary started from a command line, LMTP is a long-running process started by the master process. It is the recommended delivery method for most installations.

General settings it shares with LDA: `postmaster_address` (the From of bounces), `hostname` (Message-IDs and Reporting-UA), `sendmail_path` (default /usr/sbin/sendmail, which may differ from /usr/lib/sendmail) or `submission_host` to send through an SMTP server.

Addresses map differently from LDA parameters: `-r` is the final envelope recipient, `-a` is the original recipient (can be overridden by `lda_original_recipient_header`), and `-d` is the destination username, which is the RCPT TO with the `+extension` stripped when `recipient_delimiter` is enabled. If usernames differ from addresses, the userdb must translate.

Listening: add `lmtp` to `protocols`, otherwise listeners are ignored. By convention TCP port 24 is used. A UNIX listener at `$base_dir/lmtp` is on by default when `lmtp` is in `protocols`.

Privileges: the LMTP process runs as root and drops privileges per user, so it can deliver to users with different UIDs. With one global UID/GID (virtual users) you can run it as that user for better security.

Other points:
- Proxying to remote LMTP or SMTP servers needs `lmtp_proxy = yes`, which makes it do passdb lookups.
- For busy sites, 5 to 20 listener processes is usually fine.
- `lmtp_rcpt_check_quota = yes` checks quota at RCPT TO, but not for proxied connections.
- Most plugins, including quota and Sieve, work with LMTP.
- Address extensions need `lmtp_save_to_detail_mailbox = yes` and `recipient_delimiter = +`.

## Checked

2026-11-03. Confirmed on the LMTP Server page: RFC 2033 and long-running versus LDA, recommended for most installs, postmaster_address, hostname, sendmail_path default and submission_host, the -r/-a/-d envelope mapping, protocols must include lmtp, port 24 convention, default UNIX listener at $base_dir/lmtp, root with privilege dropping and a single-UID option, lmtp_proxy = yes, 5 to 20 listener processes (process_min_avail), lmtp_rcpt_check_quota not applying to proxied connections, plugin support. Added the address extension variables from the page.

Method: documentation only; no commands were run.

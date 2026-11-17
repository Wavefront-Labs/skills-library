---
id: computing-software.email-administration.dovecot.rawlog-protocol-traffic-capture
name: rawlog-protocol-traffic-capture
category: computing-software
field: email-administration
product: dovecot
tags: [rawlog, rawlog-dir, login-proxy-rawlog-dir, lmtp-rawlog-dir, script-login, protocol-debug]
level: advanced
status: docs-checked
description: "Capture IMAP, POP3, LMTP and submission traffic with the rawlog settings, pre-login -R, and the legacy rawlog binary and its home directory needs."
sources:
  - https://doc.dovecot.org/main/core/admin/rawlog.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot can log protocol traffic for IMAP, POP3, LMTP and submission. Options:
- Pre-login: run the login service with `-R rawlogs`, for example `executable = imap-login -R rawlogs`. It writes under `$base_dir/login/rawlogs`, which you must create with enough write permission. LMTP and doveadm have no pre-login process.
- Proxying in login processes: `login_proxy_rawlog_dir`.
- LMTP: `lmtp_rawlog_dir` and `lmtp_proxy_rawlog_dir`.
- Submission: `rawlog_dir` and `submission_relay_rawlog_dir`.
- Legacy `rawlog` binary as a post-login script.

For the pre-login rawlog, SSL/TLS sessions are currently not decrypted to rawlogs. The page's example creates the directory with `mkdir`, `chown dovenull` and `chmod 0700` on `/var/run/dovecot/login/rawlogs`.

The legacy binary is run from post-login scripting: set `executable = imap postlogin` (and `pop3 postlogin`) in the service blocks and define `service postlogin { executable = script-login -d rawlog  unix_listener postlogin { } }`. It looks for a `dovecot.rawlog/` directory in the logged-in user's home and writes `yyyymmdd-HHMMSS-pid.in` and `.out` files, one pair per connection. Users without that directory are skipped, with minimal performance impact. The userdb must return a home directory; `mail_home` does not work (a userdb field such as `home = /home/%{user}` can supply one). Verify with `doveadm user -u user@example.com`; the `dovecot.rawlog/` directory must be writable by the uid it shows. To get an info message explaining why rawlog did nothing, set `DEBUG = 1` in `import_environment`.

Rawlog options: `-b` writes packet boundaries between `<<<` and `>>>`, `-t` adds microsecond timestamps, `-I` puts the IP in the filename, `-f in` or `-f out` logs one direction only. The binary is the legacy method; `rawlog_dir` is preferred nowadays.

## Checked
2026-11-09. Read the whole Dovecot Rawlog page (doc.dovecot.org/main/core/admin/rawlog.html; the old main/admin/rawlog.html URL is a script shell with no text, so the source was replaced). Confirmed the settings list, `-R rawlogs` and `$base_dir/login/rawlogs`, the legacy binary behaviour, home directory rules and options. Removed the unsupported advice about the sensitivity of captured traffic and deleting it, and scoped the TLS statement to the pre-login rawlog as the page states it.

Method: documentation only; no commands were run.

---
id: computing-software.email-administration.dovecot.logging-destinations-and-syslog-setup
name: logging-destinations-and-syslog-setup
category: computing-software
field: email-administration
product: dovecot
tags: [logging, syslog-facility, log-path, doveadm-log, logrotate, rsyslog-flood-control]
level: practitioner
status: docs-checked
description: "Find Dovecot logs, split errors from info with syslog_facility or log_path settings, avoid rsyslog rate limits and rotate logs safely."
sources:
  - https://doc.dovecot.org/main/core/admin/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot always logs a detailed error when something goes wrong; usually the problem is looking in the wrong file, since errors can land in a different file from informational messages. By default it uses syslog with the mail facility. `doveadm log find` shows where logs go, and `doveadm log errors` prints the last 1000 error messages of the running server.

To log to files directly, set `log_path` (warnings and errors), `info_log_path` and `debug_log_path`. Alternatively change `syslog_facility`. With syslog there are levels such as warning and crit (fatal, process dies), and where each lands depends on your syslog rules; often everything goes to mail.log or maillog, with err and crit in mail.err.

Better practice: set `syslog_facility = local5` and send all local5 messages to dovecot.log and the important warning and error ones to dovecot-errors.log. If syslog also copies info to /var/log/messages, add `;local5.none` to that rule to stop duplicates.

rsyslog flood control is on by default and drops messages when Dovecot logs a lot, particularly with debug logging, so disable rate limiting in /etc/rsyslog.conf.

Use logrotate with a script in /etc/logrotate.d/dovecot. Under SELinux, doveadm may fail to read config from the logrotate context, so use the alternative postrotate that sends signal 0 and then USR1 to the PID in master.pid.

Clients see only "Internal error occurred. Refer to server log for more information." with a timestamp, so Dovecot does not leak details; use the timestamp to find the real error in the error log.

Verbosity settings, all disabled by default: `auth_verbose = yes` logs failed authentication attempts; `log_debug = category=auth` enables all auth debug logging (also enables `auth_verbose`; passwords shown as `<hidden>`); `auth_debug_passwords = yes` removes the hiding (not with PAM); `log_debug = category=mail` logs mail-related debugging; `verbose_ssl = category=ssl` logs SSL errors and warnings; `auth_verbose_passwords = no|plain|sha1` logs the password used on a failed login, and `sha1` logs only its SHA1.

## Checked
2026-11-09. Read the whole Dovecot Logging page (doc.dovecot.org/main/core/admin/logging.html; the old main/admin/ URL is a script shell with no text, so the source was replaced) and confirmed every statement, including the rsyslog flood-control note, the logrotate postrotate variants and the 1000-error limit.

Method: documentation only; no commands were run.

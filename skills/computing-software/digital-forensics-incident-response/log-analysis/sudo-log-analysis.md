---
id: computing-software.digital-forensics-incident-response.log-analysis.sudo-log-analysis
name: sudo-log-analysis
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sudo-logs, linux-logs, authentication-log, privilege-escalation, dfir]
level: practitioner
status: docs-checked
description: "Reconstruct privileged activity from sudo logs: entry format, denied entries, logfile and syslog settings, I/O logs and sudoreplay, and gaps when logging is disabled."
sources: ["https://www.sudo.ws/docs/man/sudoers.man/", "https://www.sudo.ws/docs/man/sudoreplay.man/", "https://man7.org/linux/man-pages/man1/journalctl.1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sudo log analysis

**Goal:** show which user ran which command as root (or another user), when, and from which
terminal - and spot attempts and abuse.

## Where sudo logs
- By default sudoers logs to syslog (facility `auth` unless the `syslog` setting changes it);
  the `logfile` setting adds a separate sudo log file, and negating either option turns that destination off.
- Accepted command entries follow this template:
  `date hostname progname: username : TTY=ttyname ; CHROOT=chroot ; PWD=cwd ; USER=runasuser ; GROUP=runasgroup ; TSID=logid ; ENV=env_vars COMMAND=command`
  TTY is the short terminal name (e.g. `pts/0`, or `unknown` when none); PWD is the directory sudo was run in;
  USER is the user the command ran as; COMMAND includes arguments.
- Denied entries: `user NOT in sudoers` and `3 incorrect password attempts` (the count varies with
  the `passwd_tries` option).
- **I/O logging**: `log_input` and `log_output` are off by default; when enabled sudo runs the command
  in a pseudo-terminal and records input/output under `iolog_dir` (default `/var/log/sudo-io`).
  `sudoreplay -l` lists sessions (optionally filtered by user, command, tty, host, runas user or date range);
  `sudoreplay <session-id>` replays one (IDs are normally six characters such as `0100A5`).
- Which syslog file receives the `auth` facility depends on the host's syslog configuration (not covered by the cited pages); on systemd hosts journalctl can read it.

## Queries
```bash
journalctl _COMM=sudo --since "2026-10-01" -o short-iso
zgrep -h "COMMAND=" /var/log/auth.log*
zgrep -h "incorrect password\|NOT in sudoers" /var/log/auth.log*
sudoreplay -l ; sudoreplay <session-id>          # if I/O logging enabled
```
`--since` and `-o short-iso` (RFC 3339 timestamps) are documented in journalctl; the page documents
FIELD=VALUE matches generally but does not show `_COMM=` as an example. The auth.log path is Debian-style; adjust per host.

## What to look for
- Interactive root shells (`sudo -i`, `sudo su -`, `sudo bash`): sudo logs the launch, not what is done inside, unless I/O logging is on.
- Commands editing `sudoers`, `passwd`, `shadow`, SSH keys, cron, systemd units.
- Logging switched off: a `Defaults !syslog` (syslog negated) without a `logfile` leaves no sudo log; check sudoers and sudoers.d timestamps.

## Gotchas
- Log rotation compresses older files; include `.gz` (hence `zgrep`).
- The ignore_logfile_errors flag only matters when file-based logging via `logfile` is configured.

## Verify
Every privileged action in the incident is tied to a user, TTY/source and time from sudo and session logs.

## Checked
Method: 2026-11-08 docs-only read of the sudoers, sudoreplay and journalctl manual pages; log entry template, denied entries, logging settings, iolog_dir and sudoreplay claims confirmed. Dropped as unsupported by the pages: pam_unix session lines, Baron Samedit/GTFOBins notes, root history advice. Hedged: the `_COMM=` match and the claim that `!syslog` tampering is visible.

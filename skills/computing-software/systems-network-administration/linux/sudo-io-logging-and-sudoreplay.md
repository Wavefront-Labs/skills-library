---
id: computing-software.systems-network-administration.linux.sudo-io-logging-and-sudoreplay
name: sudo-io-logging-and-sudoreplay
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sudo, sudo-logging, sudo-io-log, sudoreplay, log-output, logfile, sudo-logsrvd, audit-trail, timestamp-timeout, sudo-timeout, sysadmin]
level: practitioner
status: docs-checked
description: "Audit privileged sessions: sudo logging to syslog/file, full I/O session recording with log_input/log_output and sudoreplay, sudo_logsrvd, and credential timeouts."
sources:
  - https://github.com/sudo-project/sudo/blob/main/docs/sudoers.mdoc.in
  - https://github.com/sudo-project/sudo/blob/main/docs/sudoreplay.mdoc.in
  - https://github.com/sudo-project/sudo/blob/main/docs/sudo_logsrvd.conf.mdoc.in
  - https://github.com/sudo-project/sudo/blob/main/docs/sudo.mdoc.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sudo logging, I/O recording and timeouts

**Goal:** know who ran what as root, be able to replay what they saw/typed in a root shell,
and control how long sudo trusts a password.

## 1. Basic command logging
Every sudo command is logged through syslog by default (the `syslog` and `logfile` settings control where
events go; syslog, a file or both). Add a dedicated file:
```sudoers
Defaults logfile=/var/log/sudo.log
Defaults log_year, log_host
```

## 2. Session I/O recording
```sudoers
Defaults log_output                     # record terminal output (what they saw)
Defaults log_input                      # record keystrokes (captures passwords typed into programs!)
Defaults iolog_dir=/var/log/sudo-io/%{user}   # %{seq} (base 36 sequence) is appended per session by default
Defaults!/usr/bin/sudoreplay !log_output
Defaults:backup !log_output             # skip noisy automation
```
Or per rule with tags: `WEBOPS ALL = (root) LOG_OUTPUT: /bin/bash`.
```bash
sudoreplay -l                           # list sessions (TSID, user, command, time)
sudoreplay -l user alice command bash
sudoreplay 0100A5                       # replay by session ID (TSID); keys: space pauses, < halves and > doubles speed
sudoreplay -s 5 0100A5                  # speed factor 5
```
`log_input` stores everything typed, including secrets — restrict access to the I/O log dir and
consider output-only. `maxseq` caps the session sequence number substituted for `%{seq}`; plan expiry of old
session directories separately.

## 3. Central logging
`sudo_logsrvd` (sudo 1.9 and later) receives event and I/O logs from many hosts. Server addresses take the form
`host[:port][(tls)]`; the default port is 30343 for plaintext and 30344 for TLS, and TLS is used only when the
`(tls)` flag is given:
```sudoers
Defaults log_servers=logsrv.example.com:30344(tls)
Defaults log_server_cabundle=/path/to/ca-bundle.pem
```
`ignore_iolog_errors` lets commands run even when the I/O log (local or remote) cannot be written; leave it off
if you need a command to be refused when it cannot be recorded.
Alternatively forward syslog and use `auditd` execve rules to catch commands run inside root shells.

## 4. Credential caching (timestamp_timeout)
```sudoers
Defaults timestamp_timeout=5            # minutes a successful auth is cached (build-time default, 5 upstream; 0 = always ask; negative = until reboot)
Defaults timestamp_type=tty             # per terminal (default); global = shared across the user's sessions
Defaults passwd_tries=3                 # build-time default, 3 upstream
```
`sudo -k` invalidates the cached credential for the current terminal, `sudo -K` removes every cached credential
of the user; `sudo -v` refreshes the timestamp.
Short timeouts reduce the window for malware riding an admin's terminal.

## Gotchas
- `sudo -i`/`sudo su -` sessions: plain logging records only the shell start, not the commands — that's why I/O logs or auditd matter.
- I/O logs on the same host can be deleted by the root user you're auditing — ship them off-host.
- `log_output` on commands producing huge output (backups) fills disks.

## Verify
- [ ] `sudoreplay -l` lists a test `sudo -i` session; replay shows the commands.
- [ ] The syslog or logfile entry for a sudo command shows the user, TTY, working directory, target user and command.
- [ ] `sudo -l` after timeout prompts again as configured.

## Checked
Checked 2026-10-25 against the sudo-project/sudo manual sources (docs/ directory, main branch) and configure.ac.
Confirmed: `logfile`, `log_year`, `log_host`, `log_input`/`log_output`, `LOG_OUTPUT` tag, `iolog_dir` and `%{seq}`, `maxseq`, sudoreplay list syntax and keys, `-s` speed factor, `log_servers` syntax with default ports 30343/30344 and the `(tls)` flag, `log_server_cabundle`, `ignore_iolog_errors`, `timestamp_timeout` semantics and build defaults (timeout 5, passwd_tries 3), `-k`/`-K`/`-v`.
Corrected: `ignore_log_errors` is not a sudoers setting (`ignore_iolog_errors` and `ignore_logfile_errors` are); a TLS connection needs the `(tls)` flag; sudoreplay IDs are six-character IDs. Removed as unconfirmed: journalctl field search, log file paths, the auditd rule and the distribution log locations.

Method: documentation only; no commands were run.

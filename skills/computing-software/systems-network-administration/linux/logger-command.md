---
id: computing-software.systems-network-administration.linux.logger-command
name: logger-command
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, logger, syslog, util-linux, journald, systemd-cat, shell-logging, remote-syslog-test, structured-data, logging, bash, sysadmin]
level: intro
status: docs-checked
description: "Send messages to syslog/journald from shell scripts with logger: tags, facility.priority, PID, journal fields, remote UDP/TCP test messages, and systemd-cat."
sources:
  - https://github.com/util-linux/util-linux/blob/master/misc-utils/logger.1.adoc
  - https://github.com/systemd/systemd/blob/main/man/systemd-cat.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logger — syslog from the shell

**Goal:** scripts and cron jobs leave searchable, correctly-tagged log lines, and you can
inject test messages to prove a logging path works.

## 1. Basics
```bash
logger "backup finished"                               # default priority user.notice; default tag is the logged-in user name
logger -t backup -p local0.info "backup finished in ${SECONDS}s"
logger -t backup -p local0.err --id=$$ "backup FAILED: rsync exit $rc"   # --id adds the PID
journalctl -t backup --since today                      # find by tag (SYSLOG_IDENTIFIER)
```
Always set `-t` (searchable identifier) and a meaningful priority — alerts usually key on `err` and above.

## 2. In scripts
```bash
log() { logger -t "${0##*/}" -p "local0.${2:-info}" -- "$1"; }
log "starting"; log "disk almost full" warning
some_command 2>&1 | logger -t myjob -p local0.info      # every output line becomes a message
logger -t myjob -f /var/tmp/report.txt                   # log a file's lines
```
`--` protects messages starting with `-`.
With journald, `systemd-cat` keeps stdout/stderr priorities separate:
`systemd-cat -t myjob -p info --stderr-priority=err ./job.sh`.

## 3. Journal fields (journald hosts)
```bash
logger --journald <<EOF
MESSAGE=deploy complete
SYSLOG_IDENTIFIER=deploy
PRIORITY=6
RELEASE=2026.10.16
EOF
journalctl SYSLOG_IDENTIFIER=deploy -o verbose | grep RELEASE
```
`--journald` ignores other logger options such as priority; put `PRIORITY=` in the input. Each line must start with a field journald accepts.

## 4. Remote test messages
```bash
logger -n logs.corp.example -P 514 -d -t nettest "udp test"   # -d UDP
logger -n logs.corp.example -P 514 -T -t nettest "tcp test"   # -T TCP
logger --rfc5424 -n logs.corp.example -T "with full timestamp"
```
These go to the remote server instead of the local log socket — good for testing the collector and firewall directly. Without `-d` or `-T`, logger tries UDP first.

## Gotchas
- logger's default message size limit is 1 KiB (RFC 3164 tradition); `--size` changes it, and the limit includes the syslog header.
- A facility such as `local0` only lands in a dedicated file if your syslog daemon is configured to route it.

## Verify
- [ ] `journalctl -t <tag> -p err` (or the rsyslog target file) shows the message with the right priority.
- [ ] A remote `logger -n` test appears on the collector.

## Checked

2026-10-26. util-linux master (last commit 2026-10-26) logger(1): default priority user.notice, default tag, -t, -p, --id, -f, --, -n/-P/-d/-T, --rfc5424, --journald semantics, --size default 1 KiB; systemd-cat(1): -t, -p, --stderr-priority. Removed the util-linux 2.30 version claim, the older-daemon truncation remark, the rsyslog routing details and the container remark, which were not confirmed. journalctl(1): -t/--identifier=SYSLOG_IDENTIFIER.

Method: documentation only; no commands were run.

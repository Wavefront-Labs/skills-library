---
id: computing-software.networking-hardware-and-wireless.apache-httpd.log-rotation-and-piped-logs
name: log-rotation-and-piped-logs
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, logging, rotatelogs, piped-logs, logrotate, graceful, log-rotation]
level: practitioner
status: docs-checked
description: "Rotate httpd logs with rotatelogs piped logs or logrotate plus graceful restart: intervals, sizes, strftime names, rotatelogs options and security cautions."
sources:
  - https://httpd.apache.org/docs/2.4/programs/rotatelogs.html
  - https://httpd.apache.org/docs/2.4/logs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log rotation and piped logs
## rotatelogs
```apache
CustomLog "|bin/rotatelogs /var/log/logfile 86400" common
CustomLog "|bin/rotatelogs -l /var/log/logfile.%Y.%m.%d 86400" common
CustomLog "|bin/rotatelogs /var/log/logfile 5M" common
ErrorLog "|bin/rotatelogs /var/log/errorlog.%Y-%m-%d-%H_%M_%S 5M"
```
A name with `%` is a strftime pattern. Use enough granularity: `errorlog.%Y-%m-%d` with size rotation can overwrite the same file.

## Options
`-l` local time; `-L linkname` hard link to current log; `-p program` run on each new file (`$1` new, `$2` old); `-f` open at start; `-D` create directories; `-t` truncate instead of rotate (`-T` from 2.4.56); `-v`; `-e` echo to stdout; `-c` create a file per interval; `-n number` circular names (2.4.5+).

## logrotate
After moving files aside, signal a graceful restart so httpd reopens logs:
```
apachectl graceful
```
Or the equivalent `systemctl reload`. Old logs close late, so scripts need a delay.

## Piped logs
`|command` runs without a shell; `|$command` uses `/bin/sh -c`. httpd restarts a crashed pipe. Piped processes inherit the parent's user, usually root, so keep them simple and secure.

## Security
Write access to log directories can lead to the startup uid.

## Checked

2026-11-08. rotatelogs examples, options (-l, -L, -p, -f, -D, -t, -T from 2.4.56, -v, -e, -c, -n from 2.4.5), strftime granularity warning, logrotate with graceful restart, piped-log shell vs direct spawn, restart on crash, root inheritance and the log-directory write-access warning confirmed against the rotatelogs and logs pages.

Method: documentation only; no commands were run.

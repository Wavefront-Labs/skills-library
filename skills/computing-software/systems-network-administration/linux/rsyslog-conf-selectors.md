---
id: computing-software.systems-network-administration.linux.rsyslog-conf-selectors
name: rsyslog-conf-selectors
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rsyslog, rsyslog-conf, rsyslog-selectors, syslog-facility, syslog-priority, property-based-filter, rainerscript, rsyslog-d, logging, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Route messages with rsyslog.conf: facility.priority selectors and their operators, property and RainerScript filters, rsyslog.d drop-ins, stop/discard, and testing config before restart."
sources:
  - https://www.rsyslog.com/doc/configuration/filters.html
  - https://www.rsyslog.com/doc/configuration/sysklogd_format.html
  - https://www.rsyslog.com/doc/rainerscript/include.html
  - https://www.rsyslog.com/doc/configuration/properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rsyslog.conf selectors and filters

**Goal:** get each kind of message into the right file (and only there), using the
selector syntax every distro ships plus RainerScript where it's clearer.

## 1. Selector syntax: `facility.priority  action`
- Facilities: `auth`, `authpriv`, `cron`, `daemon`, `kern`, `mail`, `user`, `local0`–`local7`, `*`.
- Priorities (high→low): `emerg alert crit err warning notice info debug`, plus `none`.
- `mail.err` = err **and higher**; `mail.=err` = exactly err; `mail.!err` = below err; `mail.none` = nothing from mail.
- Combine: `*.info;mail.none;authpriv.none;cron.none  /var/log/messages` (`;` = multiple selectors on one line, `,` = several facilities: `mail,news.crit`).
- Actions: file path (`/path`), `@host` UDP, `@@host` TCP, `:omusrmsg:*` all users, `~`/`stop` discard.

## 2. Drop-ins and order
A distro `/etc/rsyslog.conf` normally pulls drop-ins in with `include(file="/etc/rsyslog.d/*.conf")`; wildcard matches are included in file-name sort order, and an include is pasted in at its position. Statements such as `stop` only affect rules that come after them, so a drop-in included **before** the default rules can keep messages out of the default log file (check where your distro's include sits):
```
# /etc/rsyslog.d/20-myapp.conf
if $programname == 'myapp' then {
    action(type="omfile" file="/var/log/myapp.log")
    stop
}
local3.*    /var/log/haproxy.log
& ~
```
`& action` applies an extra action to the previous line's selector (here `~` discards the message after the file write).

## 3. Property filters
```
:msg, contains, "DROP"            /var/log/firewall.log
:programname, isequal, "sshd"     /var/log/sshd.log
:hostname, startswith, "web"      /var/log/web-hosts.log
:msg, regex, "error [0-9]+"       /var/log/errors.log
```
Operators: `contains`, `isequal`, `startswith`, `regex`, `ereregex`; prefix `!` to negate.
RainerScript is better for anything compound: `if $syslogseverity <= 3 and $syslogfacility-text == 'daemon' then ...`.

## 4. Test and apply
```bash
rsyslogd -N1                          # validate config (level 1); exits non-zero on errors
systemctl restart rsyslog
logger -p local3.info -t haproxy "selector test"
tail -1 /var/log/haproxy.log
```

## Gotchas
- New log files need rotation: add a logrotate entry whose postrotate step sends rsyslogd a HUP (rsyslogd closes and reopens its files on HUP).
- On journald systems rsyslog gets messages via `imjournal`/`imuxsock`; `$programname` is the static part of the message tag (what `logger -t` sets), not always the binary name.
- Order matters: a catch-all `*.*` before your `stop` rule still logs the message there.

## Verify
- [ ] `rsyslogd -N1` clean; a `logger -p <facility>.<prio> -t <tag>` test lands only in the intended file.
- [ ] `/var/log/messages` no longer contains the messages you diverted with `stop`.

## Checked
Checked 2026-10-25 against the rsyslog documentation source on GitHub (rsyslog/rsyslog doc/source, main, release 8.2610.0 of 2026-10-20) and the systemd man pages. Confirmed: selector semantics (`=`, `!`, `none`, `,` and `;`, higher-priority-and-above rule) and the sysklogd restriction on excluding lower priorities; property filter operators `contains`, `isequal`, `startswith`, `regex`, `ereregex` and the `!` negation; `~` discard; `@`/`@@` forwarding; `include()` wildcard order and position sensitivity; `rsyslogd -N level` config check; HUP handling. Removed unconfirmed claims: the `-/path` no-sync prefix, SELinux label and the distro `rsyslog-rotate` helper.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.linux.rsyslog-imjournal-integration
name: rsyslog-imjournal-integration
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rsyslog, imjournal, journald-to-rsyslog, imuxsock, forwardtosyslog, journald, statefile, ratelimit, structured-fields, logging, sysadmin]
level: practitioner
status: docs-checked
description: "Connect journald and rsyslog correctly: imjournal vs imuxsock/ForwardToSyslog, state file and rate limits, journal fields in rsyslog, duplicate-avoidance, and choosing what stores what."
sources:
  - https://www.rsyslog.com/doc/configuration/modules/imjournal.html
  - https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html
  - https://www.rsyslog.com/doc/configuration/modules/imuxsock.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# journald → rsyslog integration (imjournal)

**Goal:** every message journald sees also reaches rsyslog (for files and forwarding)
exactly once, without loss under bursts or duplicates after restarts.

## 1. Two ways in
| Method | How |
|---|---|
| `imjournal` | rsyslog reads the journal through the journal API, with a cursor state file; needed only if you want structured journal data |
| `imuxsock` + journald `ForwardToSyslog=yes` | journald forwards to the `/run/systemd/journal/syslog` socket; the rsyslog docs recommend this when structured data is not needed and say it is faster |
Use **one**, not both: both together read the same messages twice. `ForwardToSyslog=` is off by default in journald.

## 2. imjournal settings
```
module(load="imjournal"
       StateFile="imjournal.state"     # in $WorkDirectory; remembers the cursor across restarts
       Ratelimit.Interval="600" Ratelimit.Burst="20000"
       IgnorePreviousMessages="off"    # "on" skips the backlog on first start
       FileCreateMode="0644")
module(load="imuxsock" SysSock.Use="off")   # avoid the second input path when imjournal is used
```
Rate limiting: imjournal's limiter is on by default and, per the module docs, permits 20,000 messages per 10 minutes (the values shown); messages over that are discarded, counted in the `ratelimit_discarded_in_interval` impstats field. Raise them or fix the chatty service. journald itself
rate-limits too (`RateLimitIntervalSec`, `RateLimitBurst` in `journald.conf`).

## 3. Journal fields in rsyslog
Structured journal data is available through `mmjsonparse` and the `%$!all-json%` property; the imjournal documentation's own example is:
```
module(load="imjournal" StateFile="imjournal.state")
module(load="mmjsonparse")
template(name="CEETemplate" type="string" string="%TIMESTAMP% %HOSTNAME% %syslogtag% @cee: %$!all-json%\n")
action(type="mmjsonparse")
action(type="omfile" file="/var/log/ceelog" template="CEETemplate")
```
The exact names of individual journal fields as rsyslog properties are not listed in the docs; inspect `%$!all-json%` output on your system before filtering on one.

## 4. Storage split (decide deliberately)
- journald volatile (`Storage=volatile`) + rsyslog files: classic text logs, journal only in RAM.
- journald persistent + rsyslog only forwarding: local queries via journalctl, central copy remote.
- Both persistent: double disk use; cap journald with `SystemMaxUse=`.

## Gotchas
- With no state file, imjournal reads the whole existing journal (a flood of old messages) unless `IgnorePreviousMessages="on"`, which starts at new entries only when no state file exists.
- A relative `StateFile` is created in the rsyslog working directory; an absolute path is used as is.
- `ForwardToSyslog=yes` on an imjournal host = duplicates; check `journald.conf` drop-ins.

## Verify
- [ ] `logger -t dup-test hello` appears exactly once in `/var/log/messages` (or syslog) and once in `journalctl -t dup-test`.
- [ ] `systemctl restart rsyslog` produces no replay of old messages; impstats shows no `ratelimit_discarded_in_interval` under normal load.

## Checked
Checked 2026-10-25 against the rsyslog documentation source on GitHub (rsyslog/rsyslog doc/source, main, release 8.2610.0 of 2026-10-20) and the systemd man pages. Confirmed: imjournal parameters `StateFile` (relative path under the work directory), `IgnorePreviousMessages` (boolean, default off, applies only when no state file exists), `Ratelimit.Interval`/`Ratelimit.Burst` (default 20,000 messages per 10 minutes), `FileCreateMode`, imuxsock `SysSock.Use` and the `/run/systemd/journal/syslog` socket, the `%$!all-json%` example, and from the systemd journald.conf man page `ForwardToSyslog=` (off by default), `RateLimitIntervalSec=`, `RateLimitBurst=`, `SystemMaxUse=`, `Storage=`. Removed unconfirmed claims: per-distro defaults, the exact rate-limit log message, individual `$!_SYSTEMD_UNIT`-style property names, and the vacuum and cursor behaviour.

Method: documentation only; no commands were run.

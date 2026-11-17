---
id: computing-software.systems-network-administration.linux.journald-rate-limiting
name: journald-rate-limiting
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, journald, journald-rate-limit, ratelimitburst, ratelimitintervalsec, logratelimitintervalsec, suppressed-messages]
level: practitioner
status: docs-checked
description: "Diagnose and tune journald rate limiting ('Suppressed N messages from unit'): RateLimitIntervalSec/Burst globally, LogRateLimit per unit, and fixing chatty services."
sources:
  - https://github.com/systemd/systemd/blob/main/man/journald.conf.xml
  - https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml
  - https://github.com/rsyslog/rsyslog-doc/blob/master/source/configuration/modules/imjournal.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# journald rate limiting

**Symptom:** journald logs a message that it dropped N messages from a service (journald's "Suppressed ... messages" line,
exact wording varies by version) — log lines from an incident are simply gone.

## Defaults
`RateLimitIntervalSec=30s`, `RateLimitBurst=10000` per service. The effective burst is multiplied by a factor
from the free journal disk space (base-2 logarithm: 1 at 1 MB or less up to 6 at 1 TB or less).
Messages above the burst within the interval are dropped, then a message reporting the number dropped is logged.

## Tune
Globally — `/etc/systemd/journald.conf.d/ratelimit.conf`:
```ini
[Journal]
RateLimitIntervalSec=30s
RateLimitBurst=50000
# setting either value to 0 turns rate limiting off (risky: a log storm can fill disk / eat CPU)
```
`systemctl restart systemd-journald`.

Per service (`LogRateLimit*` added in systemd 240; they override the journald.conf values) — `systemctl edit myapp`:
```ini
[Service]
LogRateLimitIntervalSec=10s
LogRateLimitBurst=20000
LogLevelMax=info          # drop debug at the source instead
```

## rsyslog has its own limits
If logs reach rsyslog via imjournal: `module(load="imjournal" Ratelimit.Interval="600" Ratelimit.Burst="20000")`
(both values are the defaults: 20,000 messages per 600 s; interval 0 turns it off);
imuxsock has `SysSock.RateLimit.Interval` / `.Burst` / `.Severity` (defaults 0, 200, 1). Messages may pass journald and be dropped in rsyslog.

## Better fixes
- Find the noisy unit from the journald line that reports the dropped messages, or by counting recent entries per unit.
- Lower app log level, or send debug to a file the app rotates itself. `LogRateLimit*` does not apply to output sent straight to a file with `StandardOutput=file:`.
- Make sure `SystemMaxUse=` can absorb bursts.

## Verify
- [ ] Generate a burst (`for i in $(seq 30000); do logger -t burst $i; done`) — no dropped-messages line for the tuned unit; journal size stays within limits.

## Checked

Checked 2026-10-26 against systemd/systemd main (last commit 2026-10-25) man/journald.conf.xml and man/systemd.exec.xml, and rsyslog-doc imjournal.rst and imuxsock.rst. Confirmed: RateLimitIntervalSec and RateLimitBurst defaults (30 s, 10000), the free-disk-space multiplier table, 0 disabling limiting, LogRateLimitIntervalSec/Burst (added in v240) overriding journald.conf and not applying to StandardOutput=file output, LogLevelMax, imjournal Ratelimit.Interval 600 and Ratelimit.Burst 20000 defaults, imuxsock SysSock.RateLimit defaults. Removed: the quoted Suppressed log line wording and the jq pipeline.

Method: documentation only; no commands were run.

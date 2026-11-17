---
id: computing-software.database-administration.yugabytedb.clock-synchronization-chrony-clockbound
name: clock-synchronization-chrony-clockbound
category: computing-software
field: database-administration
product: yugabytedb
tags: [clock-sync, chrony, max-clock-skew-usec, clockbound, ptp, time-source, hybrid-time]
level: advanced
status: docs-checked
description: "Configure clock sync for YugabyteDB with chrony, size max_clock_skew_usec, and use ClockBound or PTP on AWS and GCP to shrink skew and read restarts."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/checklist.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/manual-deployment/system-config.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clock synchronization

YugabyteDB uses hybrid time, so node clocks must agree. `--max_clock_skew_usec` defaults to 500000 (500 ms); set it to about twice the skew you expect. Clock drift is assumed bounded to 500 PPM.

Chrony is the preferred daemon. A sample configuration sets:
- `minpoll 4` and `maxpoll 4`
- `minsources 2`
- `maxdistance 0.1`
plus your cloud's time source. Verify with `chronyc tracking` and `chronyc sources`.

Chrony details from the system-config page:
- `minpoll 4 maxpoll 4` fixes polling at 16 seconds; this is required if you use ClockBound.
- `minsources` defaults to 1, which lets one source steer the clock; use at least 2.
- `maxdistance` defaults to 3 seconds, so it never rejects anything; keep it well below `--max_clock_skew_usec`.
- On a cloud use the provider's link-local time service; on premises configure several independent sources spread across zones, preferably ones that smear leap seconds.
- Clock error is root dispersion plus half of root delay plus system time from `chronyc tracking`. The update interval in `chronyc tracking` should match the configured 16 seconds.

Tighter options:
- **PTP** (AWS only): run `bin/configure_ptp.sh`.
- **ClockBound**: run `bin/configure_clockbound.sh`, then start the servers with `--time_source=clockbound` on AWS or GCP. When PTP is also in use, set `clockbound_clock_error_estimate_usec=100`.

## Checked

2026-11-04. Confirmed against the deployment checklist and the system configuration page: the two-times-expected-skew recommendation for --max_clock_skew_usec, the 500 PPM drift bound, the chrony settings and their defaults, the clock error formula, PTP being AWS only, ClockBound on AWS and GCP, time_source=clockbound and clockbound_clock_error_estimate_usec=100 with PTP. Removed the shutdown claim, the read-restart claim and the hybrid_clock_skew monitoring paragraph, which the pages do not state.

Method: documentation only; no commands were run.

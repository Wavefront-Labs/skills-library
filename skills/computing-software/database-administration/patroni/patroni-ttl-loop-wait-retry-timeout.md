---
id: computing-software.database-administration.patroni.patroni-ttl-loop-wait-retry-timeout
name: patroni-ttl-loop-wait-retry-timeout
category: computing-software
field: database-administration
product: patroni
tags: [patroni, ttl, loop-wait, retry-timeout, tuning]
level: practitioner
status: docs-checked
description: "The three timing parameters, their defaults and minimums, and the constraint they must satisfy."
sources:
  - https://patroni.readthedocs.io/en/latest/dynamic_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change failover timing without breaking the HA loop.

Dynamic configuration parameters (seconds):
- `loop_wait`: how long the HA loop sleeps. Default 10, minimum 1.
- `ttl`: TTL to acquire the leader lock; effectively the time before automatic failover begins. Default 30, minimum 20.
- `retry_timeout`: timeout for DCS and PostgreSQL operation retries. Default 10, minimum 3. DCS or network issues shorter than this do not cause the leader to be demoted.

When changing any of them you must follow:

```
loop_wait + 2 * retry_timeout <= ttl
```

Change them with `patronictl edit-config`, for example:

```
patronictl -c postgres0.yml edit-config batman --set loop_wait="15" --set ttl="45" --force
```

These options can be changed only dynamically (along with `maximum_lag_on_failover`, `max_timelines_history`, `check_timeline` and `postgresql.use_slots`). Patroni reads the section from the DCS and changes its run-time values.

FAQ definitions: `loop_wait` is the sleep before a new HA cycle; `retry_timeout` is how long a non-responsive DCS is tolerated before Patroni may demote the primary as a safety action; `ttl` is the lease on the leader lock, and when the leader cannot renew it for longer than `ttl` the lease expires and triggers a leader race.

Patroni writes the DCS options to `patroni.dynamic.json` in the data directory on every change; only the leader may restore them from that file if they are absent or invalid in the DCS.

## Checked

2026-11-03. Confirmed against Dynamic Configuration (loop_wait, ttl, retry_timeout defaults and minimums, the `loop_wait + 2 * retry_timeout <= ttl` rule), the patronictl edit-config example and the FAQ definitions; patroni.dynamic.json behaviour from the patroni_configuration page.

Method: documentation only; no commands were run.

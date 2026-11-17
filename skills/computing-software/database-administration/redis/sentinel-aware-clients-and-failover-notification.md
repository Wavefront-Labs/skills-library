---
id: computing-software.database-administration.redis.sentinel-aware-clients-and-failover-notification
name: sentinel-aware-clients-and-failover-notification
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, sentinel-clients, redis-sentinel, failover-notification, client-reconfiguration, redis-ha]
level: practitioner
status: docs-checked
description: "Connect applications to Redis through Sentinel so they find the current primary after failover, handle reconnection, and hook failover events for alerting."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/
  - https://redis.io/docs/latest/develop/reference/sentinel-clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel-aware clients and failover notification

**Goal:** applications follow the primary automatically when Sentinel promotes a replica.

## The protocol
1. Client connects to any Sentinel from a list, asks `SENTINEL get-master-addr-by-name mymaster`.
2. Connects to that address and verifies with `ROLE` that it is `master` (a stale answer is possible).
3. If it is not a master, waits a few hundred milliseconds and repeats from step 1; after a disconnect it also repeats from step 1.
4. Optionally subscribes to Sentinel's Pub/Sub (for example `+switch-master`) for early notice; messages can be missed, so the lookup procedure above stays the source of truth.

## Client examples
```python
from redis.sentinel import Sentinel
s = Sentinel([("s1", 26379), ("s2", 26379), ("s3", 26379)], socket_timeout=0.5, sentinel_kwargs={"password": "..."})
primary = s.master_for("mymaster", password="...", socket_timeout=0.5)
replica = s.slave_for("mymaster", password="...")
```

## Do not
- Hard-code the primary IP or use a VIP without a mechanism that moves it.
- Put Sentinel behind a load balancer for writes: clients must talk to the primary directly.
- Use client-side timeouts longer than your failover budget.

## Failover notifications
```text
sentinel notification-script mymaster /usr/local/bin/redis-notify.sh     # called on Sentinel events: event type and description as arguments (see sentinel.conf)
sentinel client-reconfig-script mymaster /usr/local/bin/redis-reconfig.sh # called on failover with old/new addresses
```
`client-reconfig-script` args: `<master-name> <role> <state> <from-ip> <from-port> <to-ip> <to-port>`; use it to update DNS/proxy config or page on-call. A script may run for at most 60 seconds (then it is killed and retried); exit code 1 is retried later (up to 10 times), 2 or higher is not. `SENTINEL SET` cannot change these two settings at runtime unless `sentinel deny-scripts-reconfig no` (default yes).

## Monitoring
`redis-cli -p 26379 PSUBSCRIBE '*'` streams events (`+sdown`, `+odown`, `+try-failover`, `+elected-leader`, `+switch-master`). Alert on `+switch-master`.

## Verify
In staging run `SENTINEL FAILOVER mymaster`; the application keeps writing with only a few seconds of errors, and the reconfig script fires once.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the Sentinel clients guideline: ask Sentinels (first replying one moved to the front) with `SENTINEL get-master-addr-by-name`, verify with `ROLE`, retry after a few hundred milliseconds if it is not a master, optionally subscribe to Sentinel Pub/Sub but messages are not guaranteed; Sentinel list refresh is optional. Confirmed from sentinel.conf (8.2): client-reconfig-script arguments `<master-name> <role> <state> <from-ip> <from-port> <to-ip> <to-port>`, 60 second limit, exit code 1 retried up to 10 times, 2 or higher not retried, `deny-scripts-reconfig` default yes. redis-py `Sentinel(sentinels, min_other_sentinels, sentinel_kwargs, **connection_kwargs)`, `master_for` and `slave_for` signatures confirmed from sentinel.py. Removed unconfirmed: READONLY error step, Java and Node client lines.
Method: documentation only; no commands were run.

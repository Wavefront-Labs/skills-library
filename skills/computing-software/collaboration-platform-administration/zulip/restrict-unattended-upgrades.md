---
id: computing-software.collaboration-platform-administration.zulip.restrict-unattended-upgrades
name: restrict-unattended-upgrades
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [unattended-upgrades, package-blacklist, apt-upgrades]
level: practitioner
status: docs-checked
description: "Stop Ubuntu unattended-upgrades from restarting PostgreSQL, memcached, Redis or RabbitMQ under Zulip: Package-Blacklist patterns and the restart-server follow-up."
sources: ["https://zulip.readthedocs.io/en/latest/production/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restricting unattended upgrades

Unrestricted Ubuntu unattended-upgrades will upgrade (and therefore restart) PostgreSQL the moment a new release appears. Restarting PostgreSQL, memcached, Redis or RabbitMQ drops the connections Zulip processes hold. Zulip reconnects on its own, so the outage ends when the service is back, but each of its roughly 20 workers throws an error and sends an error email when it next uses the dead connection.

An unplanned outage also produces a trickle of error emails over hours or days, because idle workers only discover a dropped connection when they next use it.

Prevent the trickle for planned package updates by running `~zulip/deployments/current/scripts/restart-server` after installing updates to PostgreSQL, memcached, RabbitMQ or Redis.

Prevent surprise upgrades by excluding those packages in `/etc/apt/apt.conf.d/50unattended-upgrades`. The blacklist entries are Python regular expressions:

```
Unattended-Upgrade::Package-Blacklist {
    "libc\d+";
    "memcached$";
    "nginx-full$";
    "postgresql-\d+$";
    "postgresql-\d+-pgdg-pgroonga$";
    "rabbitmq-server$";
    "redis-server$";
    "supervisor$";
};
```

If you disable unattended-upgrades entirely instead, remember to install apt upgrades manually and regularly. The Nagios plugin `check_debian_packages` can warn when the system falls behind.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/troubleshooting.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.

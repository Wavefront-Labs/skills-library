---
id: computing-software.collaboration-platform-administration.zulip.hardware-requirements-and-scaling
name: hardware-requirements-and-scaling
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [zulip-sizing, hardware-requirements, scalability, capacity-planning]
level: practitioner
status: docs-checked
description: "Size a Zulip server from daily active users: RAM, CPU, disk, dedicated database, S3 uploads, warm spares and Tornado sharding guidance."
sources: ["https://zulip.readthedocs.io/en/latest/production/requirements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zulip hardware requirements and scaling

Minimum is a dedicated machine on a supported Ubuntu or Debian release, x86-64 or aarch64, 2 GB RAM (add 2 GB swap below 5 GB RAM) and about 10 GB free disk. At 100+ users use 2 CPUs and 4 GB RAM. Use SSD with no IOPS cap, because the disk mostly serves the database.

Scaling depends on daily active users, total accounts and message volume. Django dominates resource use, so RAM is the usual constraint:

- 25+ daily actives: 4 GB
- 100+: 8 GB
- 400+: 16 GB for the app server plus 16 GB for the database
- 2000+: 32 GB plus 32 GB for the database, then linear

For database disk, budget 10 GB per million messages plus 1 GB per 1000 users when messages have under 100 recipients. If most go to public channels with 10K+ subscribers, add 20 GB per 1000 accounts per million public messages.

At scale, use the S3 uploads backend and give the app server about 50 GB for OS, code, logs and scratch, more if uploads are cached heavily. Hundreds of daily actives justify a remote PostgreSQL server.

For disaster recovery, keep a warm spare app server holding a copy of `/etc/zulip` and either synced `LOCAL_UPLOADS_DIR` or S3, plus a PostgreSQL warm standby. Prefer a hot spare over load-balancing one realm across several app servers. Thousands of daily actives can shard the Tornado service by realm or by user ID.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/requirements.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.

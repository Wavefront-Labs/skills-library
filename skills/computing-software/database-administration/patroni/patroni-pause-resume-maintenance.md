---
id: computing-software.database-administration.patroni.patroni-pause-resume-maintenance
name: patroni-pause-resume-maintenance
category: computing-software
field: database-administration
product: patroni
tags: [patroni, pause, maintenance, patronictl, upgrade]
level: practitioner
status: docs-checked
description: "What Patroni does and stops doing in pause mode, and how to enter and leave it."
sources:
  - https://patroni.readthedocs.io/en/latest/pause.html
  - https://patroni.readthedocs.io/en/latest/patronictl.html
  - https://patroni.readthedocs.io/en/latest/watchdog.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: detach Patroni from HA decisions for planned maintenance.

Pause mode suits uncommon activities such as major version upgrades or corruption recovery, where nodes are started, stopped or temporarily promoted. It is equivalent to Pacemaker maintenance mode and keeps cluster state in the DCS.

In pause mode Patroni does not change PostgreSQL state, except:
- Each member key in DCS is updated with current information, which runs read-only queries on running members.
- The primary with the leader lock keeps updating it. If that node is demoted manually, Patroni releases the lock instead of promoting it back.
- Manual unscheduled restart, failover/switchover and reinitialize are allowed; no scheduled action is. Switchover is allowed only when the target node is specified.
- Parallel primaries produce a warning, not a demotion.
- With no leader lock, the running primary acquires it; with several primaries the first to acquire wins. If no primary exists, no replica is promoted, except that after a manual promotion releasing the lock only the named candidate may take it.
- Stopped Postgres is not started; stopping Patroni does not stop Postgres.
- Slots that are not other members or configured permanent slots are not removed.

Commands: `patronictl pause [CLUSTER] [--wait]` and `patronictl resume [CLUSTER] [--wait]` (`--wait` blocks until all members have recognised the change), or PATCH the cluster config key with `{"pause": true/false/null}`. The watchdog is disabled while paused; `patronictl list` shows Maintenance mode in the footer (pretty format only).

## Checked

2026-11-08. Confirmed against the Patroni pause/resume page (read in full), the patronictl page (pause, resume and list sections) and the watchdog page (disabled while paused).

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.netbox.background-jobs-scheduling
name: background-jobs-scheduling
category: computing-software
field: systems-network-administration
product: netbox
tags: [background-jobs, rqworker, scheduled-jobs]
level: practitioner
status: docs-checked
description: "Know which tasks run on the worker and how scheduling works."
sources: ["https://netboxlabs.com/docs/netbox/features/background-jobs/", "https://netboxlabs.com/docs/netbox/installation/4a-gunicorn/", "https://netboxlabs.com/docs/netbox/installation/2-redis/", "https://netboxlabs.com/docs/netbox/features/event-rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Background jobs

Goal: know what runs outside the web request cycle.

NetBox executes certain functions as background tasks:

- Custom script execution
- Synchronization of remote data sources
- Housekeeping tasks

Plugins can enqueue their own background tasks using the **Job** model. All of them are executed by the `rqworker` process or processes, which runs as the `netbox-rq` systemd service in the gunicorn setup. NetBox uses Redis for caching and queuing.

**Scheduling.** A job can run immediately or at a set time in the future. Scheduled jobs can also repeat at a set interval.

**Practical consequences**

- If a script, sync or event seems stuck in a pending state, check that `netbox-rq` is active.
- Redis must be reachable, since NetBox uses it for queuing.
- Since workers execute what is read from Redis, keep Redis private and authenticated as the install guide advises.

**Where to look**

- Event rules also queue work for the same worker.

**Checklist**

1. Worker service enabled.
2. Redis tasks database reachable.
3. Use scheduling for repeating work.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Background Jobs, Event Rules, Gunicorn and Redis installation pages (all read in full). Removed the unconfirmed claim about the Job model recording status.

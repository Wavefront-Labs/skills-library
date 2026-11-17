---
id: computing-software.systems-network-administration.healthchecks.self-hosted-db-cleanup
name: self-hosted-db-cleanup
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, pruneusers, prunetokenbucket, pruneobjects, ping-log-limit]
level: advanced
status: docs-checked
description: "Maintain a self-hosted Healthchecks database: automatic ping pruning, the Ping log limit, and the pruneusers, prunetokenbucket and pruneobjects commands."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/docker/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Automatic cleanup removes old rows in `api_ping`, `api_flip` and `api_notification`. By default the 100 most recent pings per check are kept. An admin can raise this per user in the user's Profile, "Ping log limit" field.

Manual commands:
- `./manage.py pruneusers`: removes accounts older than one month that never logged in.
- `./manage.py prunetokenbucket`: removes `api_tokenbucket` rate-limit records older than one day.
- `./manage.py pruneobjects`: removes stale objects from external object storage, such as those left by deleted checks, projects or accounts. Run occasionally, for example monthly.

In Docker, run them inside the container:

```
docker compose run web /opt/healthchecks/manage.py pruneobjects
```

Safety: test the commands on a copy of the database first; in production run them regularly and keep automatic backups.

Other upkeep: `sendalerts` must always run, `sendreports` sends due reports, and `compress`, `collectstatic` and `migrate` run on every upgrade. Back up the database and monitor the Healthchecks instance itself (the API `status` endpoint helps).

## Checked

2026-11-04. Confirmed against the Healthchecks self-hosted page, README and docker README: tables pruned automatically, the default of 100 most recent pings per check, Ping log limit in the user Profile, pruneusers, prunetokenbucket and pruneobjects behaviour, the monthly example, testing on a copy, running commands inside the container, the sendalerts and sendreports requirements and the per-upgrade compress, collectstatic and migrate commands. Nothing removed.

Method: documentation only; no commands were run.

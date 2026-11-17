---
id: computing-software.collaboration-platform-administration.zulip.split-services-across-hosts
name: split-services-across-hosts
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [standalone-services, puppet-profiles, multi-host-deployment]
level: advanced
status: docs-checked
description: "Run Zulip dependencies such as Memcached, PostgreSQL, RabbitMQ, Redis and Smokescreen on separate machines using settings.py and zulip::profile Puppet classes."
sources: ["https://zulip.readthedocs.io/en/latest/production/deployment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running Zulip services on different machines

Each top-level service can live on its own host: Memcached, PostgreSQL, RabbitMQ, Redis and Smokescreen. On the application server, edit `/etc/zulip/settings.py`; searching the file for a service name shows inline comments explaining how to point at a remote instance.

On the service host, apply only the relevant Puppet profile. Every module under `zulip::profile` can be configured standalone. After unpacking a release tarball, for example, a Redis server is:

```
./scripts/setup/install --puppet-classes zulip::profile::redis
```

The list of includes in the main standalone manifest for the default all-in-one server shows the profiles you are most likely to want, and you may subclass lower-level manifests for customisation. The project's own production Puppet repository is cited as an example of doing so.

For the database specifically, see the dedicated PostgreSQL documentation, which covers a managed cloud instance such as AWS RDS and warm-standby replicas. The app-server install then uses `--puppet-classes=zulip::profile::standalone_nodb`.

A Smokescreen host uses `zulip::profile::smokescreen`; the application servers then point their `[http_proxy]` block in `zulip.conf` at it.

## Checked

Confirmed against the Running Zulip's service dependencies on different machines section of the deployment page and the standalone_nodb install in the PostgreSQL page. Removed the closing advice about secrets, firewall rules and the benefit of splitting (not on the pages).

Method: docs-checked 2026-11-09 against docs/production/deployment.md and docs/production/postgresql.md in the zulip/zulip repository (main), the sources of the cited pages.

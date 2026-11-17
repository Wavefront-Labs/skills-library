---
id: computing-software.collaboration-platform-administration.zulip.install-on-existing-server
name: install-on-existing-server
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [existing-server, nginx-merge, shared-host]
level: advanced
status: docs-checked
description: "Install Zulip on a host that already runs other services and handle the nginx merge, Puppet agent, PostgreSQL version and shared Redis, Memcached and RabbitMQ conflicts."
sources: ["https://zulip.readthedocs.io/en/latest/production/install-existing-server.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing Zulip on an existing server

This is expert-only and unsupported: the installer assumes it may overwrite configuration under `/etc`. Back up first and have a rebuild script ready.

nginx: save your current config, fetch Zulip's nginx template, and merge them with a diff tool before installing. The file is a Puppet ERB template, so replace each `<%= ... %>` placeholder, for example the CA bundle reference becomes `/etc/ssl/certs/ca-certificates.crt` on Debian and Ubuntu. After the install, merge the Zulip file into the live `nginx.conf` and restart nginx. Zulip's Puppet changes ownership of `/var/log/nginx` so the `zulip` user can read it, which may affect other sites. If other virtual hosts exist, set `nginx_server_name` in `/etc/zulip/zulip.conf` so Zulip's server blocks claim only their hostnames.

Puppet: a running Puppet server makes the installer fail with a certificate request error to port 8140. Stop the `puppet-agent` and `puppet` services first.

PostgreSQL: any PostgreSQL version other than the one Zulip expects, found at install time, aborts the install. Pass `--postgresql-version=` to use your version; the package is upgraded from the PostgreSQL apt repository but data is kept. Zulip uses `main` as a database name, so make sure none of yours is called that.

Memcached, Redis and RabbitMQ are configured for Zulip with basic settings; make sure other users of those are compatible.

There is no uninstall process.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/install-existing-server.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.

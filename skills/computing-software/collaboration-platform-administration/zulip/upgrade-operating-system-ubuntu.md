---
id: computing-software.collaboration-platform-administration.zulip.upgrade-operating-system-ubuntu
name: upgrade-operating-system-ubuntu
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [os-upgrade, do-release-upgrade, upgrade-zulip-stage-2, rabbitmq-purge]
level: sme
status: docs-checked
description: "Upgrade Ubuntu under a running Zulip server: back up, purge rabbitmq-server on 22.04 to 24.04, do-release-upgrade, reinstall with upgrade-zulip-stage-2, upgrade-postgresql."
sources: ["https://zulip.readthedocs.io/en/latest/production/upgrade.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading the operating system under Zulip

Docker users upgrade the OS by upgrading the image. Otherwise follow this flow, shown for Ubuntu 22.04 to 24.04.

1. Upgrade Zulip to the latest 8.x release (at least 8.3, which adds Ubuntu 24.04 support).
2. As the `zulip` user, run `stop-server` then `manage.py backup --output=...` from the current deployment.
3. Remove RabbitMQ before the OS upgrade, since Ubuntu's packaging fails moving from 3.9 to 3.12. As root run `rabbitmqctl list_queues`; if queues hold events, run `manage.py process_queue --all` as `zulip` until they drain (Ctrl-C), or accept losing that data; then `apt purge rabbitmq-server`, which removes its database and configuration.
4. As root run `do-release-upgrade`. For configuration files of Zulip-managed services answer `N` (keep installed), which hardly matters since the next step rewrites them. Answer `N` to the reboot prompt.
5. Reinstall Zulip's dependencies and configuration:

```
rm -rf /srv/zulip-venv-cache/* ~zulip/deployments/current/.venv /root/.cache/uv
~zulip/deployments/current/scripts/lib/upgrade-zulip-stage-2 \
    ~zulip/deployments/current/ --ignore-static-assets --audit-fts-indexes
```

Ignore a pending kernel upgrade dialog and choose "cancel" for outdated daemons. This recompiles Python dependencies, rebuilds full-text search indexes and reinstalls RabbitMQ.

6. As root run `scripts/setup/upgrade-postgresql`, then `reboot`.

Older hops (20.04 to 22.04, 18.04 to 20.04) are similar; 18.04 to 20.04 also needs collation-affected indexes regenerated because glibc changed.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/upgrade.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.

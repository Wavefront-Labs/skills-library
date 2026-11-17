---
id: computing-software.collaboration-platform-administration.zulip.upgrade-zulip-release
name: upgrade-zulip-release
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [zulip-upgrade, upgrade-zulip, release-tarball, upgrade-notes]
level: intro
status: docs-checked
description: "Upgrade a Zulip server to a new release with upgrade-zulip and the release tarball: read upgrade notes, what the upgrade does, and expected downtime."
sources: ["https://zulip.readthedocs.io/en/latest/production/upgrade.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading Zulip to a release

Run the latest release; the project works to keep upgrades uneventful. Extra care applies if you use Docker, have patched Zulip, or modified Zulip-managed configuration files.

Steps:

1. Read the upgrade notes in the changelog for every release between your version and the target.
2. Download the release tarball from the download server, for example `curl -fLO https://download.zulip.com/server/zulip-server-latest.tar.gz`.
3. As root on the server run:

```
~zulip/deployments/current/scripts/upgrade-zulip zulip-server-latest.tar.gz
```

What the upgrade does, in order:

1. Runs `apt-get upgrade`.
2. Installs new versions of Zulip's dependencies, mainly Python packages.
3. Shuts down the Zulip service.
4. Runs a `puppet apply`.
5. Runs database migrations.
6. Brings the service back up on the new version.

Expect brief downtime, under 30 seconds unless an expensive migration is involved. Such migrations are called out in the release notes and can usually be avoided with some care. If downtime matters, rehearse the upgrade on a restored backup, upgrade off hours, or arrange paid support.

Afterwards consider upgrading PostgreSQL, which is versioned separately. Troubleshooting and rollback are covered in their own procedure. Scripts are idempotent, so rerunning after fixing a problem is safe.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/upgrade.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.

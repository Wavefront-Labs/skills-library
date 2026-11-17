---
id: computing-software.collaboration-platform-administration.zulip.preserve-local-service-config-changes
name: preserve-local-service-config-changes
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [puppet-overwrite, nginx-include, zulip-include, local-config-changes]
level: advanced
status: docs-checked
description: "Keep local changes to Zulip-managed service configs across upgrades: zulip-puppet-apply dry run, nginx include directories conf.d, zulip-include app.d and localhost.d."
sources: ["https://zulip.readthedocs.io/en/latest/production/upgrade.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Preserving local configuration changes

Warning: if you edited service configuration files that Zulip installs, such as the nginx configuration, the `puppet apply` run during upgrades overwrites them.

Find out what would be overwritten before upgrading by running `scripts/zulip-puppet-apply` without the `-f` option. It does a test Puppet run and lists the changes it would make. Save copies of any files you modified, upgrade, then restore your configuration.

Prefer supported options first. Zulip's configuration is designed to be flexible enough for everything from small self-hosted systems to Zulip Cloud, so check `/etc/zulip/zulip.conf` for an option covering your customisation. If you must modify files, report the need to the project so the Puppet configuration can be made flexible enough.

To extend nginx without editing Zulip's files, use the include directories, each in a different context:

- `/etc/nginx/conf.d` is in the `http` context.
- `/etc/nginx/zulip-include/app.d` is in the `server` context for the public-facing server.
- `/etc/nginx/zulip-include/localhost.d` is in the `server` context for the server listening on `127.0.0.1:80`, used for internal inter-process communication.

If you patch Zulip's code itself, the upgrade procedure has additional requirements; see the guidance on modifying Zulip.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/upgrade.html (zulip.readthedocs.io, latest). Removed: the inference that include directories survive because Puppet does not rewrite them.

Method: documentation only; no commands were run.

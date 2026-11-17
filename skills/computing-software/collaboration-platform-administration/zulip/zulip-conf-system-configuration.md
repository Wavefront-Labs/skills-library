---
id: computing-software.collaboration-platform-administration.zulip.zulip-conf-system-configuration
name: zulip-conf-system-configuration
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [zulip-conf, system-configuration, puppet-apply, deploy-options]
level: practitioner
status: docs-checked
description: "Understand /etc/zulip/zulip.conf: INI sections, truthy values, puppet_classes, pgroonga, timesync, deploy_options and zulip-puppet-apply to apply changes."
sources: ["https://zulip.readthedocs.io/en/latest/production/system-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# /etc/zulip/zulip.conf basics

`/etc/zulip/zulip.conf` is an INI file for system and deployment properties; `/etc/zulip/settings.py` configures the application. Changes to `zulip.conf` generally take effect only after running `~zulip/deployments/current/scripts/zulip-puppet-apply` as root. It shows the changes it will make and asks for confirmation.

Boolean values: `true` and `false` are canonical, but case-insensitively `1`, `y`, `t`, `yes`, `enable` and `enabled` count as true. Anything else, including an empty string, is false.

`[machine]` section:

- `puppet_classes`: comma-separated Puppet classes. The usual `zulip::profile::standalone` bundles app_frontend, memcached, postgresql, rabbitmq, redis and smokescreen profiles. Add `zulip::apache_sso` when using Apache-based single sign-on with `REMOTE_USER`.
- `pgroonga`: true enables the multi-language PGroonga search extension.
- `timesync`: `chrony` by default, also `ntpd` or `none`. Use `none` only in containers like LXC that cannot set the clock, because Zulip needs an accurate clock.

`[deployment]` section:

- `deploy_options`: passed from `upgrade-zulip` into stage 2. `--skip-puppet` leaves you to run `zulip-puppet-apply`; `--skip-migrations` leaves `./manage.py migrate` to you (set `MIGRATIONS_ADD_REMOVE_INDEXES_CONCURRENTLY = True` if migrating on a live server so index changes do not lock tables); `--skip-purge-old-deployments` keeps old deployments, otherwise only those from the last two weeks are kept. Most installations should set none.
- `git_repo_url`: default repository for Git-based upgrades.

## Checked

2026-11-08. Checked: settings and defaults read against the Zulip system-configuration page (docs/production/system-configuration.md, read in full). Removed: nothing.

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.fluentd.plugin-management-and-versions
name: plugin-management-and-versions
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, fluent-gem, plugins, gemfile, td-agent-gem, plugin-directory, version-pinning]
level: practitioner
status: docs-checked
description: "Install and pin Fluentd plugins: fluent-gem, td-agent-gem, -p and /etc/fluent/plugin, version pinning and the --gemfile option with Bundler."
sources:
  - https://docs.fluentd.org/deployment/plugin-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd plugin management
- Install with `fluent-gem install fluent-plugin-grep`. With td-agent use `td-agent-gem`, or plugins will not be found. After updating Fluentd's Ruby version, reinstall plugins that have C extensions. Native-extension gems need build tools (`gcc`, `make`, `autoconf`).
- Load local plugin files with `fluentd -p /path/to/plugin` (repeatable), or place them in `/etc/fluent/plugin` (td-agent: `/etc/td-agent/plugin`), which is on the load path by default.
- An unreliable plugin can break Fluentd; the page's advice is to avoid them and report faults to the owner.

Version pinning on production: avoid bare `gem install fluentd`, `gem install fluent-plugin-elasticsearch` and especially `gem update`; use `-v`, for example `gem install fluentd -v 1.2.1`.

`--gemfile` uses Bundler; Fluentd installs only the listed gems and loads them separately from shared gems, preventing surprise updates and reinstalling on Ruby upgrades:
```
source 'https://rubygems.org'
gem 'fluentd', '1.2.1'
gem 'fluent-plugin-elasticsearch', '2.10.3'
```
```
fluentd --gemfile /etc/fluent/Gemfile
```
For td-agent 3.1.1 the page uses a systemd drop-in `override.conf` setting `TD_AGENT_OPTIONS=--gemfile=... --gem-path=...`, edited with `systemctl edit td-agent.service`; all listed gems download even if bundled.

If `fluent-gem list` shows several versions of a plugin, the latest is used.

## Checked

2026-11-04. Confirmed against the Fluentd Plugin Management page (docs.fluentd.org/deployment/plugin-management): fluent-gem, td-agent-gem, native extension tools, -p, /etc/fluent/plugin and /etc/td-agent/plugin, version pinning commands, --gemfile and the td-agent 3.1.1 drop-in, the fluent-gem list FAQ. Nothing removed.

Method: documentation only; no commands were run.

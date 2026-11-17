---
id: computing-software.database-administration.patroni.patroni-config-layers-precedence
name: patroni-config-layers-precedence
category: computing-software
field: database-administration
product: patroni
tags: [patroni, configuration, dynamic-config, environment, sighup]
level: intro
status: docs-checked
description: "The three Patroni configuration layers (dynamic, local file, environment), their precedence, and how each is changed."
sources:
  - https://patroni.readthedocs.io/en/latest/patroni_configuration.html
  - https://patroni.readthedocs.io/en/latest/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know where a setting lives and how to change it safely.

There are three layers:
1. Global dynamic configuration, stored in the DCS and applied on all nodes. Change it with `patronictl edit-config` or the REST API. Options not part of the startup configuration are applied asynchronously on the next wake-up cycle and the node is reloaded.
2. Local configuration file (patroni.yml). It takes precedence over dynamic configuration. Reload it at runtime with SIGHUP, `POST /reload`, or `patronictl reload`. The local config may be a single file or a directory; YAML files in a directory load in sorted order and the last file wins on duplicate keys.
3. Environment configuration, which overrides both. Per the FAQ it is read only at startup, so changing it requires restarting the Patroni agent (take care not to cause a failover; consider `patronictl pause`).

If a changed Postgres parameter needs a restart, Patroni sets a `pending_restart` flag in the member data and status shows `"restart_pending": true`.

The reload via `patronictl reload` may fail with expired REST API certificates (mitigate with the `-k` option) or with wrong credentials after changing restapi or ctl credentials in a shared file.

Settings under `bootstrap.dcs` are used only once, at bootstrap; later changes there have no effect.

## Checked

2026-11-08: the three configuration layers, reload methods and sorted directory loading confirmed in the Patroni configuration page; environment configuration read only at startup, the reload failure cases and the bootstrap.dcs rule confirmed in the FAQ. Pages were read in full except where noted.

Method: documentation only; no commands were run.

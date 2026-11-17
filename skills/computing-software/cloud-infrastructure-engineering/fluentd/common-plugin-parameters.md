---
id: computing-software.cloud-infrastructure-engineering.fluentd.common-plugin-parameters
name: common-plugin-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, plugin-parameters, id, log-level, label]
level: intro
status: docs-checked
description: "Parameters every Fluentd plugin accepts: @type, @id (used for buffer, storage and logging paths), @log_level per plugin, and @label for inputs."
sources:
  - https://docs.fluentd.org/configuration/plugin-common-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common plugin parameters
- `@type`: selects the plugin.
- `@id`: unique name for the plugin instance. It is used as paths for buffer, storage, logging and other purposes. The page says to set it on every plugin to enable the `root_dir` feature globally (see `system-directive-settings`).
- `@log_level`: per-plugin level, default `info`. The global level comes from `log_level` in `<system>` or `-v`/`-q`. Use it to quiet a noisy plugin or enable `debug` for just one instance.
- `@label` (event-emitting plugins such as inputs): routes events to a `<label>` section. Value must start with `@`. Recommended over tag rewriting for modular configs.

```
<match>
  @type file
  @id service_www_accesslog
  path /path/to/my/access.log
</match>
```

## Checked

2026-11-04. Confirmed against the Fluentd Config: Common Parameters page (docs.fluentd.org/configuration/plugin-common-parameters): @type, @id, @log_level default and override behaviour, @label rules. Removed: the claim that in_monitor_agent reports @id as plugin_id (not on this page).

Method: documentation only; no commands were run.

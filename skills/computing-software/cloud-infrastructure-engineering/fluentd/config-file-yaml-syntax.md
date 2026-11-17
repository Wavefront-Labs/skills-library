---
id: computing-software.cloud-infrastructure-engineering.fluentd.config-file-yaml-syntax
name: config-file-yaml-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, yaml, config-file, include, fluent-s]
level: practitioner
status: docs-checked
description: "Write Fluentd configuration in YAML: system and config top-level objects, $type/$tag/$label keys, !fluent/s, !include, worker and label elements."
sources:
  - https://docs.fluentd.org/configuration/config-file-yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd YAML configuration
YAML is not a 1-to-1 mapping of the classic syntax. Two top-level objects: `system` and `config`. Under `config` use list elements `source`, `match`, `filter`, `label` (and `worker`).

Special keys and tags:
- `$type` (plugin type), `$tag` (match/filter pattern), `$label` (input label), `$arg` (a directive argument, e.g. worker range), `$name` (label name), `$id`, `$log_level` (`$log_level` since v1.17.1 / v1.16.6; older versions use deprecated `log_level`).
- `!fluent/s` marks a Fluentd string equal to a double-quoted string, for `"#{Socket.gethostname}"`.
- `!fluent/json` marks a hash value.
- `!include` includes other files, e.g. `- !include config.d/*.yaml`.

```
config:
  - source:
      $type: forward
      port: 24224
  - match:
      $tag: myapp.access
      $type: file
      path: /var/log/fluent/access
```
Quote label values (`$label: '@SYSTEM'`); a `label` element needs `$name` and its own nested `config`. A `worker` element takes `$arg: 0-1` and nested `config`. `system:` holds system-wide settings (for example `log_level`, `without_source`, `process_name`).

## Checked

2026-11-04. Confirmed against the Fluentd Config File Syntax (YAML) page (docs.fluentd.org/configuration/config-file-yaml): top-level objects, special keys and tags, the $log_level version note, label quoting, worker $arg, !include. Reworded the system: sentence to match the page.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.icinga-2.command-arguments-set-if-skip-key-order-repeat
name: command-arguments-set-if-skip-key-order-repeat
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, command-arguments, set-if, skip-key, repeat-key, order, required, description]
level: advanced
status: docs-checked
description: Use CheckCommand arguments fields value, description, required, skip_key, set_if, order and repeat_key to build plugin command lines.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# command arguments: set_if, skip_key, order, repeat_key
Prefer the `arguments` dictionary over a long `command` array. Each key is a parameter; its value is a dictionary with optional fields. An argument is omitted when its value is not set.

- **value**: usually a macro. Prefer the long plugin parameter name, with the schema `<command name>_<parameter name>`, e.g. `value = "$systemd_unit$"` and a default `vars.systemd_unit = "icinga2"`.
- **description**: best practice (also in the ITL) is to copy the plugin help text here; Icinga Director shows it.
- **required**: `true` logs an error when the argument is missing, easier than plugin errors. Default is optional.
- **skip_key**: the dictionary key cannot be empty, so use `skip_key = true` for parameters printed without a name. Together with `required = true` and `order = -1` the icingacli businessprocess example prints `'/bin/icingacli' 'businessprocess' 'process' 'check' 'bp-shop-web'`.
- **set_if**: adds a parameter without value (e.g. `--sni` when `$http_sni$` is true; numeric values are allowed), or conditions a parameter that has a value. For runtime evaluation use a lambda: `set_if = {{ macro("$postgres_unixsocket$") == false }}`.
- **order**: numeric position, e.g. `-5`, `-4`, `99`. Positional arguments need thorough testing.
- **repeat_key**: for array values the key and each element repeat by default (`'-a' 'x' '-a' 'y'`). `repeat_key = false` gives `'-a' 'x' 'y'`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the Command Arguments section of the Icinga 2 Monitoring Basics chapter (03-monitoring-basics.md from the Icinga/icinga2 repository, the source of the cited page) from Value through Repeat Key. Confirmed optional-by-default and omission when unset, the naming schema and systemd example, description and Icinga Director, required logging an error, skip_key with the icingacli example and resulting command line, both set_if scenarios including the lambda, order values -5, -4 and 99 and the testing note, and repeat_key true and false outputs. Nothing was removed. No commands were run.

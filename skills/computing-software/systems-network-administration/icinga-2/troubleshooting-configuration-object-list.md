---
id: computing-software.systems-network-administration.icinga-2.troubleshooting-configuration-object-list
name: troubleshooting-configuration-object-list
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, troubleshooting, object-list, configuration, dump-objects, inheritance, dollar-sign]
level: practitioner
status: docs-checked
description: Debug Icinga 2 configuration with icinga2 object list --name --type, daemon -C --dump-objects, notice-level validation, template inheritance origins and dollar sign escaping.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/15-troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting configuration
**`icinga2 object list`** shows every object with its attributes and where each was modified (file and line), which reveals template inheritance and objects created by apply rules. Filter: `icinga2 object list --name *ssh* --type Service`. The output is read from a cache, so run `icinga2 daemon -C --dump-objects` to refresh `icinga2.debug`; group assign expressions are a known gap and are not reflected in host output. The API also gives runtime objects.

**Apply rules not matching:** analyse them with the script debugger.

**Check command definitions:** built-ins come from `include <itl>` and `include <plugins>` in `icinga2.conf`, found under `IncludeConfDir` (default `/usr/share/icinga2/includes`). These files are overwritten on upgrade; put your own commands in a file such as `conf.d/commands.conf`.

**Configuration ignored:** check it is not commented out (`//`, `#`, `/* */`) and that it is included from `icinga2.conf`. Validate with notice severity: `icinga2 daemon -C -x notice | grep command`.

**Dollar signs:** a validation error `Closing $ not found in macro format string` means a literal single `$` is not escaped. Write `$$`, for example `"top-syntax=$${list}"`.

## Checked

2026-11-04. Confirmed against the Icinga 2 troubleshooting chapter: object list cache and daemon -C --dump-objects, known group assign gap, IncludeConfDir default, notice-level validation and the $$ escape error.

Method: documentation only; no commands were run.

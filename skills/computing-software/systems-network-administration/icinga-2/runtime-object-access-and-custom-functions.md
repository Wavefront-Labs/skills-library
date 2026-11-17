---
id: computing-software.systems-network-administration.icinga-2.runtime-object-access-and-custom-functions
name: runtime-object-access-and-custom-functions
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, get-host, get-time-period, global-functions, lambda, set-if, cluster-check, assign-where]
level: advanced
status: docs-checked
description: "Use Icinga 2 functions in object configuration: global functions, function-valued attributes, assign where, set_if, get_host at runtime."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# runtime object access and custom functions
**Global functions.** Register them in the global scope, for example in a `functions.conf` included right after `constants.conf` (or in constants.conf):
```
globals.state_to_string = function(state) { ... }
```
Use an else branch with `log()` for better error handling and test in the debug console (`icinga2 console`). These functions are not marked side-effect-free, so they are not available via the REST API.

**As attributes.** A function-valued attribute can call a global function that returns an inner function using `use(...)`, e.g. a `group_specific_value(group, group_value, non_group_value)` returning 300 for hosts in `slow-lan` and 100 otherwise for `ping_wrta`.

**In assign where.** Write a global function when match/in is not enough, e.g. checking that a host uses a template matching `lexmark*`, or inspecting a nested `vars_app` dictionary; then call it inside `assign where`.

**In set_if.** Use a lambda such as a `contains` call on a dictionary; it fails if the variable is not a Dictionary, so guard with `typeof`.

**As command attribute.** `command` may be a function returning an array, handy for NotificationCommand/EventCommand to pick a script based on a custom variable.

**Accessors.** `get_host(name).state`, `get_host(node).last_check_result.output` and `get_time_period("backup").is_inside` allow a virtual cluster host state or time-dependent thresholds (return 20 or 5 for `load_wload1` depending on the period).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/.
Reworded the attribute-access paragraph to match the page. No commands were run.

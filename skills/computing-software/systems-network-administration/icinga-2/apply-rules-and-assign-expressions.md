---
id: computing-software.systems-network-administration.icinga-2.apply-rules-and-assign-expressions
name: apply-rules-and-assign-expressions
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, apply, assign-where, ignore-where, match, regex, service-apply]
level: practitioner
status: docs-checked
description: "Write Icinga 2 apply rules with assign where and ignore where, match and regex, the in operator, and attribute inheritance from vars."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apply rules and assign expressions
Apply rules generate Service, Notification, Dependency and ScheduledDowntime objects from a pattern; one rule can replace 1000 service objects:
```
apply Service "ping4" {
  check_command = "ping4"
  assign where host.address
}
```
Every expression must evaluate to boolean; an empty string or an undefined attribute (for example `host.vars.attribute_does_not_exist`) is false. Multiple `assign where` rows are OR-ed; combine conditions with `&&`/`||` (or `and`/`or`). `ignore where` removes matches.

Expression examples from the docs:
```
assign where "hostgroup-dev" in host.groups
assign where host.vars.application_type == "database"
assign where host.vars.app_dict.contains("app")
assign where match("webserver*", host.name)
assign where regex("^webserver-[\\d+]", host.name)
ignore where match("*internal", host.name)
```
Apply notifications with `apply Notification "x" to Service` or `to Host`. Attributes can be set from the matched object, e.g. `user_groups = host.vars.notification.mail.groups`, and conditional statements can override template values (interval, period, command) from host custom variables.

Dependencies and recurring downtimes use the same mechanism. Use `icinga2 object list` after `icinga2 daemon -C` to inspect generated objects.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/. No commands were run.

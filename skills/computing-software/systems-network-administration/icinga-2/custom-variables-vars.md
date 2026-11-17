---
id: computing-software.systems-network-administration.icinga-2.custom-variables-vars
name: custom-variables-vars
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, custom-variables, vars, dictionary, nested-values, function-values]
level: practitioner
status: docs-checked
description: Define Icinga 2 custom variables in the vars dictionary with value types, nesting, and function values evaluated at runtime.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# custom variables (vars)
Custom variables live in the `vars` dictionary (older docs called them custom attributes). Three equivalent forms:
```
vars.ssh_port = 2222
vars = { ssh_port = 2222 }
vars["ssh_port"] = 2222
```
Valid values: strings, numbers, booleans, arrays, dictionaries and functions. Nesting is allowed:
```
vars.disks["disk /"] = {
  disk_partitions = "/"
}
vars.notification["mail"] = {
  groups = [ "icingaadmins" ]
}
```
Remember the resolved structure when reading sub-keys in apply rules or functions, for example `host.vars.notification.mail.groups`. That array matches what the `user_groups` attribute of a notification apply rule expects.

**Function values.** A custom variable can be a function; each time Icinga needs the value it runs the function and uses the return value:
```
vars.text = {{ Math.random() * 100 }}
```
Variables in scope are `user` (notifications), `service`, `host` and `command`. The `macro("$address$")` function reads any macro expression, and `resolve_arguments` resolves a command with arguments (used by the `by_ssh` command). Accessing object attributes at runtime is described in the advanced topics chapter.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the Custom Variables section of the Icinga 2 Monitoring Basics chapter (03-monitoring-basics.md from the Icinga/icinga2 repository, the source of the cited page) including Custom Variable Values and Functions as Custom Variables. Confirmed the three equivalent forms, the valid value types, nesting examples, the user_groups note, function values with the user, service, host and command scope, macro() and resolve_arguments with by_ssh. Nothing was removed. No commands were run.

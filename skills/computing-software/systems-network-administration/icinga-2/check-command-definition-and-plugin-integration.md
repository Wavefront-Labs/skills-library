---
id: computing-software.systems-network-administration.icinga-2.check-command-definition-and-plugin-integration
name: check-command-definition-and-plugin-integration
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, checkcommand, plugindir, check-mysql, command-parameters, vars, check-plugin]
level: practitioner
status: docs-checked
description: Integrate a monitoring plugin with a CheckCommand object, pass parameters from Host or Service custom variables, set defaults, and override per service or via apply for.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# check command definition and plugin integration
A CheckCommand defines the command line of a check and is referenced by `check_command` on Host and Service. The `checker` feature must be enabled to execute checks.

Put the plugin in `PluginDir` and call it with `--help` to learn its options. The command is an array of double-quoted strings; parameters go into the `arguments` dictionary and use custom variables as macros, with a command-type prefix such as `mysql_`:
```
object CheckCommand "my-mysql" {
  command = [ PluginDir + "/check_mysql" ]
  arguments = {
    "-H" = "$mysql_host$"
    "-u" = {
      required = true
      value = "$mysql_user$"
    }
  }
  vars.mysql_host = "$address$"
}
```
Defaults on the command are overridden by custom variables on the Host or Service (or inherited with `+=`):
```
apply Service "mysql-icinga-db-health" {
  import "generic-service"
  check_command = "my-mysql"
  vars.mysql_user = MysqlUsername
  vars.mysql_database = "icinga"
  assign where match("icinga2*", host.name)
}
```
`MysqlUsername` and `MysqlPassword` are global constants in constants.conf in this example. For a non-default SSH port set `vars.ssh_port = 2022` in the service apply rule or on the host; the macro resolution order decides which wins.

With `apply Service for (disk => config in host.vars.local_disks)`, use `vars += config` and set thresholds like `vars.disk_wfree = "10%"`. A variable such as `disk_partitions` can hold a string or an array.

Parameters for ITL commands are documented in the Icinga Template Library chapter.

## Checked

2026-11-04. Confirmed against the Icinga 2 service monitoring chapter: CheckCommand arguments, custom variable overrides, apply for loops and disk variables.

Method: documentation only; no commands were run.

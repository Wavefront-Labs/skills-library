---
id: computing-software.systems-network-administration.nagios-core.macro-arguments-and-substitution
name: macro-arguments-and-substitution
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, macros, macro-substitution, arg-macros, command-arguments, user-macros, resource-file]
level: practitioner
status: docs-checked
description: "How Nagios Core expands macros in command definitions, passes $ARG1$..$ARGn$ after ! separators, escapes literal ! and backslash, and keeps secrets in $USERn$ resource files."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/macros.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macro substitution

Before running a check, notification or event handler, Nagios replaces macros in the command definition. Host/service macros refer to the object the command is running for, so one command serves many hosts.

## Arguments
```
check_command  check_ping!200.0,80%!400.0,40%
```
`$ARG1$`=`200.0,80%`, `$ARG2$`=`400.0,40%`. Escape a literal `!` as `\!`; backslashes also need escaping.

## $USERn$
Defined in `resource_file` (multiple allowed), e.g. `$USER1$=/usr/local/nagios/libexec`. CGIs do not read resource files, so mode 600/660 is safe for passwords. Not exported to the environment.

## Macros containing macros
`HOSTNOTES`, `HOSTNOTESURL`, `HOSTACTIONURL` and the SERVICE equivalents may themselves contain macros.

## Scope
A macro used in a command where it is invalid is replaced with an empty string. Full list: `computing-software.systems-network-administration.nagios-core.standard-macro-reference`. Literal `$` in a command line is `$$` (see the command-definition skill).

## Debugging
In `debug_level`, 2048 is the Macros category.

## Checked

2026-11-04. Confirmed against the Macros page (substitution, $ARGn$ example, backslash escaping, macros containing macros, $USERn$ not in the environment), the main configuration page (resource_file, CGIs do not read it so 600 or 660 permissions are fine, debug_level 2048 = Macros) and the Macro list page (invalid macros become empty strings). Removed the claim that debug_level shows expanded command lines.

Method: documentation only; no commands were run.

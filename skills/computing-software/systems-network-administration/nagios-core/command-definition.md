---
id: computing-software.systems-network-administration.nagios-core.command-definition
name: command-definition
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, command-definition, define-command, command-line, command-name, arg-macros, dollar-escape]
level: practitioner
status: docs-checked
description: "Write Nagios Core command objects: command_name, command_line with macros, $ARGn$ passed after ! separators, escaping a literal dollar as $$, no semicolons."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/macros.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command definition

Both `command_name` and `command_line` are required.

```
define command {
    command_name    check_pop
    command_line    /usr/local/nagios/libexec/check_pop -H $HOSTADDRESS$
}
```

## Rules
- Macros in `command_line` are expanded before execution. Do not wrap the line in quotes.
- Literal `$` must be written `$$`.
- A semicolon cannot appear in `command_line`; work around it with a `$USERn$` macro holding the semicolon.
- Arguments: a service uses `check_command check_ping!200.0,80%!400.0,40%`; these become `$ARG1$`, `$ARG2$`. Escape a literal `!` with a backslash, and escape backslashes too.
- Use full paths to scripts and binaries (security page).

Used for host and service checks, notifications and event handlers.

## Checked

2026-11-04. Confirmed against the Object Definitions page (command_name and command_line, macros expanded, no quotes, $$ for a literal dollar sign, semicolon comment limitation and the $USERn$ workaround, bang-separated arguments), the Macros page (check_ping example, backslash escaping of ! and backslashes) and the Security page (full paths). Removed the unconfirmed self-check and the wider list of command uses.

Method: documentation only; no commands were run.

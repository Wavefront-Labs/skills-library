---
id: computing-software.systems-network-administration.zabbix.item-key-syntax
name: item-key-syntax
category: computing-software
field: systems-network-administration
product: zabbix
tags: [item-key, key-parameters, quoting, syntax, parameters]
level: practitioner
status: docs-checked
description: "Write valid item keys: allowed key name characters, quoting rules, empty parameters and array parameters."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/item/key
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An item key is a name optionally followed by comma-separated parameters in square brackets, such as net.tcp.service[ssh,,22].

Key name: only 0-9, a-z, A-Z, underscore, dash and dot.

Each parameter is one of three kinds:
- Quoted string: any Unicode character. Use double quotes only; single quotes are not supported. A parameter that contains a comma or a quotation mark must be quoted, and an embedded quotation mark is escaped with a backslash.
- Unquoted string: any Unicode character except comma and right square bracket, and it cannot start with a left square bracket.
- Array: parameters enclosed in square brackets, such as [a,b]. Multi-level arrays like [a,[b,[c,d]],e] are not allowed.

A parameter may be left empty to use its default. Keep the commas when later parameters are set: icmpping[,,200,,500] sets a 200 ms interval and 500 ms timeout and leaves the rest at defaults.

User macros and some built-in macros may appear in parameters, for example net.tcp.service[ssh,,{$SSH_PORT}]. Which built-in macros work in key parameters is listed under supported macros.

Shell quoting is separate: when testing with zabbix_get, wrap a key that contains spaces or quotes in shell quotes. Those outer quotes are stripped by the shell and never sent to the agent.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/item/key): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.

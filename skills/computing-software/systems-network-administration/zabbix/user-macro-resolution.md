---
id: computing-software.systems-network-administration.zabbix.user-macro-resolution
name: user-macro-resolution
category: computing-software
field: systems-network-administration
product: zabbix
tags: [user-macros, precedence, global-macros, host-macros, trigger-expression, macro, user]
level: practitioner
status: docs-checked
description: "Define user macros and understand resolution order across host, template depth and global levels."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/macros/user_macros
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
User macros use the syntax {$MACRO}. Names allow uppercase A-Z, 0-9, underscore and dot. They can be global (Administration > Macros), template or host level. Maximum value length is 2048 characters. Value types: Text, Secret text, Vault secret.

Resolution order:
1. Host level macros.
2. Macros of templates linked directly to the host, sorted by template ID.
3. Second-level templates, then third level and so on, each sorted by template ID.
4. Global macros.
If none is found the macro stays unresolved. The same name on several templates of one level uses the lowest template ID, which is a configuration risk.

Practices:
- Prefer host macros to global ones. Adding, updating or deleting global macros forces an incremental configuration update for all hosts.
- If template items or triggers use a macro, define it on the template too, even if it exists globally, so Text macros survive XML export and import. Secret values are not exported.
- Macros are deliberately left unresolved in configuration lists such as the trigger list.
- In trigger expressions, macros resolve only as a parameter or constant, never as a host, item key, function, operator or another expression. Secret macros cannot be used in trigger expressions.
- Typical uses: passwords, ports, file names, regular expressions and thresholds that vary per host.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/macros/user_macros): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.

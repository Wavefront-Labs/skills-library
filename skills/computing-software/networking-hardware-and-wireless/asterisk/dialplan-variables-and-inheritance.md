---
id: computing-software.networking-hardware-and-wireless.asterisk.dialplan-variables-and-inheritance
name: dialplan-variables-and-inheritance
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, variables, set, global, inheritance, substring, exten, uniqueid]
level: practitioner
status: docs-checked
description: "Use Asterisk dialplan variables: Set and dollar-brace substitution, substring syntax, globals, underscore inheritance prefixes, built-ins like EXTEN, and case sensitivity rules."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Variables/Channel-Variables/Setting-and-Substituting-Channel-Variables/
  - https://docs.asterisk.org/Configuration/Dialplan/Variables/Channel-Variables/Variable-Inheritance/
  - https://docs.asterisk.org/Configuration/Dialplan/Variables/Channel-Variables/Case-Sensitivity/
  - https://docs.asterisk.org/Configuration/Dialplan/Variables/Global-Variables-Basics/
  - https://docs.asterisk.org/Configuration/Dialplan/Variables/Manipulating-Variables-Basics/
  - https://docs.asterisk.org/Configuration/Dialplan/Variables/Using-the-CONTEXT-EXTEN-PRIORITY-UNIQUEID-and-CHANNEL-Variables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dialplan variables and inheritance
- Set: `Set(varname=value)`; substitute with `${varname}`. Writing the bare name refers by name, so `Set(${varname1}=value)` assigns to the variable whose name is stored in varname1.
- Substrings: `${NUMBER:2}` skips 2 leading characters (98765 gives 765); `${NUMBER:-2}` returns the last two (65); `${NUMBER:0:3}` returns at most 3 characters.
- Globals: declare under `[globals]` in `extensions.conf`, or `Set(GLOBAL(MYGLOBALVAR)=somevalue)`; read them like channel variables.
- Inheritance: a `_` prefix (`Set(_FOO=bar)`) passes the variable to channels created for the original channel; `__` (two underscores) keeps inheriting through further channels. Setting any version removes the other versions.
- Built-ins: `CONTEXT`, `EXTEN`, `PRIORITY`, `UNIQUEID` (like `1267568856.11`) and `CHANNEL` (channel name).
- Case: from Asterisk 12 all variable evaluation is case-sensitive, so check that names match exactly when upgrading.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Setting-and-Substituting-Channel-Variables, Variable-Inheritance, Case-Sensitivity, Global-Variables-Basics, Manipulating-Variables-Basics, Using-the-CONTEXT-EXTEN-PRIORITY-UNIQUEID-and-CHANNEL-Variables) and confirmed the commands, options, defaults and names stated above. Pre-12 case claim narrowed to what the page states.

Method: documentation only; no commands were run.

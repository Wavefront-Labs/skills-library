---
id: computing-software.networking-hardware-and-wireless.asterisk.ael-asterisk-extension-language
name: ael-asterisk-extension-language
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, ael, extensions-ael, aelparse, dialplan, semantic-checks]
level: advanced
status: docs-checked
description: "Write and check dialplan in AEL: its four underlying syntaxes, case-sensitive keywords, the aelparse checker with -d and -n, and the semantic checks before compiling."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Asterisk-Extension-Language-AEL/Introduction-to-AEL/
  - https://docs.asterisk.org/Configuration/Dialplan/Asterisk-Extension-Language-AEL/AEL-Keywords/
  - https://docs.asterisk.org/Configuration/Dialplan/Asterisk-Extension-Language-AEL/About-aelparse/
  - https://docs.asterisk.org/Configuration/Dialplan/Asterisk-Extension-Language-AEL/AEL-Semantic-Checks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ael: asterisk extension language
AEL describes dialplans in a higher-level syntax (`extensions.ael`) that is compiled into extensions and priorities. It merges four syntaxes: AEL itself, the expression syntax `$[...]`, the variable syntax `${...}`, and the underlying extensions.conf language. One application call is made per priority.

Keywords are case-sensitive: abstract, context, macro, globals, ignorepat, switch, if, ifTime, else, random, goto, jump, local, return, break, continue, regexten, hint, for, while, case, pattern, default (usable as a context name), catch, switches, eswitches, includes. If an application name collides with a keyword, prefer the AEL statement.

Check a file with `aelparse`, built in the source `utils` directory (not installed): `-d` uses the current directory as the config directory (expects `./extensions.ael`); `-n` hides the priority and context calls and shows only parse and semantic errors and warnings.

Semantic checks before compiling include: calls to missing macros or to contexts, wrong macro argument counts, application call to a macro (missing `&`), gotos to missing labels, bad time ranges in `ifTime` and includes, duplicate context names, abstract contexts not included anywhere, and numeric labels.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Introduction-to-AEL, AEL-Keywords, About-aelparse, AEL-Semantic-Checks) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.

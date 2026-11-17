---
id: computing-software.systems-network-administration.zabbix.javascript-preprocessing
name: javascript-preprocessing
category: computing-software
field: systems-network-administration
product: zabbix
tags: [javascript, duktape, preprocessing-step, return-value, macros, preprocessing]
level: advanced
status: docs-checked
description: "Write JavaScript preprocessing steps: the value parameter, return rules, errors, limits and macro handling."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/preprocessing/javascript
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A JavaScript preprocessing step is the body of a function with one parameter named value. Zabbix wraps your code as function (value) { ... } and the returned value is the step result. Example for Fahrenheit to Celsius: return (value - 32) * 5 / 9

Rules:
- value is always a string. The return value is coerced to a string with toString().
- Returning undefined is an error. Returning null discards the value, like Discard value on custom failure.
- Signal errors by throwing a string or Error object: if (value == 0) throw "Zero input value".
- Use var for local variables; do not use undeclared assignments.
- Each script has a 10 second timeout and a 512 megabyte heap limit.
- Bytecode is cached and reset when the item's steps change. Three consecutive runtime failures reinitialise the engine.
- The engine is Duktape. Built-in object methods cannot be redefined.

Macros: user macros (and LLD macros in discovery) are replaced in the code text before execution. They are inserted as-is with no escaping and macro context is ignored, so quote them yourself. Example:
var threshold = '{$THRESHOLD}';
return (!isNaN(threshold) && value > threshold) ? threshold : value;
When testing in the frontend, macros are not resolved; enter values manually.

More examples from the docs: return (Number(value)) converts scientific notation such as 2.62128e+07 to 26212800.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/preprocessing/javascript): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: the claim that the same engine powers script items and webhooks (not on the fetched page).

Method: documentation only; no commands were run.

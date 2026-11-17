---
id: computing-software.systems-network-administration.icinga-2.script-debugger
name: script-debugger
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, script-debugger, debugger, daemon-x, apply-rule-debugging, api-filters]
level: practitioner
status: docs-checked
description: "Debug Icinga 2 apply rules, user functions and API filters with the script debugger: daemon -X, daemon -C -X, the debugger keyword."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/20-script-debugger/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Script debugger
Start the daemon with `-X` (`--script-debugger`): `icinga2 daemon -X`. To debug config validation: `icinga2 daemon -C -X`. When an exception occurs, or the `debugger` keyword is reached, a console opens.

**Typical uses:** configuration errors in apply rules; errors in user-defined functions; server-side errors in REST API filters (a failing filter silently returns an empty result).

**Apply rule example:** `vars += config` fails with `Cannot convert value of type 'String' to an object` because a host custom variable held a string where the rule expected a dictionary. At the prompt, print `vars`, `config`, `host_name`, `name`, or `this` for the whole service object. Leave with `$continue`.

**Breakpoints:** insert `debugger` inside a function, such as a `{{ ... }}` custom variable, and inspect locals (for example `text`) each time it runs.

**API filters:** `host.vars.contains("os")` fails on hosts without custom variables (`Argument is not a callable object`). Guard it: `host.vars && typeof(host.vars) == Dictionary && host.vars.contains("os")`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Icinga 2 Script Debugger chapter. Confirmed: -X and --script-debugger, daemon -C -X, the debugger keyword, the apply rule vars += config example and its error text, printing vars, config, host_name, name and this, $continue, the breakpoint example, API filter failures returning an empty result, and the guarded filter. Removed the claim that the same console is available via icinga2 console, which this page does not state.

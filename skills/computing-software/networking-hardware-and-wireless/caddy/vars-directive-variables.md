---
id: computing-software.networking-hardware-and-wireless.caddy.vars-directive-variables
name: vars-directive-variables
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [vars, variables, placeholders, vars-regexp, type-conversion, caddyfile]
level: practitioner
status: docs-checked
description: "Define request-scoped variables in a Caddyfile with vars, read them via placeholders, matchers and templates, and control the type conversion."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/vars
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stash values early in the chain and use them later.

Syntax: `vars [<matcher>] [<name> <value>]` or a block with one `<name> <value>` per line. Read a variable as the placeholder `{vars.variable_name}`, with the `vars` and `vars_regexp` request matchers, or inside the `templates` directive through the `placeholder` function using the full name `http.vars.variable_name`.

Type conversion: values are converted when possible. `true` and `false` become booleans and numbers become integers or floats; wrap a value in quotes to keep it a string. The page's block shows `abc true` (boolean), `def 1` (integer), `ghi 2.3` (float) and `jkl "example"` (string).

Conditional values work by repeating the directive with matchers; the example is `vars /foo* isFoo "yep"`, `vars isFoo "nope"`, `respond {vars.isFoo}`: paths under `/foo` print `yep` and others print `nope`.

Special case: the variable named `http.auth.user.id` lives in the replacer, and overriding it updates the `user_id` field in access logs, which is a way to label requests authenticated by something other than Caddy's own auth.

The root directive stores the site root in the same store as `http.vars.root`, which is why it is visible to other modules.

## Checked

2026-11-03: read caddyfile/directives/vars against this skill. Confirmed: vars syntax, {vars.name} placeholder, vars_regexp, templates placeholder function, type conversion example, http.auth.user.id special case.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.

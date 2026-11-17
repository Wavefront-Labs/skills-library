---
id: computing-software.networking-hardware-and-wireless.caddy.expression-matcher-cel
name: expression-matcher-cel
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [expression-matcher, cel, boolean-logic, placeholders, heredoc, caddyfile]
level: advanced
status: docs-checked
description: "Use the expression matcher with CEL for and/or logic in the Caddyfile: matcher functions, placeholder preprocessing, backtick and heredoc forms and multi-regexp cases."
sources:
  - https://caddyserver.com/docs/caddyfile/matchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: express conditions that matcher sets (pure AND) cannot.

`expression <cel...>` evaluates a CEL (Common Expression Language) expression returning true or false, supporting `&&`, `||` and parentheses. Most other request matchers work inside it as functions, each with its own CEL syntax, e.g. `path('/api*')`, `method('GET', 'HEAD')`, `host('a.example.com')`, `client_ip('12.23.34.45')`, `header({'Connection':'*Upgrade*'})`, `query({'sort': ['asc','desc']})`, `file()`.

Placeholders (and Caddyfile shorthands such as `{path}`, `{method}`, `{err.status_code}`) are preprocessed into CEL function calls first. If you need a placeholder passed as a string argument to a matcher function, escape the opening brace: `file('\{path}.md')`. Concatenating placeholders requires the long form, e.g. `file({'try_files': [{path}, {path} + '/', 'index.html']})`.

Writing: because the expression is one token, quote it with backticks or a heredoc. If the named matcher consists solely of CEL, the word `expression` can be dropped: ``@mutable `{method}.startsWith("P")` ``. Multi-line: `@api <<CEL` then `{method} == "GET"` and `&& {path}.startsWith("/api/")` then `CEL`, used as `respond @api "Hello, API!"`.

Typical uses: error-status tests (`@404 expression {err.status_code} == 404`), two regexps in one matcher (`path_regexp('^/user/(\w*)') || path_regexp('^/(\w*)')`, impossible with plain `path_regexp` since only one may exist per set), and negation with `!`.

## Checked

2026-11-03: read caddyfile/matchers against this skill. Confirmed: expression syntax, CEL functions, placeholder preprocessing and escaping, backtick and heredoc quoting, dropping the word expression, multi-line form, typical uses.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.

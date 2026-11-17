---
id: computing-software.messaging-and-integration.apache-camel.simple-language
name: simple-language
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, language, simple, expressions, predicates]
level: intro
status: docs-checked
description: "Camel Simple language: ${...} and $simple{} syntax, options trim, trimResult, nested, pretty, resultType, resolveResource, and sub-page map."
sources:
  - https://camel.apache.org/components/next/languages/simple-language.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simple language

Part of camel-core since 1.1; a small Camel-specific scripting language for EIPs and routes. The page recommends Groovy for much more complex cases.

Syntax: `${body}`, `${header.foo}`. Use `$simple{ }` to avoid clashes with Spring property placeholders.

Predicate example: `simple("${header.foo} == 'bar'")`; XML `<simple>${header.foo} == 'bar'</simple>`.

Options (defaults):
- `trim` true (trims whitespace and line breaks from the source)
- `trimResult` false
- `pretty` false (JSON or XML only)
- `nested` false (evaluate a nested simple expression in the result; security category)
- `resultType` class of the result
- `resolveResource` false (a String result starting with `resource:` is loaded as content; values only, not predicates)

Body: any input. A single function such as `${body}` returns its value unchanged; text plus functions returns text; with `resultType` set the result is that class or null.

Details live on sub-pages: Built-in Functions (core, list, boolean, date/time, math, string, XML/JSON), Built-in Operators (comparison, numeric, ternary, elvis, chain, boolean), OGNL Expressions (dot notation to call POJO methods) and Advanced Features (init blocks, custom functions).

Verify: `simple("${header.foo} == 'bar'")` as a `choice` predicate matches only messages with header foo equal to bar.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Camel Simple language page (components/next/languages/simple-language.html). Confirmed: since Camel 1.1, camel-core, Groovy suggested for complex cases, $simple{ } alternative, the option table (trim, trimResult, pretty, nested, resultType, resolveResource and their defaults), the message body table and the four sub-page names. The sub-pages themselves were not opened, so function and operator lists are not asserted.

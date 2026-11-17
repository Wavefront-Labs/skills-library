---
id: computing-software.data-engineering.apache-nifi.expression-language-basics
name: expression-language-basics
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, expression-language, attributes, escaping, subjectless-functions]
level: intro
status: docs-checked
description: "NiFi Expression Language syntax: ${attr}, function chaining, quoting odd names, embedded expressions, resolution order, $$ escaping and subjectless functions."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expression Language basics

- `${filename}` reads an attribute; chain with colons: `${filename:toUpper():equals('HELLO.TXT')}`.
- Quote unusual names: `${"my attribute"}` or `${'my attribute'}`.
- Embed: `${filename:equals( ${uuid} )}`.
- Lookup order (first match wins, null if none): FlowFile attribute, process group variables, custom properties file, NiFi JVM properties, system environment variables.
- Escape: an extra `$` before an expression escapes it (`$${UserName}` stays literal; `$$${abc}` gives `$` plus the value of abc). A number as the first character of an attribute name must be quoted, e.g. `${'5'}`.
- Subjectless functions: `${now()}`, `${UUID()}`, `${nextInt()}`, `${ip()}`, `${hostname(true)}`, `${literal(2):gt(1)}`, `${getStateValue("count")}`.
- After evaluation all attributes are stored as type String; coerce with `toNumber()`, `toDecimal()`, `toString()`. Hex literals must be quoted: `${literal("0xF"):toNumber()}`.

Verify: a processor property using the expression validates and the evaluated value matches the guide's examples.

## Checked

Confirmed against the Expression Language guide (Structure of a NiFi Expression, Hierarchy, Escaping, Subjectless functions, Data type conversion). Removed the Ctrl+Space claim (not on the page).

Method: docs-only read of cited pages, 2026-11-08

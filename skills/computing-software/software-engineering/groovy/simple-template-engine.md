---
id: computing-software.software-engineering.groovy.simple-template-engine
name: simple-template-engine
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, simple-template-engine, groovy-templates]
level: practitioner
status: docs-checked
description: "Render text templates with SimpleTemplateEngine, StreamingTemplateEngine (over 64k) and GStringTemplateEngine, using createTemplate and make."
sources:
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-templates/src/spec/doc/template-engines.adoc
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-templates/src/main/groovy/groovy/text/SimpleTemplateEngine.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SimpleTemplateEngine, StreamingTemplateEngine and GStringTemplateEngine
- `SimpleTemplateEngine` is for basic templates and allows JSP-like scriptlets, script and EL expressions. Usage is `createTemplate(text).make(binding)`.
- `StreamingTemplateEngine` is functionally equivalent but can handle strings larger than 64k. It uses JSP-style `<% %>` script and `<%= %>` expression syntax or GString-style expressions.
- `GStringTemplateEngine` stores the template as writable closures, which is useful for streaming. Templates written for it use `out` rather than `print`.
- Templates may use the normal `${expression}` and `$variable` notations to insert an expression.
- When the template text is embedded in a Groovy script, the script itself parses it first, so backslashes inside GString expressions or scriptlet code must be escaped.

## Gotchas
- Templates can contain code: do not accept template text from untrusted sources.

## Checked

2026-11-03. Confirmed against the Template engines chapter (SimpleTemplateEngine, StreamingTemplateEngine, GStringTemplateEngine, advanced usage note) and the `SimpleTemplateEngine` source (`createTemplate(text).make(binding)`). Removed: the code snippet and self-check, the claims about caching compiled templates, the "method limit" wording, and the claim that output is not escaped.

Method: documentation only; no commands were run.

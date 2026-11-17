---
id: computing-software.software-engineering.groovy.markup-template-engine
name: markup-template-engine
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, markup-template-engine]
level: advanced
status: docs-checked
description: "MarkupTemplateEngine: builder-style templates, layouts and includes, auto-escape and indent options, and optional type-checked models."
sources:
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-templates/src/spec/doc/_markup-template-engine.adoc
  - https://groovy-lang.org/templating.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MarkupTemplateEngine
- Templates are written in a builder-like DSL. They are statically compiled, and type checking of the model is optional.
- Create templates with `createTemplate(String)`, `createTemplate(Reader)`, `createTemplate(URL)` or `createTemplateByPath(String)`. Behaviour is configured through `groovy.text.markup.TemplateConfiguration`.
- `autoEscape` escapes model variables automatically before rendering; `autoIndent` indents after each inserted newline (its string is set by `autoIndentString`, four spaces by default). The guide recommends enabling both `autoIndent` and `autoNewLine` for readable output.
- `yieldUnescaped` renders text without escaping; `includeUnescaped(<name>)` includes a file without escaping. `includeEscaped` and `includeGroovy` also exist, and `include xxx:` is the include form.
- Layouts: a layout template calls `bodyContents()` where the page body should appear.
- To type check, call `createTypeCheckedModelTemplate` with the model types, or declare the types inside the template in a `modelTypes` header (then even `createTemplate` type checks). A type error is reported at template compile time.

## Gotchas
- Never allow `yieldUnescaped` or `includeUnescaped` on untrusted content.

## Checked

2026-11-03. Confirmed against the Markup template engine section of the templating user guide (template creation methods, TemplateConfiguration options, auto escape, includes, layouts, type checked models). Removed: the code snippets, the claim that templates are always compiled with the static type checker (the guide says type checking is optional), the exact `layout` call syntax and the self-check.

Method: documentation only; no commands were run.

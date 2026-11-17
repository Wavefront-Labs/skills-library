---
id: computing-software.software-engineering.groovy.builder-support
name: builder-support
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, builder-support, groovy-builders]
level: advanced
status: docs-checked
description: "Write a custom builder with BuilderSupport/FactoryBuilderSupport and factories; SwingBuilder and ObjectGraphBuilder as examples."
sources:
  - https://groovy-lang.org/dsls.html
  - https://docs.groovy-lang.org/latest/html/gapi/
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-domain-specific-languages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BuilderSupport and FactoryBuilderSupport
- Subclass `BuilderSupport` and override lifecycle methods: `setParent`, `nodeCompleted` and some or all of the `createNode` methods.
- Subclass `FactoryBuilderSupport` for extra features that simplify domain class construction; override lifecycle methods such as `resolveFactory`, `nodeCompleted` and `postInstantiate`.
- Built-in builders documented in the DSL chapter include `MarkupBuilder`, `StreamingMarkupBuilder`, `NodeBuilder`, `CliBuilder`, `ObjectGraphBuilder`, `JmxBuilder` and `FileTreeBuilder`.

## Gotchas
- Choose `BuilderSupport` for maps and lists, `FactoryBuilderSupport` when building domain classes.

## Checked

2026-11-02. Confirmed against the Domain-specific languages chapter (Builders: BuilderSupport, FactoryBuilderSupport, built-in builders). Removed: the `createNode` signatures, `registerFactory`, `JsonBuilder`/`AntBuilder`/`SwingBuilder` in the list, delegate and typo gotchas.

Method: documentation only; no commands were run.

## Self-check
Use `NodeBuilder` to build a tiny tree and walk `children()`.

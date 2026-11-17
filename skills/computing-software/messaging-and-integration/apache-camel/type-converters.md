---
id: computing-software.messaging-and-integration.apache-camel.type-converters
name: type-converters
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, type-converter, converter-annotation, fallback-converter, bulk-loader]
level: advanced
status: docs-checked
description: "Writing Camel type converters: @Converter, @FallbackConverter, generateLoader and generateBulkLoader, allowNull and discovery."
sources:
  - https://camel.apache.org/manual/type-converter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type converters

Add converters by annotating a class with `@Converter` and each conversion method with `@Converter`; every method is one from-to pair. Static methods are recommended; instance methods allow optional dependency injection.

`@FallbackConverter` marks a last-resort method used when regular converters fail. Its signature takes the target `Class`, an optional `Exchange`, the value and a `TypeConverterRegistry`; the method name is free.

Class-level options:
- `generateLoader = true`: fast loading; needs `camel-component-maven-plugin` in the build.
- `generateBulkLoader = true`: merges all converters of the artifact into one generated class, the fastest discovery. Fallback converters are not supported, and method order matters: put the most concrete source type first (`org.w3c.dom.Document` before `org.w3c.dom.Node`).

Method-level: `allowNull = true`. By default a `null` result counts as a miss and Camel stops using that converter.

Discovery: at startup Camel scans JARs for `META-INF/services/org/apache/camel/TypeConverterLoader`, a file of generated loader classes.

Keep converters thread-safe and reentrant. An optional `Exchange` parameter lets a converter read context such as a charset (the byte[] to String converter does).

Use programmatically via `message.getBody(Document.class)` or `TypeConverter.convertTo`.

Verify: `exchange.getIn().getBody(MyType.class)` returns an instance, and the loader file exists in the built jar.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Camel Type Converter manual page. Confirmed: @Converter on class and methods, static methods encouraged, thread-safe and reentrant, @FallbackConverter signature and free method name, generateLoader with the component plugin, generateBulkLoader (Camel 3.7, no fallback converters, concrete types first, Document before Node), allowNull and the null-is-a-miss default, the TypeConverterLoader discovery file, the optional Exchange parameter and the byte[] to String charset example, getBody(Document.class).

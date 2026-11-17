---
id: computing-software.software-engineering.groovy.markup-builder-xmlutil
name: markup-builder-xmlutil
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, markup-builder-xmlutil]
level: practitioner
status: docs-checked
description: "Generate XML with MarkupBuilder and StreamingMarkupBuilder, use the mkp helper, and serialize or escape text with XmlUtil."
sources:
  - https://groovy-lang.org/processing-xml.html
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-xml/src/spec/doc/xml-userguide.adoc
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-xml/src/main/java/groovy/xml/XmlUtil.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MarkupBuilder and XmlUtil
- The XML user guide covers two builders for creating XML: `groovy.xml.MarkupBuilder` and `groovy.xml.StreamingMarkupBuilder`. `MarkupBuilder` writes through a writer you supply, and its values can be any `Object` (serialized to a String).
- A namespace can be declared on a node, and an `XmlSlurper` can register that namespace to read the result.
- `StreamingMarkupBuilder.bind` returns a `Writable`.
- `MarkupBuilderHelper` is the helper accessed through the `mkp` property in both builders; for example `mkp.comment(...)` writes an XML comment and `mkp.yield(...)` prints text with XML entities escaped. `mkp.yieldUnescaped` writes text without escaping, so never use it with untrusted data.
- `groovy.xml.XmlUtil` has `escapeXml` (escapes XML text) and serialization methods; `XmlUtil.newSAXParser` honours the same `allowDocTypeDeclaration` setting as the parsers.

## Checked

2026-11-03. Confirmed against the XML user guide (MarkupBuilder, StreamingMarkupBuilder, MarkupBuilderHelper), the Processing XML chapter (`mkp` helper, `yield`, `allowDocTypeDeclaration`) and the `XmlUtil` source (`escapeXml`). Removed: the code snippet and self-check, the claim that `MarkupBuilder` escapes attributes by default, and the method-name collision note.

Method: documentation only; no commands were run.

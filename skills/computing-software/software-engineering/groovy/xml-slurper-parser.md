---
id: computing-software.software-engineering.groovy.xml-slurper-parser
name: xml-slurper-parser
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, xml-slurper-parser, groovy-xml]
level: practitioner
status: docs-checked
description: "Read XML with XmlSlurper (lazy GPathResult) or XmlParser (Node tree), choose between them, and keep DOCTYPE handling safe."
sources:
  - https://groovy-lang.org/processing-xml.html
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-xml/src/spec/doc/xml-userguide.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XmlSlurper and XmlParser
- Both are based on SAX, so both have a low memory footprint, and both can update or transform the XML.
- `XmlSlurper` returns `groovy.xml.slurpersupport.GPathResult` instances and evaluates the structure lazily: if you update the XML you must evaluate the whole tree again. `XmlParser` returns `Node` objects.
- Use `XmlSlurper` to transform an existing document into another; use `XmlParser` to update and read at the same time.
- Both accept named-parameter configuration, for example `new XmlParser(namespaceAware: false, trimWhitespace: true)`; `trimWhitespace` (default false) is an `XmlParser` option. The slurper's `declareNamespace` is shown in the Processing XML chapter for namespace-aware navigation.
- `allowDocTypeDeclaration` (default false) controls whether DOCTYPE declarations are accepted; a document with one is rejected (SAXParseException) unless you set it. Options that affect the underlying SAX parser (`namespaceAware`, `validating`, `allowDocTypeDeclaration`) must be set before the first parse call, or an `IllegalStateException` is thrown.
- Even with `allowDocTypeDeclaration=true`, external entity references stay constrained by `FEATURE_SECURE_PROCESSING`; supply a custom `EntityResolver` (both classes accept one) only if you need to resolve them in a controlled way.
- GPath navigation: `node.name()` and `node.text()` are used in the chapter's examples, and `node.@id` reads an attribute.

## Checked

2026-11-03. Confirmed against the Processing XML chapter (XmlParser and XmlSlurper differences, configuration options table, allowDocTypeDeclaration and entity resolver sections) and the XML user guide (namespaceAware option). Removed: the code snippet and self-check, `node.attribute('id')`, the multi-node `@id` concatenation claim, and the "unconfirmed per version" default wording.

Method: documentation only; no commands were run.

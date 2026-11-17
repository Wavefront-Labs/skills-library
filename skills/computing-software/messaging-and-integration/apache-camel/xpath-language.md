---
id: computing-software.messaging-and-integration.apache-camel.xpath-language
name: xpath-language
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, language, xpath, xml, namespaces]
level: practitioner
status: docs-checked
description: "Camel XPath language: resultQName NODESET default, saxon and threadSafety flags, in:header and function:properties, namespace registration and namespacesRef."
sources:
  - https://camel.apache.org/components/next/languages/xpath-language.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XPath

Options (prefix `camel.language.xpath.`): `resultQName` NODESET (also NUMBER, STRING, BOOLEAN, NODE), `documentType` `org.w3c.dom.Document`, `saxon` false (true needs `camel-saxon`), `threadSafety` false (applies to multi-element NODESET results), `logNamespaces` false, `preCompile` true. Endpoint-level: `source` (body by default; `header:`, `variable:`, `property:`), `resultType`, `namespacesRef`, `trim` true, `resolveResource` false.

Result types: default `NodeList`; STRING gives `String`; NUMBER gives `Double`; BOOLEAN `Boolean`; NODE `Node`.

Input may be text, bytes, stream, file or DOM. Streams can be read once, so use stream caching or convert to `String` if read repeatedly.

Variables: `in` (namespace `http://camel.apache.org/xml/in/`) is the message; `env` and `system` expose environment and system properties; `out` is deprecated. Unprefixed names resolve in order: `variable(name, value)`, headers, exchange properties, exchange variables.

Functions: `in:body`, `in:header`, `function:properties` (placeholder key), `function:simple`. The last two are not supported when the return type is a NodeSet, e.g. with Split.

Namespaces: Java passes a `Namespaces` object as the second argument; XML declares the prefix on a root element such as `routes` or `route`; YAML lists prefix and URI. Register a `Namespaces` bean and use `namespacesRef` (inline wins).

Examples: `xpath("/person[@name='James']")`; `xpath("/foo:person/@id", String.class)`; `source="header:invoiceDetails"`; Simple `${xpath(/order/@id)}`.

Verify: the String example returns the id attribute text rather than a NodeList.

## Checked

Method: docs-checked 2026-11-09 against the camel.apache.org xpath-language page (options, namespaces, variables, functions, stream bodies, Saxon and Simple sections; read through the Saxon section and grepped the rest).

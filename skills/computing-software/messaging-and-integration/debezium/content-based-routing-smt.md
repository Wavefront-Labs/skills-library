---
id: computing-software.messaging-and-integration.debezium.content-based-routing-smt
name: content-based-routing-smt
category: computing-software
field: messaging-and-integration
product: debezium
tags: [smt, content-based-routing, groovy, scripting]
level: advanced
status: docs-checked
description: "Route events to different topics by content with the ContentBasedRouter SMT and a JSR 223 expression."
sources:
  - https://debezium.io/documentation/reference/stable/transformations/content-based-routing.html
  - https://debezium.io/documentation/reference/stable/transformations/applying-transformations-selectively.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `ContentBasedRouter` evaluates an expression for each event and either reroutes it or leaves it on its default topic.

```
transforms=route
transforms.route.type=io.debezium.transforms.ContentBasedRouter
transforms.route.language=jsr223.groovy
transforms.route.topic.expression=value.op == 'u' ? 'updates' : null
```

A `null` result keeps the default topic. Variables bound into the expression include `key` and `value`, both Kafka Connect `Struct` objects.

Setup, because the SMT is not in the connector archives for security reasons:

1. Download `debezium-scripting-<version>.tar.gz`.
2. Extract it into the Debezium plug-in directories of Kafka Connect.
3. Add a JSR 223 engine implementation and its libraries, for Groovy `groovy`, `groovy-jsr223` and optionally `groovy-json`; for JavaScript `graalvm.js` and `graalvm.js.scriptengine`.
4. Restart Kafka Connect.

Debezium ships no JSR 223 implementation.

Security: once present, anyone who can add a connector to that Connect instance can run scripting expressions. Secure the Connect REST interface first.

Robustness: other messages (heartbeats, tombstones, schema or transaction metadata) have no `op` field and fail the expression. Add a predicate such as `TopicNameMatches` so only data change topics reach the SMT.

Gotcha: a custom-coded SMT needs recompiling for every change, which is why the scripted version exists, but expression typos surface only at runtime.

## Checked

2026-11-08. Confirmed against the Debezium pages transformations/content-based-routing and transformations/applying-transformations-selectively, both read in full: ContentBasedRouter example, Groovy and GraalVM libraries, separate debezium-scripting artifact, security note, bound variables, predicate advice and the TopicNameMatches type. Nothing removed.

Method: documentation only; no commands were run.

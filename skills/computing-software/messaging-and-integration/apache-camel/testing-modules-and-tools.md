---
id: computing-software.messaging-and-integration.apache-camel.testing-modules-and-tools
name: testing-modules-and-tools
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, testing, mock, advicewith, notifybuilder, junit5]
level: intro
status: docs-checked
description: "Camel testing toolbox: camel-test-junit5, main and spring modules, Mock, DataSet, Direct/SEDA/Stub stubs, NotifyBuilder, AdviceWith and Citrus for integration tests."
sources:
  - https://camel.apache.org/manual/testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Camel

Modules:
- `camel-test-junit5`: standalone Camel (no Spring).
- `camel-test-main-junit5`: Camel Main.
- `camel-test-spring-junit5`: Spring and Spring Boot.
- The page also lists JUnit 6 counterparts of the three JUnit 5 modules above.
- `camel-test-infra`: Testcontainers-based infrastructure with JUnit 5 extensions.
- `camel-jbang-test`: Camel CLI plugin for tests during JBang prototyping.

Endpoints for tests:
- **Mock**: set expectations on endpoints, assert at the end.
- **DataSet**: generate large message volumes for load or soak tests.
- **DataSet Test**: load expected messages from another endpoint and compare.

Stub transports:
- **Direct**: synchronous, single-threaded in-VM.
- **SEDA**: asynchronous via a BlockingQueue.
- **Stub**: like SEDA but does not validate the endpoint URI.

Existing routes:
- **NotifyBuilder** signals when a condition occurs (for example five messages completed); conditions combine into expressions.
- **AdviceWith** modifies an existing route with RouteBuilder-style code, e.g. send to a mock and optionally skip the original send.

Integration tests start the whole application with real brokers and services. Citrus (citrusframework.org) can start and stop Camel routes, validate XML/JSON/YAML/plaintext messages and run Camel CLI via JBang; YAKS is built on Citrus for BDD tests on Kubernetes.

Verify: a mock endpoint with `expectedMessageCount(1)` passes `assertIsSatisfied()` after one message.

## Checked

Method: docs-checked 2026-11-09 against the full Testing manual page (read as its raw AsciiDoc source in the apache/camel repository, which builds camel.apache.org/manual/testing.html). The Verify line is the standard Mock usage and is not taken from this page.

---
id: computing-software.messaging-and-integration.apache-camel.validate
name: validate
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, validate, predicate, validation]
level: intro
status: docs-checked
description: "Camel Validate EIP: predicate check that throws PredicateValidationException on mismatch, optional predicateExceptionFactory, body and header examples."
sources:
  - https://camel.apache.org/components/next/eips/validate-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validate

Checks the message with an Expression or Predicate so invalid messages are rejected before processing. If the predicate does not match, a `PredicateValidationException` is thrown and the exchange fails. The body is left unchanged.

Options: `expression` (required), `predicateExceptionFactory` (custom exception factory), `note`, `description`, `disabled` (default `false`; build-time only). No exchange properties.

Java examples:
```java
.validate(bodyAs(String.class).regex("..."))
.validate(header("bar").isGreaterThan(100))
.validate(simple("${header.bar} > 100"))
```
The first style reads files from `inbox` and checks the body against a regex before calling `myServiceBean.processLine`. XML and YAML versions are on the page.

Verify: a header `bar=50` fails validation with `PredicateValidationException`; `bar=150` passes.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Validate EIP page source (validate-eip.adoc) and the Validate model definition (validate.json) from the apache/camel repository, which generate the cited page. Confirmed PredicateValidationException on mismatch, unchanged body, the expression (required) and predicateExceptionFactory options, disabled default false and build-time only, no exchange properties, and the regex, header and Simple examples. Nothing was removed. No commands were run.
